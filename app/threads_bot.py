"""Threads 網頁操作。DOM 結構於 2026-11-27 實地勘查 threads.com 確認：

- 搜尋頁：/search?q=<kw>&serp_type=default，分頁連結 a[aria-label="最相關"] / a[aria-label="最近"]
- 每篇貼文容器：div[data-pressable-container="true"]，內含 a[href="/@user/post/<code>"]、<time datetime>
  與多個 span[dir="auto"]（作者、話題、日期、"翻譯"、內文、讚數…）
- 貼文頁回覆框：[contenteditable][role="textbox"]，aria-placeholder 為「回覆xxx……」（Lexical 編輯器）
  送出鈕是同區塊內的 [role="button"]，其 svg <title> 為「回覆」
- 發文：左下「新串文」按鈕（必須真實滑鼠點擊，element.click() 無效）→ div[role="dialog"]
  內的 contenteditable（placeholder「有什麼新鮮事？」）、input[type=file]、文字為「發佈」的按鈕
"""
import json
import os
import random
import re
import time
import urllib.parse
from datetime import datetime, timedelta, timezone

from .cdp import Browser, CDPError, Page

HOME = "https://www.threads.com/"

JS_LOGIN_STATE = r"""(() => {
  const t = document.body ? document.body.innerText : '';
  const btns = [...document.querySelectorAll('[role="button"],a')].map(b => b.innerText.trim());
  const logged = btns.includes('新串文') || btns.includes('發佈');
  let username = '';
  for (const a of document.querySelectorAll('a[href^="/@"]')) {
    const label = (a.getAttribute('aria-label') || '') + (a.innerText || '');
    const svgLabel = [...a.querySelectorAll('svg[aria-label]')].map(s => s.getAttribute('aria-label')).join('');
    if (/個人檔案|Profile/.test(label + svgLabel) && /^\/@[^/]+$/.test(a.getAttribute('href'))) {
      username = a.getAttribute('href').slice(2); break;
    }
  }
  const loginWall = /登入或註冊|使用 Instagram 帳號繼續|Log in or sign up/.test(t);
  return {logged: logged && !loginWall, username};
})()"""

JS_EXTRACT_POSTS = r"""(() => {
  const parseNum = s => {
    s = s.replace(/,/g, '').trim();
    let m = s.match(/^([\d.]+)\s*(萬|K|k|M)?$/);
    if (!m) return null;
    let n = parseFloat(m[1]);
    if (m[2] === '萬') n *= 10000; else if (m[2] === 'K' || m[2] === 'k') n *= 1000; else if (m[2] === 'M') n *= 1e6;
    return Math.round(n);
  };
  const out = [], seen = new Set();
  for (const c of document.querySelectorAll('div[data-pressable-container="true"]')) {
    const href = [...c.querySelectorAll('a[href*="/post/"]')].map(a => a.getAttribute('href'))
      .find(h => /^\/@[^/]+\/post\/[^/?]+$/.test(h));
    if (!href || seen.has(href)) continue;
    seen.add(href);
    const author = href.split('/')[1].slice(1);
    const time = c.querySelector('time');
    const dateText = time ? time.innerText.trim() : '';
    let spans = [...c.querySelectorAll('span[dir="auto"]')].map(s => s.innerText.trim()).filter(Boolean);
    spans = spans.filter((s, i) => spans.indexOf(s) === i);
    let start = dateText ? spans.indexOf(dateText) + 1 : 0;
    const rest = spans.slice(start).filter(s => s !== '翻譯' && s !== author);
    const textParts = [], nums = [];
    for (const s of rest) {
      const n = parseNum(s);
      if (n !== null) nums.push(n); else textParts.push(s.replace(/\n\d+\n\/\n\d+\s*$/, '').trim());
    }
    out.push({
      url: 'https://www.threads.com' + href,
      author,
      time: time ? time.getAttribute('datetime') : '',
      text: textParts.join('\n').trim(),
      likes: nums.length ? nums[0] : 0,
      replies: nums.length > 1 ? nums[1] : 0,
    });
  }
  return out;
})()"""

JS_REPLY_BOX = r"""[...document.querySelectorAll('[contenteditable="true"][role="textbox"]')]
  .find(e => (e.getAttribute('aria-placeholder') || '').startsWith('回覆'))"""

JS_REPLY_SUBMIT = r"""(() => {
  const ed = %s;
  if (!ed) return null;
  let p = ed;
  for (let i = 0; i < 8 && p; i++) {
    p = p.parentElement;
    if (!p) break;
    const b = [...p.querySelectorAll('[role="button"],button')]
      .find(x => [...x.querySelectorAll('svg title')].some(t => t.textContent.trim() === '回覆'));
    if (b) return b;
  }
  return null;
})()""" % JS_REPLY_BOX

JS_DIALOG = r"""[...document.querySelectorAll('div[role="dialog"]')].reverse()
  .find(d => d.querySelector('[contenteditable="true"]'))"""


def _with_page(account_id: int):
    return Browser(account_id).page()


def check_login(account_id: int) -> dict:
    page = _with_page(account_id)
    try:
        page.navigate(HOME, settle=3)
        return page.eval(JS_LOGIN_STATE) or {"logged": False, "username": ""}
    finally:
        page.close()


def search(account_id: int, keyword: str, recent: bool = True, limit: int = 20) -> list[dict]:
    page = _with_page(account_id)
    try:
        url = "https://www.threads.com/search?" + urllib.parse.urlencode({"q": keyword, "serp_type": "default"})
        page.navigate(url, settle=2)
        state = page.eval(JS_LOGIN_STATE)
        if not state.get("logged"):
            raise CDPError("此帳號尚未登入 Threads，請到「帳號」頁按「開啟瀏覽器登入」")
        page.wait_for('document.querySelector(\'div[data-pressable-container="true"]\')', timeout=15)
        if recent:
            if page.click('document.querySelector(\'a[aria-label="最近"]\')'):
                time.sleep(3.5)
        posts: list[dict] = []
        stale = 0
        for _ in range(12):
            got = page.eval(JS_EXTRACT_POSTS) or []
            before = len(posts)
            known = {p["url"] for p in posts}
            posts.extend(p for p in got if p["url"] not in known)
            if len(posts) >= limit:
                break
            stale = stale + 1 if len(posts) == before else 0
            if stale >= 2:
                break
            page.eval("window.scrollBy(0, window.innerHeight * 1.6)")
            time.sleep(random.uniform(2.0, 3.5))
        return posts[:limit]
    finally:
        page.close()


def _noop(_msg: str):
    pass


def _fill_dialog_and_submit(page, text: str, images: list[str] | None, progress=_noop):
    """在發文／回覆的展開視窗裡：輸入文字 → 附加圖片 → 按「發佈」→ 等視窗關閉。"""
    if not page.wait_for(JS_DIALOG, timeout=10):
        raise CDPError("撰寫視窗沒有開啟")
    time.sleep(random.uniform(0.6, 1.2))
    page.click(f"({JS_DIALOG}).querySelector('[contenteditable=\"true\"]')")
    time.sleep(0.4)
    progress(f"輸入內容（{len(text)} 字）")
    page.type_text(text)
    images = [p for p in (images or []) if os.path.exists(p)]
    if images:
        progress(f"上傳 {len(images)} 個附件")
        page.set_files(f"({JS_DIALOG}).querySelector('input[type=file]')", images)
        time.sleep(3 + 2 * len(images))
    time.sleep(random.uniform(1, 2))
    submit = f"""[...({JS_DIALOG}).querySelectorAll('[role="button"],button')].find(b => b.innerText.trim() === '發佈')"""
    if not page.click(submit):
        raise CDPError("找不到「發佈」按鈕")
    progress("已按下發佈，等待 Threads 完成")
    if not page.wait_for(f"!({JS_DIALOG})", timeout=120):
        raise CDPError("送出後視窗沒有關閉，請到瀏覽器確認")
    time.sleep(3)


JS_REPLY_EXPAND = r"""(() => {
  const ed = %s;
  let q = ed;
  for (let i = 0; i < 8 && q; i++) {
    q = q.parentElement;
    const b = q && q.querySelector('[aria-label="展開撰寫工具"]');
    if (b) return b;
  }
  return null;
})()""" % JS_REPLY_BOX


def reply(account_id: int, post_url: str, text: str, images: list[str] | None = None, progress=_noop):
    images = [p for p in (images or []) if os.path.exists(p)]
    page = _with_page(account_id)
    try:
        progress("開啟原貼文")
        page.navigate(post_url, settle=2.5)
        if not page.wait_for(JS_REPLY_BOX, timeout=15):
            raise CDPError("找不到回覆框（貼文可能已刪除、限制回覆，或帳號未登入）")
        progress("閱讀貼文中")
        time.sleep(random.uniform(1.5, 4))  # 模擬閱讀
        if images:
            # 有圖片：用「展開撰寫工具」開完整回覆視窗（快速回覆列不能附圖）
            if not page.click(JS_REPLY_EXPAND):
                raise CDPError("找不到展開回覆的按鈕")
            _fill_dialog_and_submit(page, text, images, progress)
            return
        if not page.click(JS_REPLY_BOX):
            raise CDPError("無法點擊回覆框")
        time.sleep(random.uniform(0.4, 0.9))
        progress(f"輸入留言（{len(text)} 字）")
        page.type_text(text)
        time.sleep(random.uniform(0.8, 1.6))
        typed = page.eval(f"(({JS_REPLY_BOX}) || {{innerText:''}}).innerText.trim().length")
        if not typed:
            raise CDPError("文字沒有輸入成功（回覆框不見或被清空，可能頁面重新整理了），可到留言紀錄重送")
        if not page.click(JS_REPLY_SUBMIT):
            raise CDPError("找不到回覆送出鈕")
        progress("已送出，確認結果")
        ok = page.wait_for(f"(({JS_REPLY_BOX}) || {{innerText:''}}).innerText.trim().length === 0", timeout=20)
        if not ok:
            raise CDPError("送出後沒有清空，可能送出失敗或被限制")
        time.sleep(1.5)
    finally:
        page.close()


def _norm(s: str) -> str:
    return re.sub(r"\s+", "", s or "")


def _scan_profile(page, username: str, texts: list[str], max_scroll: int = 6,
                  newest_within_min: int | None = None) -> dict[int, str]:
    """到自己的個人檔案頁，用內文比對找出貼文網址。回傳 {texts 的索引: url}。
    newest_within_min：若比對不到，改用幾分鐘內發的最新一篇（剛發文時用）。"""
    page.navigate(f"https://www.threads.com/@{username}", settle=3)
    page.wait_for('document.querySelector(\'div[data-pressable-container="true"]\')', timeout=15)
    keys = {i: _norm(t)[:20] for i, t in enumerate(texts) if _norm(t)}
    found: dict[int, str] = {}
    mine: list[dict] = []
    for _ in range(max_scroll):
        for p in page.eval(JS_EXTRACT_POSTS) or []:
            if p["author"].lower() != username.lower() or p["url"] in {m["url"] for m in mine}:
                continue
            mine.append(p)
            body = _norm(p["text"])
            for i, k in keys.items():
                if i not in found and k and k in body and p["url"] not in found.values():
                    found[i] = p["url"]
        if len(found) == len(keys):
            break
        page.eval("window.scrollBy(0, window.innerHeight * 1.6)")
        time.sleep(random.uniform(1.5, 2.5))
    if newest_within_min and keys and 0 not in found:
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=newest_within_min)
        recent = []
        for p in mine:
            try:
                t = datetime.fromisoformat(p["time"].replace("Z", "+00:00"))
            except ValueError:
                continue
            if t >= cutoff:
                recent.append((t, p["url"]))
        if recent:
            found[0] = max(recent)[1]
    return found


def find_post_urls(account_id: int, username: str, texts: list[str]) -> dict[int, str]:
    """替已發佈但沒有網址的貼文補上連結。"""
    page = _with_page(account_id)
    try:
        if not username:
            page.navigate(HOME, settle=3)
            username = (page.eval(JS_LOGIN_STATE) or {}).get("username", "")
        if not username:
            raise CDPError("抓不到此帳號的使用者名稱，請先到「帳號」頁按「檢查登入」")
        return _scan_profile(page, username, texts, max_scroll=12)
    finally:
        page.close()


def publish(account_id: int, text: str, images: list[str] | None = None, progress=_noop) -> str:
    """發文，成功後回傳貼文網址（找不到時回傳空字串，不影響發文結果）。"""
    page = _with_page(account_id)
    try:
        progress("開啟 Threads 首頁")
        page.navigate(HOME, settle=3)
        state = page.eval(JS_LOGIN_STATE)
        if not state.get("logged"):
            raise CDPError("此帳號尚未登入 Threads")
        # 視窗較窄時側欄「新串文」會隱藏（寬高 0），改點動態頂端的「有什麼新鮮事？」→ 只挑看得到的
        opener = r"""[...document.querySelectorAll('[role="button"],a')]
          .filter(b => ['新串文', '有什麼新鮮事？'].includes(b.innerText.trim()))
          .find(b => { const r = b.getBoundingClientRect(); return r.width > 0 && r.height > 0; })"""
        if not page.wait_for(opener, timeout=20) or not page.click(opener):
            raise CDPError("找不到「新串文」按鈕（頁面可能還沒載入完成）")
        progress("開啟撰寫視窗")
        _fill_dialog_and_submit(page, text, images, progress)
        username = state.get("username", "")
        if not username:
            return ""
        progress("發佈成功，到個人頁抓貼文連結")
        for attempt in range(2):  # 剛發的貼文有時要等一下才出現在個人頁
            try:
                url = _scan_profile(page, username, [text], max_scroll=2, newest_within_min=10).get(0, "")
            except Exception:
                url = ""
            if url:
                return url
            time.sleep(5)
        return ""
    finally:
        page.close()
