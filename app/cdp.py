"""直接用 Chrome DevTools Protocol 操作本機 Chrome（不需 Playwright / chromedriver）。

每個帳號一個獨立的 Chrome 設定檔（data/profiles/acc_<id>）與獨立除錯埠，
登入一次後 cookie 會保留在該設定檔裡。
"""
import json
import os
import random
import subprocess
import threading
import time
import urllib.request

import websocket

from . import db

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


class CDPError(Exception):
    pass


def find_chrome() -> str:
    for p in CHROME_CANDIDATES:
        if os.path.exists(p):
            return p
    raise CDPError("找不到 Chrome 或 Edge，請先安裝 Google Chrome")


def port_for(account_id: int) -> int:
    return 9300 + int(account_id)


def profile_for(account_id: int) -> str:
    return os.path.join(db.PROFILE_DIR, f"acc_{account_id}")


def _http_json(url: str, method: str = "GET", timeout: float = 3):
    req = urllib.request.Request(url, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


class Page:
    def __init__(self, ws_url: str):
        self.ws = websocket.create_connection(ws_url, timeout=60, suppress_origin=True)
        self._id = 0
        self._lock = threading.Lock()

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass

    def send(self, method: str, params: dict | None = None, timeout: float = 60):
        with self._lock:
            self._id += 1
            mid = self._id
            self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
            deadline = time.time() + timeout
            while time.time() < deadline:
                self.ws.settimeout(max(0.5, deadline - time.time()))
                try:
                    msg = json.loads(self.ws.recv())
                except websocket.WebSocketTimeoutException:
                    break
                if msg.get("id") == mid:
                    if "error" in msg:
                        raise CDPError(f"{method}: {msg['error'].get('message')}")
                    return msg.get("result", {})
            raise CDPError(f"{method} 逾時")

    def eval(self, expr: str, timeout: float = 60):
        r = self.send("Runtime.evaluate", {
            "expression": expr, "returnByValue": True, "awaitPromise": True,
            "userGesture": True,
        }, timeout=timeout)
        if "exceptionDetails" in r:
            d = r["exceptionDetails"]
            text = d.get("exception", {}).get("description") or d.get("text")
            raise CDPError(f"頁面腳本錯誤：{text}")
        return r.get("result", {}).get("value")

    def _post(self, method: str, params: dict | None = None):
        """送出指令但不等回應（Page.navigate 遇到「要離開網站嗎？」會卡住不回）。"""
        with self._lock:
            self._id += 1
            self.ws.send(json.dumps({"id": self._id, "method": method, "params": params or {}}))

    def dismiss_dialog(self) -> bool:
        """有「要離開網站嗎？」或其他對話框就直接按確定／離開。沒有對話框回傳 False。"""
        try:
            self.send("Page.handleJavaScriptDialog", {"accept": True}, timeout=5)
            return True
        except CDPError:
            return False

    def navigate(self, url: str, settle: float = 2.5):
        self.send("Page.enable")
        self.dismiss_dialog()  # 先清掉之前殘留的對話框
        try:
            self.eval("window.onbeforeunload = null; true", timeout=5)
        except CDPError:
            pass
        self._post("Page.navigate", {"url": url})
        for _ in range(8):  # 跳出「要離開網站嗎？」就按離開
            time.sleep(0.5)
            if self.dismiss_dialog():
                break
        deadline = time.time() + 40
        time.sleep(1)
        while time.time() < deadline:
            try:
                if self.eval("document.readyState") == "complete":
                    break
            except CDPError:
                pass
            time.sleep(0.5)
        time.sleep(settle)

    def wait_for(self, js_condition: str, timeout: float = 15, interval: float = 0.5):
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                if self.eval(f"!!({js_condition})"):
                    return True
            except CDPError:
                pass
            time.sleep(interval)
        return False

    def rect_of(self, js_element: str):
        """js_element: 一段回傳 Element 的 JS 運算式。捲到可見後回傳中心座標。"""
        return self.eval(f"""(() => {{
            const el = {js_element};
            if (!el) return null;
            el.scrollIntoView({{block: 'center', inline: 'center'}});
            const r = el.getBoundingClientRect();
            return {{x: r.x + r.width / 2, y: r.y + r.height / 2, w: r.width, h: r.height}};
        }})()""")

    def click_at(self, x: float, y: float):
        x += random.uniform(-2, 2)
        y += random.uniform(-2, 2)
        self.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})
        time.sleep(random.uniform(0.05, 0.15))
        self.send("Input.dispatchMouseEvent", {"type": "mousePressed", "x": x, "y": y,
                                               "button": "left", "clickCount": 1})
        time.sleep(random.uniform(0.04, 0.12))
        self.send("Input.dispatchMouseEvent", {"type": "mouseReleased", "x": x, "y": y,
                                               "button": "left", "clickCount": 1})

    def click(self, js_element: str) -> bool:
        r = self.rect_of(js_element)
        if not r or r["w"] == 0:
            return False
        time.sleep(0.3)
        r = self.rect_of(js_element) or r
        self.click_at(r["x"], r["y"])
        return True

    def press_enter(self):
        base = {"key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13,
                "nativeVirtualKeyCode": 13}
        self.send("Input.dispatchKeyEvent", {"type": "keyDown", "text": "\r", **base})
        self.send("Input.dispatchKeyEvent", {"type": "keyUp", **base})

    def type_text(self, text: str):
        """分段輸入，換行用 Enter，模擬人打字的節奏。"""
        lines = text.replace("\r\n", "\n").split("\n")
        for i, line in enumerate(lines):
            pos = 0
            while pos < len(line):
                n = random.randint(4, 12)
                self.send("Input.insertText", {"text": line[pos:pos + n]})
                pos += n
                time.sleep(random.uniform(0.05, 0.25))
            if i < len(lines) - 1:
                self.press_enter()
                time.sleep(random.uniform(0.1, 0.3))

    def set_files(self, js_input: str, files: list[str]):
        r = self.send("Runtime.evaluate", {"expression": js_input, "returnByValue": False})
        obj = r.get("result", {}).get("objectId")
        if not obj:
            raise CDPError("找不到上傳欄位")
        self.send("DOM.enable")
        self.send("DOM.setFileInputFiles", {"files": files, "objectId": obj})


class Browser:
    """一個帳號對應一個 Chrome 實例。"""

    def __init__(self, account_id: int):
        self.account_id = account_id
        self.port = port_for(account_id)
        self.profile = profile_for(account_id)

    def running(self) -> bool:
        try:
            _http_json(f"http://127.0.0.1:{self.port}/json/version", timeout=1.5)
            return True
        except Exception:
            return False

    def launch(self, url: str = "https://www.threads.com/"):
        if self.running():
            return
        args = [
            find_chrome(),
            f"--remote-debugging-port={self.port}",
            f"--user-data-dir={self.profile}",
            "--remote-allow-origins=*",
            "--no-first-run",
            "--no-default-browser-check",
            "--lang=zh-TW",
            "--window-size=1200,900",
            # 縮小或被其他視窗蓋住時也照常執行，不被 Chrome 降速
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            "--disable-backgrounding-occluded-windows",
            url,
        ]
        flags = 0x08000000 if os.name == "nt" else 0  # CREATE_NO_WINDOW（主控台視窗）
        subprocess.Popen(args, creationflags=flags)
        deadline = time.time() + 20
        while time.time() < deadline:
            if self.running():
                time.sleep(1.5)
                return
            time.sleep(0.5)
        raise CDPError("Chrome 啟動逾時")

    def page(self) -> Page:
        self.launch()
        tabs = _http_json(f"http://127.0.0.1:{self.port}/json/list")
        pages = [t for t in tabs if t.get("type") == "page" and not t.get("url", "").startswith("devtools")]
        if not pages:
            t = _http_json(f"http://127.0.0.1:{self.port}/json/new?about:blank", method="PUT")
            pages = [t]
        tab = pages[0]
        try:
            _http_json(f"http://127.0.0.1:{self.port}/json/activate/{tab['id']}")
        except Exception:
            pass
        return Page(tab["webSocketDebuggerUrl"])

    def close(self):
        if not self.running():
            return
        try:
            info = _http_json(f"http://127.0.0.1:{self.port}/json/version")
            ws = websocket.create_connection(info["webSocketDebuggerUrl"], timeout=5, suppress_origin=True)
            ws.send(json.dumps({"id": 1, "method": "Browser.close"}))
            ws.close()
        except Exception:
            pass
