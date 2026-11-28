import base64
import json
import os
import time
import uuid
from datetime import datetime, timedelta

from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import ai, db, threads_bot
from . import worker as worker_mod
from . import __version__
from .cdp import Browser
from .worker import next_comment_time, recent_comments, worker

WEB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "web")

app = FastAPI()


def _err(e: Exception):
    raise HTTPException(400, str(e))


def _norm_time(s: str | None) -> str:
    if not s:
        return db.now()
    s = s.replace("T", " ")
    return s + ":00" if len(s) == 16 else s


# ---------- 總覽 ----------
@app.get("/api/state")
def state():
    t = db.today() + "%"
    return {
        "version": __version__,
        "running": db.get_setting("worker_running") == "1",
        "busy": worker.busy,
        "activity": {**worker_mod.ACT, "elapsed": int(time.time() - worker_mod.ACT["since"]) if worker_mod.ACT["since"] else 0},
        "upcoming": worker_mod.upcoming(),
        "ai_provider": ai.PROVIDERS.get(db.get_setting("ai_provider"), ""),
        "accounts": db.one("SELECT COUNT(*) n FROM accounts")["n"],
        "scheduled": db.one("SELECT COUNT(*) n FROM posts WHERE status='scheduled'")["n"],
        "posted_today": db.one("SELECT COUNT(*) n FROM posts WHERE status='sent' AND posted_at LIKE ?", (t,))["n"],
        "autopost": db.one("SELECT COUNT(*) n FROM autopost WHERE enabled=1")["n"],
        "hourly_limit": db.get_int("hourly_comment_limit"),
        "next_comment": next_comment_time(),
        "queued": db.one("SELECT COUNT(*) n FROM comments WHERE status='approved'")["n"],
        "pending_comments": db.one("SELECT COUNT(*) n FROM comments WHERE status='pending'")["n"],
        "pending_posts": db.one("SELECT COUNT(*) n FROM posts WHERE status='pending'")["n"],
        "commented_today": db.one("SELECT COUNT(*) n FROM comments WHERE status='sent' AND sent_at LIKE ?", (t,))["n"],
        "tasks": db.one("SELECT COUNT(*) n FROM tasks WHERE enabled=1")["n"],
    }


@app.post("/api/worker/toggle")
def toggle():
    on = db.get_setting("worker_running") != "1"
    db.set_setting("worker_running", "1" if on else "0")
    db.log("自動排程已啟動" if on else "自動排程已暫停", "ok" if on else "warn")
    worker.wake.set()
    return {"running": on}


# ---------- 帳號 ----------
@app.get("/api/accounts")
def accounts():
    rows = db.all("SELECT * FROM accounts ORDER BY id")
    for r in rows:
        r["browser_open"] = Browser(r["id"]).running()
    return rows


@app.post("/api/accounts")
def add_account(data: dict = Body(...)):
    name = (data.get("name") or "").strip() or "未命名帳號"
    aid = db.run("INSERT INTO accounts(name,created_at) VALUES(?,?)", (name, db.now()))
    return {"id": aid}


@app.put("/api/accounts/{aid}")
def rename_account(aid: int, data: dict = Body(...)):
    db.run("UPDATE accounts SET name=? WHERE id=?", (data.get("name", "").strip(), aid))
    return {"ok": True}


@app.delete("/api/accounts/{aid}")
def del_account(aid: int):
    Browser(aid).close()
    db.run("DELETE FROM accounts WHERE id=?", (aid,))
    db.run("DELETE FROM tasks WHERE account_id=?", (aid,))
    db.run("DELETE FROM autopost WHERE account_id=?", (aid,))
    db.run("DELETE FROM posts WHERE account_id=? AND status IN ('scheduled','draft')", (aid,))
    return {"ok": True}


@app.post("/api/accounts/{aid}/open")
def open_browser(aid: int):
    try:
        Browser(aid).launch("https://www.threads.com/login")
    except Exception as e:
        _err(e)
    return {"ok": True}


@app.post("/api/accounts/{aid}/close")
def close_browser(aid: int):
    Browser(aid).close()
    return {"ok": True}


@app.post("/api/accounts/{aid}/check")
def check_account(aid: int):
    try:
        st = threads_bot.check_login(aid)
    except Exception as e:
        _err(e)
    db.run("UPDATE accounts SET logged_in=?, username=CASE WHEN ?<>'' THEN ? ELSE username END, checked_at=? WHERE id=?",
           (1 if st.get("logged") else 0, st.get("username", ""), st.get("username", ""), db.now(), aid))
    return st


# ---------- 發文 ----------
@app.get("/api/posts")
def posts():
    return db.all("""SELECT p.*, a.name account_name FROM posts p LEFT JOIN accounts a ON a.id=p.account_id
                     ORDER BY CASE p.status WHEN 'pending' THEN 0 WHEN 'scheduled' THEN 0 WHEN 'sending' THEN 0 WHEN 'draft' THEN 1 ELSE 2 END,
                     CASE WHEN p.status IN ('pending','scheduled','sending','draft') THEN p.scheduled_at END ASC,
                     p.posted_at DESC, p.id DESC LIMIT 300""")


@app.post("/api/posts")
def add_posts(data: dict = Body(...)):
    """data: {account_id, items:[{text, images, scheduled_at}]}"""
    aid = int(data["account_id"])
    ids = []
    for it in data.get("items", []):
        text = (it.get("text") or "").strip()
        if not text:
            continue
        ids.append(db.run("INSERT INTO posts(account_id,text,images,scheduled_at,status,created_at) VALUES(?,?,?,?,?,?)",
                          (aid, text, json.dumps(it.get("images") or []), _norm_time(it.get("scheduled_at")),
                           "scheduled", db.now())))
    worker.wake.set()
    return {"ids": ids}


@app.put("/api/posts/{pid}")
def edit_post(pid: int, data: dict = Body(...)):
    db.run("UPDATE posts SET text=?, scheduled_at=?, account_id=?, status='scheduled', error='' WHERE id=?",
           (data["text"], _norm_time(data.get("scheduled_at")), int(data["account_id"]), pid))
    worker.wake.set()
    return {"ok": True}


@app.post("/api/posts/{pid}/now")
def post_now(pid: int):
    db.run("UPDATE posts SET scheduled_at=?, status='scheduled', error='' WHERE id=?", (db.now(), pid))
    worker.wake.set()
    return {"ok": True}


@app.post("/api/posts/find_urls")
def find_post_urls():
    """替已發佈但沒有連結的貼文，到個人檔案頁比對內文補上連結。"""
    rows = db.all("SELECT id, account_id, text FROM posts WHERE status='sent' AND COALESCE(url,'')='' ORDER BY posted_at DESC")
    found = 0
    by_acc: dict = {}
    for r in rows:
        by_acc.setdefault(r["account_id"], []).append(r)
    for aid, items in by_acc.items():
        acc = db.one("SELECT username FROM accounts WHERE id=?", (aid,))
        if not acc:
            continue
        try:
            urls = threads_bot.find_post_urls(aid, acc.get("username", ""), [x["text"] for x in items])
        except Exception as e:
            _err(e)
        for i, url in urls.items():
            db.run("UPDATE posts SET url=? WHERE id=?", (url, items[i]["id"]))
            found += 1
    return {"found": found, "missing": len(rows) - found}


@app.delete("/api/posts/{pid}")
def del_post(pid: int):
    db.run("DELETE FROM posts WHERE id=? AND status<>'sending'", (pid,))
    return {"ok": True}


@app.post("/api/upload")
def upload(data: dict = Body(...)):
    """data: {name, data(base64)}"""
    ext = os.path.splitext(data.get("name", ""))[1].lower() or ".jpg"
    if ext not in (".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov", ".webm", ".avif"):
        _err(ValueError("只支援圖片或影片"))
    raw = data["data"].split(",", 1)[-1]
    path = os.path.join(db.UPLOAD_DIR, uuid.uuid4().hex + ext)
    with open(path, "wb") as f:
        f.write(base64.b64decode(raw))
    return {"path": path}


@app.get("/api/file")
def get_file(path: str):
    full = os.path.abspath(path)
    if not full.startswith(os.path.abspath(db.UPLOAD_DIR)) or not os.path.exists(full):
        raise HTTPException(404)
    return FileResponse(full)


@app.post("/api/ai/posts")
def ai_posts(data: dict = Body(...)):
    try:
        items = ai.write_posts(data.get("topic", ""), data.get("persona", ""),
                               int(data.get("count", 3)), data.get("length", "中"))
    except Exception as e:
        _err(e)
    return {"items": items}


@app.post("/api/schedule/plan")
def plan(data: dict = Body(...)):
    """依起始時間與間隔區間產生時間表。"""
    start = datetime.strptime(_norm_time(data.get("start")), "%Y-%m-%d %H:%M:%S")
    lo, hi = int(data.get("gap_min", 60)), int(data.get("gap_max", 120))
    import random
    out, t = [], start
    for i in range(int(data.get("count", 1))):
        if i:
            t += timedelta(minutes=random.randint(lo, max(lo, hi)))
        out.append(t.strftime("%Y-%m-%d %H:%M:00"))
    return {"times": out}


@app.put("/api/comments/{cid}")
def edit_comment(cid: int, data: dict = Body(...)):
    db.run("UPDATE comments SET draft=? WHERE id=? AND status<>'sending'", ((data.get("draft") or "").strip(), cid))
    return {"ok": True}


# ---------- 自動發文規則 ----------
AUTO_FIELDS = ["enabled", "topics", "persona", "per_day", "start_hour", "end_hour", "length", "review", "images"]


def _imgs(v) -> str:
    """圖片清單存成 JSON，最多 5 張。"""
    if isinstance(v, str):
        try:
            v = json.loads(v or "[]")
        except ValueError:
            v = []
    return json.dumps([str(x) for x in (v or [])][:5], ensure_ascii=False)


@app.get("/api/autopost")
def autopost():
    out = []
    for a in db.all("SELECT id, name, username FROM accounts ORDER BY id"):
        r = db.one("SELECT * FROM autopost WHERE account_id=?", (a["id"],)) or {
            "account_id": a["id"], "enabled": 0, "topics": "", "persona": "", "per_day": 3,
            "start_hour": 9, "end_hour": 23, "length": "中", "review": 0, "images": "[]", "next_at": ""}
        r["account_name"] = a["name"]
        r["username"] = a["username"]
        r["today"] = db.one("""SELECT COUNT(*) n FROM posts WHERE account_id=? AND source='auto' AND posted_at LIKE ?""",
                            (a["id"], db.today() + "%"))["n"]
        out.append(r)
    return out


@app.put("/api/autopost/{aid}")
def save_autopost(aid: int, data: dict = Body(...)):
    data["images"] = _imgs(data.get("images"))
    vals = [data.get(k) for k in AUTO_FIELDS]
    if int(data.get("start_hour", 0)) >= int(data.get("end_hour", 24)):
        _err(ValueError("開始時間要早於結束時間"))
    db.run(f"""INSERT INTO autopost(account_id,{','.join(AUTO_FIELDS)},next_at) VALUES(?,{','.join('?' * len(AUTO_FIELDS))},'')
               ON CONFLICT(account_id) DO UPDATE SET {','.join(k + '=excluded.' + k for k in AUTO_FIELDS)}, next_at=''""",
           (aid, *vals))
    worker.wake.set()
    return {"ok": True}


# ---------- 海巡 ----------
@app.get("/api/tasks")
def tasks():
    return db.all("SELECT t.*, a.name account_name FROM tasks t LEFT JOIN accounts a ON a.id=t.account_id ORDER BY t.id")


TASK_FIELDS = ["account_id", "name", "keywords", "recent", "persona", "length", "mode", "interval_min", "max_per_run", "min_likes", "enabled", "images"]


@app.post("/api/tasks")
def add_task(data: dict = Body(...)):
    data["images"] = _imgs(data.get("images"))
    vals = [data.get(k) for k in TASK_FIELDS]
    tid = db.run(f"INSERT INTO tasks({','.join(TASK_FIELDS)},created_at) VALUES({','.join('?' * len(TASK_FIELDS))},?)",
                 (*vals, db.now()))
    worker.wake.set()
    return {"id": tid}


@app.put("/api/tasks/{tid}")
def edit_task(tid: int, data: dict = Body(...)):
    if "images" in data:
        data["images"] = _imgs(data["images"])
    keys = [k for k in TASK_FIELDS if k in data]
    db.run(f"UPDATE tasks SET {','.join(k + '=?' for k in keys)} WHERE id=?", (*[data[k] for k in keys], tid))
    worker.wake.set()
    return {"ok": True}


@app.post("/api/tasks/{tid}/run")
def run_task_now(tid: int):
    db.run("UPDATE tasks SET last_run='', enabled=1 WHERE id=?", (tid,))
    worker.wake.set()
    return {"ok": True}


@app.delete("/api/tasks/{tid}")
def del_task(tid: int):
    db.run("DELETE FROM tasks WHERE id=?", (tid,))
    return {"ok": True}


# ---------- 留言 ----------
@app.get("/api/comments")
def comments(status: str = "pending"):
    st = status.split(",")
    return db.all(f"""SELECT c.*, a.name account_name FROM comments c LEFT JOIN accounts a ON a.id=c.account_id
                      WHERE c.status IN ({','.join('?' * len(st))}) ORDER BY c.id DESC LIMIT 300""", st)


@app.post("/api/comments/{cid}/retry")
def approve(cid: int, data: dict = Body(default={})):
    draft = (data.get("draft") or "").strip()
    if draft:
        db.run("UPDATE comments SET draft=? WHERE id=?", (draft, cid))
    c = db.one("SELECT draft FROM comments WHERE id=?", (cid,))
    if not c:
        raise HTTPException(404)
    if not (c["draft"] or "").strip():
        raise HTTPException(400, "這則沒有留言內容，請先填寫或按「重寫」")
    db.run("UPDATE comments SET status='approved', error='' WHERE id=? AND status IN ('pending','failed','skipped','rejected')", (cid,))
    worker.wake.set()
    return {"ok": True}


@app.post("/api/comments/approve_all")
def approve_all():
    db.run("UPDATE comments SET status='approved', error='' WHERE status='pending'")
    worker.wake.set()
    return {"ok": True}


@app.post("/api/comments/{cid}/cancel")
def cancel(cid: int):
    db.run("UPDATE comments SET status='rejected' WHERE id=? AND status IN ('approved','pending')", (cid,))
    return {"ok": True}


@app.post("/api/comments/{cid}/redraft")
def redraft(cid: int):
    c = db.one("SELECT c.*, t.persona, t.length FROM comments c LEFT JOIN tasks t ON t.id=c.task_id WHERE c.id=?", (cid,))
    if not c:
        raise HTTPException(404)
    try:
        avoid = [x for x in recent_comments(c["account_id"]) if x != c["draft"]] + ([c["draft"]] if c["draft"] else [])
        d = ai.draft_comment(c["post_text"], c["author"], c.get("persona") or "", c["keyword"], avoid,
                             length=c.get("length") or "中")
    except Exception as e:
        _err(e)
    if d:
        db.run("UPDATE comments SET draft=? WHERE id=?", (d, cid))
    return {"draft": d or ""}


# ---------- 設定 / 紀錄 ----------
@app.get("/api/settings")
def get_settings():
    s = {k: db.get_setting(k) for k in db.DEFAULT_SETTINGS}
    for k in ("api_key", "openai_key"):
        key = s.pop(k)
        s[k + "_masked"] = (key[:7] + "…" + key[-4:]) if len(key) > 16 else ("已設定" if key else "")
    s["providers"] = ai.PROVIDERS
    s["models"] = {}
    for p in ai.PROVIDERS:
        try:
            s["models"][p] = json.loads(db.get_setting(f"models_{p}") or "[]")
        except ValueError:
            s["models"][p] = []
    return s


@app.put("/api/settings")
def put_settings(data: dict = Body(...)):
    for k, v in data.items():
        if k in db.DEFAULT_SETTINGS and k not in ("worker_running", "ai_tested"):
            if k in ("api_key", "openai_key") and not str(v).strip():
                continue
            if k in ("ai_provider", "api_key", "openai_key", "model", "openai_model", "cli_model", "codex_model") \
                    and db.get_setting(k) != str(v).strip():
                db.set_setting("ai_tested", "0")
            db.set_setting(k, str(v).strip())
    return {"ok": True}


@app.get("/api/ai/status")
def ai_status():
    return ai.cli_status()


@app.post("/api/ai/login")
def ai_login(data: dict = Body(...)):
    try:
        ai.open_login(data.get("provider", ""))
    except Exception as e:
        _err(e)
    return {"ok": True}


@app.post("/api/ai/models")
def ai_models(data: dict = Body(...)):
    """偵測可用模型並快取；目前選的模型不在清單內時自動改選第一個。"""
    provider = data.get("provider", "")
    try:
        models = ai.list_models(provider)
    except Exception as e:
        _err(e)
    db.set_setting(f"models_{provider}", json.dumps(models, ensure_ascii=False))
    key = ai.MODEL_SETTING[provider]
    ids = [m["id"] for m in models]
    cur = db.get_setting(key)
    if models and cur not in ids and not (provider.endswith("_cli") and cur == ""):
        db.set_setting(key, ids[0])
        db.set_setting("ai_tested", "0")
    return {"models": models, "selected": db.get_setting(key)}


@app.post("/api/ai/test")
def ai_test():
    try:
        out = ai.test()
    except Exception as e:
        _err(e)
    db.set_setting("ai_tested", "1")
    return {"reply": out}


@app.get("/api/logs")
def logs(after: int = 0):
    if after:
        return db.all("SELECT * FROM logs WHERE id>? ORDER BY id", (after,))
    return list(reversed(db.all("SELECT * FROM logs ORDER BY id DESC LIMIT 200")))


@app.get("/")
def index():
    return FileResponse(os.path.join(WEB_DIR, "index.html"))


app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")
