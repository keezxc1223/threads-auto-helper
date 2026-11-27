"""AI 寫文 / 寫留言。支援四種來源（設定頁可切換）：

- claude_cli ：Claude 訂閱登入（透過本機 Claude Code，`claude -p`）
- codex_cli  ：ChatGPT 訂閱登入（透過本機 Codex CLI，`codex exec`）
- claude_api ：Claude API Key（Anthropic SDK）
- openai_api ：OpenAI API Key（OpenAI SDK）
"""
import difflib
import json
import os
import re
import shutil
import subprocess
import tempfile
import uuid

from . import db

FALLBACK_MODELS = {"claude-opus-5-5", "claude-sonnet-5-5", "claude-opus-5", "claude-fable-5-1", "claude-fable-5-2"}
NO_WINDOW = 0x08000000 if os.name == "nt" else 0
WORK_DIR = os.path.join(tempfile.gettempdir(), "threads_helper_ai")
os.makedirs(WORK_DIR, exist_ok=True)

PROVIDERS = {
    "claude_cli": "Claude 訂閱登入",
    "codex_cli": "ChatGPT 訂閱登入",
    "claude_api": "Claude API Key",
    "openai_api": "OpenAI API Key",
}


class AIError(Exception):
    pass


# ---------- 訂閱登入（CLI） ----------
def _cli(name: str) -> str | None:
    return shutil.which(name)


def _run(args: list[str], stdin: str, timeout: int = 240) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(args, input=stdin.encode("utf-8"), capture_output=True, cwd=WORK_DIR,
                              timeout=timeout, creationflags=NO_WINDOW)
    except subprocess.TimeoutExpired:
        raise AIError("AI 回應逾時")


def _ask_claude_cli(system: str, prompt: str) -> str:
    exe = _cli("claude")
    if not exe:
        raise AIError("找不到 Claude Code，請先安裝（npm i -g @anthropic-ai/claude-code）")
    # 用 json 輸出只取最終 result，避免推理過程混進文字
    args = [exe, "-p", "--output-format", "json", "--tools", "", "--no-session-persistence",
            "--strict-mcp-config", "--system-prompt", system]
    model = db.get_setting("cli_model").strip()
    if model:
        args += ["--model", model]
    r = _run(args, prompt)
    raw = r.stdout.decode("utf-8", "replace").strip()
    out, failed = "", True
    try:
        data = json.loads(raw)
        out = (data.get("result") or "").strip()
        failed = bool(data.get("is_error"))
    except ValueError:
        pass
    if r.returncode != 0 or failed or not out:
        err = (r.stderr.decode("utf-8", "replace") or out or raw).strip()
        if "login" in err.lower() or "auth" in err.lower():
            raise AIError("Claude 尚未登入，請到「設定」按「登入 Claude」")
        raise AIError(f"Claude Code 錯誤：{err[:200]}")
    return out


def _ask_codex_cli(system: str, prompt: str) -> str:
    exe = _cli("codex")
    if not exe:
        raise AIError("找不到 Codex CLI，請先安裝（npm i -g @openai/codex）")
    out_file = os.path.join(WORK_DIR, f"codex_{uuid.uuid4().hex}.txt")
    if os.path.exists(out_file):
        os.remove(out_file)
    args = [exe, "exec", "--skip-git-repo-check", "--sandbox", "read-only", "--ephemeral",
            "--color", "never", "-c", "model_reasoning_effort=low", "-o", out_file]
    model = db.get_setting("codex_model").strip()
    if model:
        args += ["-m", model]
    args.append("-")
    full = f"{system}\n\n---\n\n{prompt}\n\n（直接輸出結果文字，不要執行任何指令、不要讀寫檔案。）"
    r = _run(args, full)
    out = ""
    if os.path.exists(out_file):
        with open(out_file, encoding="utf-8", errors="replace") as f:
            out = f.read().strip()
        os.remove(out_file)
    if r.returncode != 0 or not out:
        err = r.stderr.decode("utf-8", "replace").strip()
        if "login" in err.lower() or "auth" in err.lower():
            raise AIError("ChatGPT 尚未登入，請到「設定」按「登入 ChatGPT」")
        raise AIError(f"Codex 錯誤：{err[-200:]}")
    return out


def cli_status() -> dict:
    """回傳兩個訂閱登入的安裝/登入狀態。"""
    res = {}
    exe = _cli("claude")
    st = {"installed": bool(exe), "logged_in": False, "detail": ""}
    if exe:
        try:
            r = subprocess.run([exe, "auth", "status"], capture_output=True, timeout=20, creationflags=NO_WINDOW)
            info = json.loads(r.stdout.decode("utf-8", "replace") or "{}")
            st["logged_in"] = bool(info.get("loggedIn"))
            st["detail"] = info.get("authMethod", "")
        except Exception:
            pass
    res["claude_cli"] = st
    exe = _cli("codex")
    st = {"installed": bool(exe), "logged_in": False, "detail": ""}
    if exe:
        try:
            r = subprocess.run([exe, "login", "status"], capture_output=True, timeout=20, creationflags=NO_WINDOW)
            text = (r.stdout + r.stderr).decode("utf-8", "replace").strip()
            st["logged_in"] = r.returncode == 0 and "logged in" in text.lower() and "not" not in text.lower()
            st["detail"] = text.splitlines()[0] if text else ""
        except Exception:
            pass
    res["codex_cli"] = st
    return res


def open_login(provider: str):
    """開一個主控台視窗讓使用者完成訂閱登入。"""
    cmd = {"claude_cli": "claude auth login", "codex_cli": "codex login"}.get(provider)
    if not cmd:
        raise AIError("此來源不需要登入")
    if not _cli(cmd.split()[0]):
        raise AIError("尚未安裝對應的工具")
    subprocess.Popen(f'start "AI 登入" cmd /k {cmd}', shell=True)


# ---------- API Key ----------
def _ask_claude_api(system: str, prompt: str, max_tokens: int) -> str:
    import anthropic
    key = db.get_setting("api_key").strip()
    if not key:
        raise AIError("尚未設定 Claude API Key")
    model = db.get_setting("model") or "claude-opus-5-5"
    kwargs = dict(model=model, max_tokens=max_tokens, system=system,
                  messages=[{"role": "user", "content": prompt}],
                  output_config={"effort": "low"})
    client = anthropic.Anthropic(api_key=key)
    try:
        if model in FALLBACK_MODELS:
            resp = client.beta.messages.create(betas=["server-side-fallback-2026-07-01"],
                                               fallbacks="default", **kwargs)
        else:
            resp = client.messages.create(**kwargs)
    except anthropic.AuthenticationError:
        raise AIError("Claude API Key 無效")
    except anthropic.RateLimitError:
        raise AIError("Claude API 呼叫太頻繁，稍後再試")
    except anthropic.APIStatusError as e:
        raise AIError(f"Claude API 錯誤（{e.status_code}）：{e.message}")
    except anthropic.APIConnectionError:
        raise AIError("連不上 Claude API，請檢查網路")
    if resp.stop_reason == "refusal":
        raise AIError("AI 拒絕產生這段內容")
    return "".join(b.text for b in resp.content if b.type == "text").strip()


def _ask_openai_api(system: str, prompt: str) -> str:
    import openai
    key = db.get_setting("openai_key").strip()
    if not key:
        raise AIError("尚未設定 OpenAI API Key")
    model = db.get_setting("openai_model").strip()
    if not model:
        raise AIError("請先到「設定」偵測並選擇 OpenAI 模型")
    try:
        resp = openai.OpenAI(api_key=key).responses.create(model=model, instructions=system, input=prompt)
    except openai.AuthenticationError:
        raise AIError("OpenAI API Key 無效")
    except openai.RateLimitError:
        raise AIError("OpenAI 呼叫太頻繁或額度不足")
    except openai.APIStatusError as e:
        raise AIError(f"OpenAI 錯誤（{e.status_code}）：{e.message}")
    except openai.APIConnectionError:
        raise AIError("連不上 OpenAI，請檢查網路")
    return (resp.output_text or "").strip()


def _ask(system: str, prompt: str, max_tokens: int = 4000) -> str:
    p = db.get_setting("ai_provider") or "claude_cli"
    if p == "claude_cli":
        return _ask_claude_cli(system, prompt)
    if p == "codex_cli":
        return _ask_codex_cli(system, prompt)
    if p == "openai_api":
        return _ask_openai_api(system, prompt)
    return _ask_claude_api(system, prompt, max_tokens)


CLAUDE_ALIASES = ["", "fable", "opus", "sonnet", "haiku"]  # "" = Claude Code 預設


def pretty_model(model_id: str) -> str:
    """claude-opus-5-5 → Claude Opus 5.5"""
    m = re.match(r"claude-([a-z]+)-(\d+)(?:-(\d+))?$", model_id or "")
    if not m:
        return model_id
    ver = m.group(2) + (f".{m.group(3)}" if m.group(3) else "")
    return f"Claude {m.group(1).capitalize()} {ver}"


def _probe_claude(alias: str) -> str | None:
    """實際打一次，回傳這個別名目前對應的完整模型 ID；不可用回傳 None。"""
    exe = _cli("claude")
    args = [exe, "-p", "--output-format", "json", "--tools", "", "--no-session-persistence", "--strict-mcp-config"]
    if alias:
        args += ["--model", alias]
    try:
        r = _run(args, "只回覆 OK", timeout=90)
        data = json.loads(r.stdout.decode("utf-8", "replace"))
    except (AIError, ValueError):
        return None
    if r.returncode != 0 or data.get("is_error"):
        return None
    used = list((data.get("modelUsage") or {}).keys())
    return used[0] if used else (alias or "default")


def _codex_default(items: list[dict]) -> str:
    """Codex 預設模型：config.toml 的 model，沒有就用清單第一個。"""
    try:
        import tomllib
        path = os.path.join(os.path.expanduser("~"), ".codex", "config.toml")
        with open(path, "rb") as f:
            m = tomllib.load(f).get("model")
        if m:
            return m
    except (OSError, ValueError):
        pass
    return items[0]["slug"] if items else ""


# ---------- 模型標籤（顯示在模型選單旁） ----------
# kind：top=最強/最貴、rec=推薦、cheap=最省/最快、info=一般、old=舊版、warn=即將停用、def=預設
CLAUDE_FAMILY = {
    "fable": ([["最強", "top"], ["最貴", "top"]], "推理最強，適合長文；額度消耗最多、速度較慢"),
    "mythos": ([["最強", "top"], ["最貴", "top"]], "推理最強；額度消耗最多"),
    "opus": ([["品質高", "info"]], "寫作品質很好，額度消耗中高"),
    "sonnet": ([["推薦", "rec"]], "速度快、品質好，寫貼文和留言 CP 值最高"),
    "haiku": ([["最省", "cheap"], ["最快", "cheap"]], "最快最省，適合大量留言，文筆較簡單"),
}


def _claude_ver(model_id: str):
    m = re.match(r"claude-([a-z]+)-(\d+)(?:-(\d+))?", model_id or "")
    if not m:
        return None, ()
    return m.group(1), (int(m.group(2)), int(m.group(3) or 0))


def _annotate_claude(models: list[dict]) -> list[dict]:
    latest = {}
    for m in models:
        fam, ver = _claude_ver(m.get("version") or m["id"])
        if fam:
            latest[fam] = max(latest.get(fam, ()), ver)
    for m in models:
        fam, ver = _claude_ver(m.get("version") or m["id"])
        tags, desc = CLAUDE_FAMILY.get(fam, ([], ""))
        tags = [list(t) for t in tags]
        if fam and ver < latest.get(fam, ()):
            tags = [["舊版", "old"]]
        m["tags"], m["desc"] = tags, desc
    return models


CODEX_DESC = [  # (英文描述關鍵字, 標籤, 中文說明)
    ("most capable", [["最強", "top"], ["最耗額度", "top"]], "最強的模型，適合複雜任務；額度消耗較多"),
    ("fast, go-to", [["推薦", "rec"]], "快速的日常主力模型，寫貼文留言最划算"),
    ("fast and affordable", [["最省", "cheap"], ["最快", "cheap"]], "快速又省額度，適合簡單任務"),
    ("efficient", [["省額度", "cheap"]], "效率高，擅長看圖與操作電腦"),
    ("previous generation model for complex", [["上一代", "old"]], "上一代的最強模型"),
    ("previous generation", [["上一代", "old"]], "上一代的日常模型"),
    ("legacy", [["舊版", "old"]], "舊版模型"),
]


def _annotate_codex(m: dict) -> tuple[list, str]:
    d = (m.get("description") or "").lower()
    tags, desc = [], m.get("description") or ""
    for key, t, zh in CODEX_DESC:
        if key in d:
            tags, desc = [list(x) for x in t], zh
            break
    upg = m.get("upgrade") or {}
    if upg.get("retirement_at"):
        tags.append([f"{upg['retirement_at'][5:7].lstrip('0')}/{upg['retirement_at'][8:10]} 停用", "warn"])
    return tags, desc


def _with_default(entries: list[dict], default_id: str, label: str) -> list[dict]:
    """在最前面加一筆「預設模型」，標籤沿用它實際對應的模型。"""
    src = next((e for e in entries if e["version"] == default_id), None)
    if not src:
        return entries
    return [{"id": "", "name": f"預設模型：{label}", "version": default_id,
             "tags": [["預設", "def"]] + src.get("tags", []), "desc": src.get("desc", "")}] + entries


def list_models(provider: str) -> list[dict]:
    """偵測目前登入／金鑰可用的模型，回傳 [{id, name, version}]。訂閱模式的第一筆 id="" 代表預設。"""
    if provider == "claude_cli":
        if not _cli("claude"):
            raise AIError("尚未安裝 Claude Code")
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(5) as ex:
            got = list(ex.map(_probe_claude, CLAUDE_ALIASES))
        models = [{"id": a, "name": pretty_model(v), "version": v}
                  for a, v in zip(CLAUDE_ALIASES, got) if v and a]
        if not models:
            raise AIError("偵測不到可用模型，請確認 Claude 已登入")
        _annotate_claude(models)
        if got[0]:
            models = _with_default(models, got[0], pretty_model(got[0]))
        return models
    if provider == "codex_cli":
        exe = _cli("codex")
        if not exe:
            raise AIError("尚未安裝 Codex CLI")
        r = subprocess.run([exe, "debug", "models"], capture_output=True, timeout=60, creationflags=NO_WINDOW)
        try:
            data = json.loads(r.stdout.decode("utf-8", "replace"))
        except ValueError:
            raise AIError("讀取 Codex 模型清單失敗")
        items = sorted([m for m in data.get("models", []) if m.get("visibility") == "list"],
                       key=lambda m: m.get("priority") or 0)
        entries = []
        for m in items:
            tags, desc = _annotate_codex(m)
            entries.append({"id": m["slug"], "name": m.get("display_name") or m["slug"], "version": m["slug"],
                            "tags": tags, "desc": desc})
        default = _codex_default(items)
        names = {e["id"]: e["name"] for e in entries}
        return _with_default(entries, default, names.get(default, default))
    if provider == "claude_api":
        import anthropic
        key = db.get_setting("api_key").strip()
        if not key:
            raise AIError("請先填入 Claude API Key 並儲存")
        try:
            models = [{"id": m.id, "name": m.display_name, "version": m.id}
                      for m in anthropic.Anthropic(api_key=key).models.list(limit=100)]
            return _annotate_claude(models)
        except anthropic.AuthenticationError:
            raise AIError("Claude API Key 無效")
        except anthropic.APIError as e:
            raise AIError(f"讀取模型失敗：{e}")
    if provider == "openai_api":
        import openai
        key = db.get_setting("openai_key").strip()
        if not key:
            raise AIError("請先填入 OpenAI API Key 並儲存")
        try:
            ids = [m.id for m in openai.OpenAI(api_key=key).models.list()]
        except openai.AuthenticationError:
            raise AIError("OpenAI API Key 無效")
        except openai.APIError as e:
            raise AIError(f"讀取模型失敗：{e}")
        bad = ("audio", "realtime", "tts", "transcribe", "embedding", "image", "search", "moderation", "dall-e", "whisper", "instruct")
        ids = sorted((i for i in ids if (i.startswith("gpt") or i[:2] in ("o1", "o3", "o4")) and not any(b in i for b in bad)),
                     reverse=True)
        out = []
        for i in ids:
            tags = [["最省", "cheap"]] if ("nano" in i or "mini" in i) else []
            out.append({"id": i, "name": i, "version": i, "tags": tags, "desc": ""})
        return out
    raise AIError("未知的 AI 來源")


MODEL_SETTING = {"claude_cli": "cli_model", "codex_cli": "codex_model", "claude_api": "model", "openai_api": "openai_model"}


def test() -> str:
    text = _ask("你是測試助手。", "請輸出 <reply>連線成功</reply>，不要其他內容。", 200)
    found = _tagged(text, "reply")
    if not found:
        raise AIError(f"AI 有回應但格式不對：{text[:80]}")
    return found[-1]


# ---------- 內容 ----------
BASE_STYLE = """你在台灣經營 Threads（脆）帳號。寫作規則：
- 一律使用台灣繁體中文與台灣口語，語氣自然像真人，不要像廣告或 AI。
- 不要用 emoji 開頭，不要堆砌 hashtag（最多 1 個，可以不用）。
- 不要寫「身為一個…」「總而言之」這類 AI 腔。"""


def _tagged(text: str, tag: str) -> list[str]:
    """只取 <tag>...</tag> 內的文字，避免模型的思考過程混進來。"""
    return [m.strip() for m in re.findall(rf"<{tag}>(.*?)</{tag}>", text, flags=re.S) if m.strip()]


def write_posts(topic: str, persona: str, count: int = 3, length: str = "中", avoid: list[str] | None = None) -> list[str]:
    brand = db.get_setting("brand_persona")
    length_hint = {"短": "每篇 30 字以內", "中": "每篇 60～150 字", "長": "每篇 200～400 字，可分段"}.get(length, "每篇 60～150 字")
    system = BASE_STYLE + (f"\n\n帳號定位：{brand}" if brand else "") + (f"\n\n本次風格：{persona}" if persona else "")
    prompt = (f"主題：{topic}\n\n請寫 {count} 篇彼此角度不同的 Threads 貼文，{length_hint}，每篇不超過 500 字。"
              "容易引起留言互動（例如結尾拋一個問題），但不要每篇都同一招。\n"
              "每篇貼文完整放在 <post> 和 </post> 之間，標籤外面不要寫任何東西，不要編號、不要標題。")
    if avoid:
        prompt += ("\n\n以下是這個帳號最近發過的文，不要重複類似的開頭、角度或句子：\n"
                   + "\n---\n".join(a[:200] for a in avoid))
    text = _ask(system, prompt)
    parts = _tagged(text, "post")
    if not parts and "=====" in text:  # 模型沒照格式時的退路
        parts = [p.strip() for p in text.split("=====") if p.strip()]
    if not parts:
        raise AIError("AI 回傳格式不正確，請再試一次")
    return [p[:500] for p in parts][:count]


def _norm(s: str) -> str:
    return re.sub(r"[\s\W_]+", "", s.lower())


def too_similar(text: str, others: list[str], threshold: float = 0.55) -> bool:
    """跟任何一則舊留言太像（整體相似或開頭相同）就算重複。"""
    a = _norm(text)
    if not a:
        return False
    for o in others:
        b = _norm(o)
        if not b:
            continue
        if a == b or a[:6] == b[:6] or difflib.SequenceMatcher(None, a, b).ratio() >= threshold:
            return True
    return False


def _comment_once(post_text: str, author: str, persona: str, keyword: str, avoid: list[str], strict: bool) -> str | None:
    brand = db.get_setting("brand_persona")
    system = (BASE_STYLE + (f"\n\n帳號定位：{brand}" if brand else "")
              + f"\n\n留言策略：{persona or '真誠地參與討論，提供有用的看法'}")
    prompt = (f"以下是在 Threads 搜尋「{keyword}」找到的一篇貼文（作者 @{author}）：\n"
              f"<thread_post>\n{post_text[:1500]}\n</thread_post>\n\n"
              "請寫一則回覆留言：1～2 句、40 字以內、要針對這篇貼文的具體內容回應（提到貼文裡的細節），"
              "讀起來像真人隨手留言。不要放連結，不要硬推銷，不要每次都用問句。\n"
              "抱怨、提問、求推薦、分享經驗的貼文都是好的留言機會，要回。"
              "只有在貼文跟主題完全無關，或是政治、喪事、意外災難這類敏感話題時，才輸出 <reply>SKIP</reply>。\n")
    if avoid:
        prompt += ("\n這個帳號最近已經留過下面這些留言。新留言絕對不能跟它們重複，"
                   "開頭、句型、用詞、切入角度都要換：\n<past>\n" + "\n".join(f"- {a}" for a in avoid[:30]) + "\n</past>\n")
    if strict:
        prompt += "\n注意：你上一版寫得跟過去的留言太像了，這次換一個完全不同的開頭和說法。\n"
    prompt += "\n最後把留言完整放在 <reply> 和 </reply> 之間。"
    text = _ask(system, prompt, max_tokens=1000)
    found = _tagged(text, "reply")
    if not found:
        return FORMAT_ERROR
    out = found[-1].strip("「」\"")
    if not out or out.upper().startswith("SKIP"):
        return None
    if len(out) > 200:
        return FORMAT_ERROR
    return out


FORMAT_ERROR = "__FORMAT_ERROR__"


def draft_comment(post_text: str, author: str, persona: str, keyword: str,
                  avoid: list[str] | None = None) -> str | None:
    """回傳留言文字；判斷不適合留言、或重寫後仍和舊留言太像時回傳 None。"""
    avoid = avoid or []
    similar = False
    for _ in range(4):
        out = _comment_once(post_text, author, persona, keyword, avoid, strict=similar)
        if out is None:
            return None
        if out == FORMAT_ERROR:
            continue
        if not too_similar(out, avoid):
            return out
        similar = True
    return None


