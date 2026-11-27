"""背景排程（全自動）：
1. 自動發文規則：AI 依主題寫文，每天在指定時段內隨機時間發 N 篇
2. 到點發出排程貼文（含手動排程）
3. 海巡：搜關鍵字 → AI 寫留言 → 直接進送出佇列
4. 送出佇列：每個帳號每小時最多 N 則，間隔自動隨機分散
全部依序執行，同一時間只操作一個瀏覽器。
"""
import json
import random
import threading
import time
from datetime import datetime, timedelta

from . import ai, db, threads_bot

_next_comment_at: dict[int, float] = {}


def _fmt(d: datetime) -> str:
    return d.strftime("%Y-%m-%d %H:%M:%S")


def _account_name(aid: int) -> str:
    a = db.one("SELECT name FROM accounts WHERE id=?", (aid,))
    return a["name"] if a else f"#{aid}"


def next_comment_time() -> str:
    """佇列中下一則留言預計送出的時間（HH:MM），沒有待送就回傳空字串。"""
    rows = db.all("SELECT DISTINCT account_id FROM comments WHERE status='approved'")
    if not rows:
        return ""
    t = min(_next_comment_at.get(r["account_id"], 0) for r in rows)
    return "馬上" if t <= time.time() else datetime.fromtimestamp(t).strftime("%H:%M")


def hourly_limit() -> int:
    return max(1, db.get_int("hourly_comment_limit"))


def sent_last_hour(aid: int) -> int:
    since = _fmt(datetime.now() - timedelta(hours=1))
    return db.one("SELECT COUNT(*) n FROM comments WHERE account_id=? AND status='sent' AND sent_at>=?",
                  (aid, since))["n"]


# ---------- 自動發文 ----------
def _auto_posts_today(aid: int) -> int:
    return db.one("""SELECT COUNT(*) n FROM posts WHERE account_id=? AND source='auto'
                     AND (posted_at LIKE ? OR (status IN ('pending','scheduled','sending') AND created_at LIKE ?))""",
                  (aid, db.today() + "%", db.today() + "%"))["n"]


def _window(rule: dict, day: datetime):
    start = day.replace(hour=int(rule["start_hour"]), minute=0, second=0, microsecond=0)
    end_h = int(rule["end_hour"])
    end = day.replace(hour=23, minute=59, second=0, microsecond=0) if end_h >= 24 else \
        day.replace(hour=end_h, minute=0, second=0, microsecond=0)
    return start, end


def plan_next(rule: dict) -> str:
    """依今天剩餘篇數，把下一篇排在剩餘時段內的隨機位置。"""
    now = datetime.now()
    start, end = _window(rule, now)
    remaining = int(rule["per_day"]) - _auto_posts_today(rule["account_id"])
    if remaining <= 0 or now >= end:
        tomorrow = now + timedelta(days=1)
        s, e = _window(rule, tomorrow)
        span = max(60, (e - s).total_seconds() / max(1, int(rule["per_day"])))
        return _fmt(s + timedelta(seconds=random.uniform(0, span)))
    base = max(now, start)
    # 間隔至少是「完整時段平均間隔」的一半，避免很晚才開啟時把當天篇數擠在一起
    full_gap = (end - start).total_seconds() / max(1, int(rule["per_day"]))
    slot = max((end - base).total_seconds() / remaining, full_gap * 0.5)
    last = db.one("SELECT MAX(posted_at) t FROM posts WHERE account_id=? AND source='auto' AND status='sent'",
                  (rule["account_id"],))
    if last and last["t"]:
        base = max(base, datetime.strptime(last["t"], "%Y-%m-%d %H:%M:%S") + timedelta(seconds=full_gap * 0.5))
    nxt = base + timedelta(seconds=random.uniform(0.15, 0.85) * slot)
    if nxt > end:  # 今天塞不下了 → 明天
        s, e = _window(rule, now + timedelta(days=1))
        return _fmt(s + timedelta(seconds=random.uniform(0, full_gap)))
    return _fmt(nxt)


def do_autopost() -> bool:
    now = datetime.now()
    for rule in db.all("SELECT * FROM autopost WHERE enabled=1"):
        aid = rule["account_id"]
        if not rule["next_at"]:
            db.run("UPDATE autopost SET next_at=? WHERE account_id=?", (plan_next(rule), aid))
            continue
        if datetime.strptime(rule["next_at"], "%Y-%m-%d %H:%M:%S") > now:
            continue
        start, end = _window(rule, now)
        if not (start <= now <= end) or _auto_posts_today(aid) >= int(rule["per_day"]):
            db.run("UPDATE autopost SET next_at=? WHERE account_id=?", (plan_next(rule), aid))
            continue
        topics = [t.strip() for t in rule["topics"].splitlines() if t.strip()]
        if not topics:
            continue
        topic = random.choice(topics)
        recent = [r["text"] for r in db.all(
            "SELECT text FROM posts WHERE account_id=? ORDER BY id DESC LIMIT 6", (aid,))]
        name = _account_name(aid)
        try:
            items = ai.write_posts(topic, rule["persona"], 1, rule["length"] or "中", recent)
        except Exception as e:
            db.log(f"[{name}] AI 自動寫文失敗：{e}", "error")
            db.run("UPDATE autopost SET next_at=? WHERE account_id=?",
                   (_fmt(now + timedelta(minutes=15)), aid))
            return True
        if items:
            review = int(rule.get("review") or 0)
            db.run("""INSERT INTO posts(account_id,text,images,scheduled_at,status,source,created_at)
                      VALUES(?,?,?,?,?,'auto',?)""",
                   (aid, items[0], rule.get("images") or "[]", db.now(), "pending" if review else "scheduled", db.now()))
            db.log(f"[{name}] AI 已寫好自動貼文（主題：{topic}）" + ("，等你審核" if review else ""))
        rule = db.one("SELECT * FROM autopost WHERE account_id=?", (aid,))
        db.run("UPDATE autopost SET next_at=? WHERE account_id=?", (plan_next(rule), aid))
        return True
    return False


def do_due_post() -> bool:
    p = db.one("SELECT * FROM posts WHERE status='scheduled' AND scheduled_at<=? ORDER BY scheduled_at LIMIT 1",
               (db.now(),))
    if not p:
        return False
    aid = p["account_id"]
    db.run("UPDATE posts SET status='sending' WHERE id=?", (p["id"],))
    db.log(f"[{_account_name(aid)}] 開始發文 #{p['id']}")
    try:
        url = threads_bot.publish(aid, p["text"], json.loads(p["images"] or "[]")) or ""
        db.run("UPDATE posts SET status='sent', posted_at=?, error='', url=? WHERE id=?", (db.now(), url, p["id"]))
        db.log(f"[{_account_name(aid)}] 發文成功 #{p['id']}", "ok")
    except Exception as e:
        db.run("UPDATE posts SET status='failed', error=? WHERE id=?", (str(e), p["id"]))
        db.log(f"[{_account_name(aid)}] 發文失敗 #{p['id']}：{e}", "error")
    return True


# ---------- 留言 ----------
def do_queued_comment() -> bool:
    rows = db.all("SELECT * FROM comments WHERE status='approved' ORDER BY id")
    t = time.time()
    limit = hourly_limit()
    for c in rows:
        aid = c["account_id"]
        if aid not in _next_comment_at:  # 程式重開後，從上一則送出時間接續間隔
            last = db.one("SELECT MAX(sent_at) t FROM comments WHERE account_id=? AND status='sent'", (aid,))
            _next_comment_at[aid] = (datetime.strptime(last["t"], "%Y-%m-%d %H:%M:%S").timestamp() + 3600 / limit
                                     if last and last["t"] else 0)
        if _next_comment_at.get(aid, 0) > t or sent_last_hour(aid) >= limit:
            continue
        db.run("UPDATE comments SET status='sending' WHERE id=?", (c["id"],))
        try:
            threads_bot.reply(aid, c["post_url"], c["draft"], json.loads(c.get("images") or "[]"))
            db.run("UPDATE comments SET status='sent', sent_at=?, error='' WHERE id=?", (db.now(), c["id"]))
            db.log(f"[{_account_name(aid)}] 已留言給 @{c['author']}：{c['draft'][:30]}", "ok")
        except Exception as e:
            db.run("UPDATE comments SET status='failed', error=? WHERE id=?", (str(e), c["id"]))
            db.log(f"[{_account_name(aid)}] 留言失敗 @{c['author']}：{e}", "error")
        # 平均間隔 = 3600 / 每小時上限，再加減 40% 隨機
        _next_comment_at[aid] = time.time() + (3600 / limit) * random.uniform(0.6, 1.4)
        return True
    return False


def recent_comments(aid: int, n: int = 40) -> list[str]:
    """此帳號最近的留言（已送、待送、送失敗），給 AI 避免重複。"""
    rows = db.all("""SELECT draft FROM comments WHERE account_id=? AND draft<>''
                     AND status IN ('sent','approved','sending','failed') ORDER BY id DESC LIMIT ?""", (aid, n))
    return [r["draft"] for r in rows]


def run_task(task: dict):
    aid = task["account_id"]
    name = _account_name(aid)
    db.run("UPDATE tasks SET last_run=? WHERE id=?", (db.now(), task["id"]))
    queued = db.one("SELECT COUNT(*) n FROM comments WHERE account_id=? AND status IN ('approved','pending')",
                    (aid,))["n"]
    room = hourly_limit() * 2 - queued
    if room <= 0:
        db.log(f"[{name}] 還有 {queued} 則留言待送或待審核，這輪海巡先跳過")
        return
    want = min(task["max_per_run"], room)
    me = (db.one("SELECT username FROM accounts WHERE id=?", (aid,)) or {}).get("username", "")
    keywords = [k.strip() for k in task["keywords"].replace("，", ",").replace("\n", ",").split(",") if k.strip()]
    random.shuffle(keywords)
    made = 0
    db.log(f"[{name}] 海巡「{task['name']}」開始")
    for kw in keywords:
        if made >= want:
            break
        try:
            posts = threads_bot.search(aid, kw, recent=bool(task["recent"]), limit=25)
        except Exception as e:
            db.log(f"[{name}] 搜尋「{kw}」失敗：{e}", "error")
            continue
        fresh = 0
        for p in posts:
            if made >= want:
                break
            if me and p["author"].lower() == me.lower():
                continue
            if db.one("SELECT 1 FROM seen WHERE account_id=? AND post_url=?", (aid, p["url"])):
                continue
            db.run("INSERT OR IGNORE INTO seen(account_id,post_url) VALUES(?,?)", (aid, p["url"]))
            fresh += 1
            if p["likes"] < task["min_likes"] or len(p["text"]) < 4:
                continue
            try:
                draft = ai.draft_comment(p["text"], p["author"], task["persona"], kw, recent_comments(aid))
            except Exception as e:
                db.log(f"[{name}] AI 產生留言失敗：{e}", "error")
                return
            db.run("""INSERT INTO comments(task_id,account_id,keyword,post_url,author,post_text,likes,draft,images,status,created_at)
                      VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                   (task["id"], aid, kw, p["url"], p["author"], p["text"], p["likes"], draft or "",
                    task.get("images") or "[]",
                    ("pending" if task.get("mode") == "review" else "approved") if draft else "skipped", db.now()))
            if draft:
                made += 1
        db.log(f"[{name}] 「{kw}」掃到 {len(posts)} 篇，新貼文 {fresh} 篇")
    where = "待審核" if task.get("mode") == "review" else "送出佇列"
    db.log(f"[{name}] 海巡「{task['name']}」完成，{made} 則留言進入{where}", "ok")


def do_due_task() -> bool:
    for t in db.all("SELECT * FROM tasks WHERE enabled=1 ORDER BY id"):
        last = t["last_run"]
        if last:
            due = datetime.strptime(last, "%Y-%m-%d %H:%M:%S") + timedelta(minutes=t["interval_min"])
            if due > datetime.now():
                continue
        run_task(t)
        return True
    return False


class Worker(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.wake = threading.Event()
        self.busy = ""

    def run(self):
        steps = [("寫文中", do_autopost), ("發文中", do_due_post),
                 ("留言中", do_queued_comment), ("海巡中", do_due_task)]
        while True:
            did = False
            try:
                if db.get_setting("worker_running") == "1":
                    for label, fn in steps:
                        self.busy = label
                        did = fn() or did
            except Exception as e:
                db.log(f"排程錯誤：{e}", "error")
            self.busy = ""
            if did:
                continue
            self.wake.wait(10)
            self.wake.clear()


worker = Worker()
