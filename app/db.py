"""SQLite 存取：每次呼叫開新連線，避免跨執行緒問題。"""
import os
import sqlite3
import sys
import threading
from datetime import datetime

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
PROFILE_DIR = os.path.join(DATA_DIR, "profiles")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
DB_PATH = os.path.join(DATA_DIR, "threads.db")
for d in (DATA_DIR, PROFILE_DIR, UPLOAD_DIR):
    os.makedirs(d, exist_ok=True)

_write_lock = threading.Lock()

SCHEMA = """
CREATE TABLE IF NOT EXISTS accounts(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  username TEXT DEFAULT '',
  logged_in INTEGER DEFAULT 0,
  checked_at TEXT DEFAULT '',
  created_at TEXT
);
CREATE TABLE IF NOT EXISTS posts(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER,
  text TEXT,
  images TEXT DEFAULT '[]',
  scheduled_at TEXT,
  status TEXT DEFAULT 'scheduled',
  error TEXT DEFAULT '',
  posted_at TEXT DEFAULT '',
  source TEXT DEFAULT 'manual',
  created_at TEXT
);
CREATE TABLE IF NOT EXISTS autopost(
  account_id INTEGER PRIMARY KEY,
  enabled INTEGER DEFAULT 0,
  topics TEXT DEFAULT '',
  persona TEXT DEFAULT '',
  per_day INTEGER DEFAULT 3,
  start_hour INTEGER DEFAULT 9,
  end_hour INTEGER DEFAULT 23,
  length TEXT DEFAULT '中',
  review INTEGER DEFAULT 0,
  images TEXT DEFAULT '[]',
  next_at TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS tasks(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  account_id INTEGER,
  name TEXT,
  keywords TEXT,
  recent INTEGER DEFAULT 1,
  persona TEXT DEFAULT '',
  mode TEXT DEFAULT 'auto',
  interval_min INTEGER DEFAULT 60,
  max_per_run INTEGER DEFAULT 5,
  min_likes INTEGER DEFAULT 0,
  images TEXT DEFAULT '[]',
  enabled INTEGER DEFAULT 1,
  last_run TEXT DEFAULT '',
  created_at TEXT
);
CREATE TABLE IF NOT EXISTS seen(
  account_id INTEGER,
  post_url TEXT,
  PRIMARY KEY(account_id, post_url)
);
CREATE TABLE IF NOT EXISTS comments(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  task_id INTEGER,
  account_id INTEGER,
  keyword TEXT,
  post_url TEXT,
  author TEXT,
  post_text TEXT,
  likes INTEGER DEFAULT 0,
  draft TEXT,
  images TEXT DEFAULT '[]',
  status TEXT,
  error TEXT DEFAULT '',
  created_at TEXT,
  sent_at TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS logs(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT,
  level TEXT,
  msg TEXT
);
CREATE TABLE IF NOT EXISTS settings(
  key TEXT PRIMARY KEY,
  value TEXT
);
"""

DEFAULT_SETTINGS = {
    "ai_provider": "claude_cli",
    "ai_tested": "0",
    "api_key": "",
    "model": "claude-opus-5-5",
    "openai_key": "",
    "openai_model": "",
    "cli_model": "",
    "codex_model": "",
    "hourly_comment_limit": "6",
    "worker_running": "1",
    "brand_persona": "",
}


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _conn():
    c = sqlite3.connect(DB_PATH, timeout=15)
    c.row_factory = sqlite3.Row
    return c


def init():
    with _write_lock, _conn() as c:
        c.executescript(SCHEMA)
        for k, v in DEFAULT_SETTINGS.items():
            c.execute("INSERT OR IGNORE INTO settings(key,value) VALUES(?,?)", (k, v))
        # 舊資料庫升級
        if "review" not in [r[1] for r in c.execute("PRAGMA table_info(autopost)")]:
            c.execute("ALTER TABLE autopost ADD COLUMN review INTEGER DEFAULT 0")
        if "length" not in [r[1] for r in c.execute("PRAGMA table_info(tasks)")]:
            c.execute("ALTER TABLE tasks ADD COLUMN length TEXT DEFAULT '中'")
        if "url" not in [r[1] for r in c.execute("PRAGMA table_info(posts)")]:
            c.execute("ALTER TABLE posts ADD COLUMN url TEXT DEFAULT ''")
        for table in ("autopost", "tasks", "comments"):
            if "images" not in [r[1] for r in c.execute(f"PRAGMA table_info({table})")]:
                c.execute(f"ALTER TABLE {table} ADD COLUMN images TEXT DEFAULT '[]'")
        if not c.execute("SELECT 1 FROM settings WHERE key='mig_task_mode'").fetchone():
            c.execute("UPDATE tasks SET mode='auto'")  # 之前建立的任務都是自動送出
            c.execute("INSERT INTO settings(key,value) VALUES('mig_task_mode','1')")
        # 程式中斷時卡在「處理中」的項目恢復
        c.execute("UPDATE posts SET status='scheduled' WHERE status='sending'")
        c.execute("UPDATE comments SET status='approved' WHERE status='sending'")


def all(sql, args=()):
    with _conn() as c:
        return [dict(r) for r in c.execute(sql, args).fetchall()]


def one(sql, args=()):
    with _conn() as c:
        r = c.execute(sql, args).fetchone()
        return dict(r) if r else None


def run(sql, args=()) -> int:
    with _write_lock, _conn() as c:
        cur = c.execute(sql, args)
        return cur.lastrowid


def get_setting(key: str) -> str:
    r = one("SELECT value FROM settings WHERE key=?", (key,))
    return r["value"] if r else DEFAULT_SETTINGS.get(key, "")


def get_int(key: str) -> int:
    try:
        return int(get_setting(key))
    except ValueError:
        return int(DEFAULT_SETTINGS.get(key, "0") or 0)


def set_setting(key: str, value: str):
    run("INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, str(value)))


def log(msg: str, level: str = "info"):
    run("INSERT INTO logs(ts,level,msg) VALUES(?,?,?)", (now(), level, msg))
    print(f"[{level}] {msg}", flush=True)
