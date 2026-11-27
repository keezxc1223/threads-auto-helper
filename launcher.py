"""一鍵啟動：檢查套件（缺才安裝），然後以無主控台模式開啟脆自動助手。"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REQ = os.path.join(HERE, "requirements.txt")


def missing_packages() -> bool:
    r = subprocess.run([sys.executable, "-m", "pip", "install", "--dry-run", "-q", "-r", REQ],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return "Would install" in (r.stdout + r.stderr)


def main():
    print("脆自動助手 啟動中…")
    if missing_packages():
        print("第一次執行，安裝必要套件（約 1～2 分鐘）…")
        r = subprocess.run([sys.executable, "-m", "pip", "install", "-r", REQ,
                            "--disable-pip-version-check", "--progress-bar", "on"])
        if r.returncode != 0:
            input("套件安裝失敗，請截圖這個畫面。按 Enter 關閉…")
            return
        print("套件安裝完成")
    else:
        print("套件已就緒")
    pyw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    exe = pyw if os.path.exists(pyw) else sys.executable
    flags = 0x00000008 if os.name == "nt" else 0  # DETACHED_PROCESS
    subprocess.Popen([exe, os.path.join(HERE, "main.py")], cwd=HERE, creationflags=flags)


if __name__ == "__main__":
    main()
