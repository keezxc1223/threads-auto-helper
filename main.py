"""脆自動助手：啟動 API 伺服器、背景排程，並開啟桌面視窗。"""
import socket
import sys
import threading
import time
import webbrowser

from app import __version__, db

# pythonw / exe 沒有主控台，print 會出錯 → 導到記錄檔
if sys.stdout is None or sys.stderr is None:
    _log = open(f"{db.DATA_DIR}/app.log", "a", encoding="utf-8", buffering=1)
    sys.stdout = sys.stdout or _log
    sys.stderr = sys.stderr or _log

import uvicorn  # noqa: E402
from app.server import app
from app.worker import worker


def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def main():
    db.init()
    db.log(f"程式啟動 v{__version__}")
    worker.start()
    port = free_port()
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="warning"))
    threading.Thread(target=server.run, daemon=True).start()
    while not server.started:
        time.sleep(0.1)
    url = f"http://127.0.0.1:{port}/"
    try:
        import webview
        webview.create_window("脆自動助手", url, width=1320, height=860, min_size=(1080, 680))
        webview.start()
    except Exception as e:
        print("桌面視窗開啟失敗，改用瀏覽器：", e)
        webbrowser.open(url)
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            pass
    sys.exit(0)


if __name__ == "__main__":
    main()
