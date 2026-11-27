<a id="top"></a>

<h1 align="center">脆自動助手</h1>

<p align="center">
  <b>在 Windows 上經營 Threads（脆）的 AI 自動化工具</b><br>
  AI 寫文 · 排程發文 · 關鍵字海巡自動留言 · 多帳號 · 資料全存本機
</p>

<p align="center">
  <img alt="platform" src="https://img.shields.io/badge/Windows-10%20%7C%2011-2d3748?style=flat-square">
  <img alt="python" src="https://img.shields.io/badge/Python-3.10%2B-3776ab?style=flat-square">
  <img alt="browser" src="https://img.shields.io/badge/Chrome%20%2F%20Edge-required-4ecdc4?style=flat-square">
  <img alt="ai" src="https://img.shields.io/badge/AI-Claude%20%7C%20ChatGPT-6c8cff?style=flat-square">
  <img alt="private" src="https://img.shields.io/badge/repo-private-555?style=flat-square">
</p>

<p align="center">
  <a href="#快速開始">快速開始</a> ·
  <a href="#功能">功能</a> ·
  <a href="#頻率限制與帳號安全">帳號安全</a> ·
  <a href="#疑難排解">疑難排解</a> ·
  <a href="#開發者文件">開發者文件</a>
</p>

> [!WARNING]
> **使用前請注意**：自動化操作可能違反 Threads／Meta 的使用條款，導致觸及降低、功能受限或帳號停權，風險由使用者自行承擔。請先用小號、低頻率測試。完整條款見[免責聲明](#disclaimer免責聲明)。

## 特色

- **AI 自動發文**：設定主題與風格，AI 每天在指定時段內隨機挑時間發 N 篇，可選全自動或審核後才發。
- **手動排程**：自己寫或請 AI 一次產生 1～5 篇讓你挑，可附圖片或影片（最多 10 個），立即發或指定時間發。
- **關鍵字海巡**：搜尋最新或最相關的貼文，依讚數門檻篩選；AI 先判斷適不適合留言，適合才寫。
- **送出佇列**：每個帳號每小時最多 N 則留言，間隔自動隨機分散，模擬真人節奏。
- **完整紀錄**：發文紀錄附 Threads 貼文連結，留言紀錄可審核、修改、AI 重寫、重試；刪除前都會二次確認。
- **多帳號**：每個帳號一個獨立的 Chrome 設定檔，登入一次就會記住，cookie 互不干擾。
- **四種 AI 來源**：Claude 或 ChatGPT 訂閱登入（不另外計費），或 Claude／OpenAI API Key。
- **防重複**：AI 寫的內容會和近期內容比相似度，太像就重寫；海巡看過的貼文不會再看。
- **資料全在本機**：帳號、貼文、留言、金鑰都存在 `data/`，不經過任何第三方伺服器（只有 AI 寫文時會把提示詞送到你選的 AI 服務）。

---

## 快速開始

1. 安裝 [Python 3.10 以上](https://www.python.org/downloads/)（安裝時勾選「Add Python to PATH」）與 Google Chrome。
2. 雙擊 **`啟動.bat`**。第一次會自動安裝套件（約 1～2 分鐘），之後直接開啟桌面視窗。
3. 到「**設定**」選一種 AI 服務，完成登入或填入金鑰，按「測試」確認可用。
4. 到「**帳號**」新增帳號 → 按「開啟瀏覽器登入」→ 在跳出的專屬瀏覽器登入 Threads → 按「檢查登入」。
5. 到「**自動發文**」或「**自動海巡**」建立規則，確認左下角顯示「**自動執行中**」即可。

每個步驟的細節見[安裝與前置設定](#安裝與前置設定)。

---

## 系統需求

| 項目 | 需求 |
| --- | --- |
| 作業系統 | Windows 10 / 11（主要支援平台） |
| Python | 3.10 以上（開發環境為 3.13） |
| 瀏覽器 | Google Chrome 或 Microsoft Edge（程式會自動尋找） |
| AI 服務 | 四選一，見[AI 服務設定](#2-設定-ai-服務) |
| Threads 介面語言 | **繁體中文**（網頁操作以中文按鈕文字比對，見[開發者文件](#開發者文件)） |

---

## 功能

點擊各項目展開詳細說明。

<details>
<summary><b>總覽</b></summary>

- 今日發文數、今日留言數、排程數、待審核數。
- 新手引導清單：AI 設定、新增帳號、建立規則，完成的項目會打勾。
- **執行紀錄**：即時顯示背景工作的每一步與錯誤（保留最近 300 筆）。
- 左下角開關可以隨時暫停或啟動全部自動工作。

</details>

<details>
<summary><b>帳號</b></summary>

- 新增、改名、刪除帳號（刪除前會確認；海巡任務、自動發文規則與未發出的排程會一併刪除，瀏覽器登入資料保留）。
- 「開啟瀏覽器登入」會用該帳號專屬的 Chrome 設定檔（`data/profiles/acc_<id>`）開啟 Threads，登入一次就會記住。
- 「檢查登入」會確認登入狀態，並抓取 `@使用者名稱`（發文紀錄的貼文連結需要它）。

</details>

<details>
<summary><b>自動發文</b></summary>

每個帳號一組規則：

| 設定 | 說明 |
| --- | --- |
| 主題 | 可以填多個，AI 每次挑一個寫 |
| 風格 | 例如「幽默、像朋友聊天」 |
| 每天篇數 | 超過 5 篇會出現提醒，超過 15 篇會強烈警告 |
| 發文時段 | 開始與結束小時，在時段內隨機挑時間 |
| 篇幅 | 短、中、長 |
| 發文方式 | **自動發出**，或**審核後才發**（放到「發文紀錄 → 待審核」） |
| 固定附圖 | 選填，每篇都會附上 |

</details>

<details>
<summary><b>手動排程</b></summary>

- 左邊撰寫，字數上限 500（符合 Threads 限制），即時顯示字數。
- 「**AI 幫我寫**」：輸入主題、風格、篇數（1～5）、篇幅，挑一篇帶入。
- 附件：圖片或影片（mp4 / mov / webm），最多 10 個。
- 發文時間：立即，或指定日期時間。
- 右邊列出待審核、排程中、已發佈、失敗的貼文，可立即發、編輯、刪除。

</details>

<details>
<summary><b>發文紀錄</b></summary>

集中顯示自動發文與手動排程的所有貼文，預設開在「已發佈」。

- **分頁**：已發佈、排程中、待審核、失敗，各自顯示數量。
- **來源篩選**：全部、AI 自動發文、手動排程。
- **貼文連結**：發佈成功後，程式會到該帳號的個人檔案頁，用內文比對找到剛發的貼文並存下網址。點「在 Threads 查看」直接開啟。
- **補上連結**：較早發的、沒有連結的貼文，可以在「已發佈」按「補上連結」批次補齊。
- **刪除確認**：刪除前會顯示貼文開頭讓你確認。已發佈的貼文只會刪除本機紀錄，**不會**刪除 Threads 上的貼文。

> 連結比對以內文開頭約 20 個字為準。已刪除或太舊捲不到的貼文會找不到；開頭完全相同的多篇貼文可能會對錯。

</details>

<details>
<summary><b>自動海巡</b></summary>

每個任務包含：

| 設定 | 說明 |
| --- | --- |
| 關鍵字 | 可多個，依序搜尋 |
| 搜尋排序 | 「最近」或「最相關」 |
| 留言風格 | AI 寫留言時的語氣 |
| 最低讚數 | 低於門檻的貼文略過 |
| 執行間隔 | 幾分鐘跑一次 |
| 每次最多 | 每次執行最多留幾則 |
| 留言方式 | **自動送出**，或**審核後才送出**（放到「留言紀錄 → 待審核」） |
| 附圖 | 選填，會改用完整回覆視窗附上 |

AI 會先判斷貼文適不適合留言（例如不相關、敏感或純廣告），不適合就標為「略過」。任務卡片上可以「立即執行」、編輯或刪除（刪除前會確認，已產生的留言紀錄會保留）。

</details>

<details>
<summary><b>留言紀錄</b></summary>

預設開在「已送出」。

| 分頁 | 可以做的事 |
| --- | --- |
| 待審核 | 修改、AI 重寫、拒絕、核准，或「全部核准」 |
| 待送出 | 顯示下一則預計送出時間；送出前可修改、AI 重寫、取消 |
| 已送出 | 查看留言內容、原貼文與送出時間 |
| 失敗 | 查看錯誤原因，修改後重試 |
| 略過／取消 | AI 判斷不適合的可以選「還是要留言」；取消的可以恢復送出 |

</details>

<details>
<summary><b>設定</b></summary>

- **AI 服務與模型**：四種來源切換，模型清單自動偵測。
- **每小時留言上限**：每個帳號分開計算，預設 6 則。
- **品牌定位**：帳號的定位、語氣與禁忌，AI 寫文與留言都會參考。

</details>

---

## 安裝與前置設定

### 1. 安裝與啟動

**一鍵啟動（建議）**：雙擊 `啟動.bat`。啟動器會檢查套件，缺了才安裝，然後用 `pythonw` 在背景執行，不會留下黑色主控台視窗。

**手動啟動**：

```bash
pip install -r requirements.txt
python main.py
```

程式會在 `127.0.0.1` 上挑一個空的連接埠啟動，並用 pywebview 開啟桌面視窗；pywebview 開不起來時會改用預設瀏覽器。

### 2. 設定 AI 服務

| 選項 | 計費方式 | 需要 |
| --- | --- | --- |
| **Claude 訂閱登入**（預設） | 用 Claude Pro 或 Max 訂閱額度，不另外計費 | 本機安裝 [Claude Code](https://claude.com/claude-code) CLI |
| **ChatGPT 訂閱登入** | 用 ChatGPT Plus 或 Pro 訂閱額度，不另外計費 | 本機安裝 Codex CLI |
| **Claude API Key** | 依用量計費 | [Anthropic API 金鑰](https://console.anthropic.com/) |
| **OpenAI API Key** | 依用量計費 | [OpenAI API 金鑰](https://platform.openai.com/) |

- **訂閱登入**：在設定頁按「登入 Claude」或「登入 ChatGPT」，會開一個視窗，照指示在瀏覽器完成登入（ChatGPT 請選「Sign in with ChatGPT」）。
- **API Key**：貼上金鑰後按「測試」。金鑰只存在本機的 `data/threads.db`。
- AI 回覆格式不對時會自動重試。

### 3. 登入 Threads 帳號

1. 「帳號」→「新增帳號」，取一個好認的名字。
2. 按「**開啟瀏覽器登入**」，會開一個該帳號專屬的 Chrome 視窗。
3. 在**那個視窗**裡登入 Threads（可以用 Instagram 帳號）。
4. 回到助手按「**檢查登入**」，顯示「已登入 @使用者名稱」就完成了。

> [!NOTE]
> 每個帳號的登入狀態都存在自己的瀏覽器設定檔，跟你平常用的 Chrome 完全分開。之後就算關掉瀏覽器，下次也不用再登入。

### 4. 建立自動規則並啟動

- 想定期發文 →「自動發文」
- 想自動找貼文留言 →「自動海巡」
- 第一次建議選「**審核後才發**／**審核後才送出**」，確認 AI 寫的內容符合預期後再改成全自動。

---

## 頻率限制與帳號安全

Threads 會偵測機器人行為。程式內建以下保護：

| 項目 | 建議值 | 超過時 |
| --- | --- | --- |
| 每天發文 | ≤ 5 篇 | 超過 15 篇會出現強烈警告 |
| 每小時留言 | ≤ 6 則 | 超過 15 則會出現強烈警告 |

- **隨機化**：發文時間在時段內隨機挑；留言間隔約為 `60 ÷ 每小時上限` 分鐘，再加上隨機變動。
- **模擬真人**：用真實滑鼠事件點擊、逐字輸入，送出前有「閱讀」停頓。
- **一次只做一件事**：背景工作依序執行，同一時間只操作一個瀏覽器。
- **建議**：新帳號先用低頻率跑幾天；內容盡量多元，避免同樣的留言反覆出現。

---

## 疑難排解

| 症狀 | 可能原因與解法 |
| --- | --- |
| 雙擊 `啟動.bat` 一閃就關 | 沒有安裝 Python，或安裝時沒勾「Add Python to PATH」。重新安裝 Python 並勾選 |
| 「找不到 Chrome 或 Edge」 | 安裝 Google Chrome |
| 帳號一直顯示未登入 | 要在「開啟瀏覽器登入」跳出的**那個視窗**登入，不是平常的 Chrome；登入後再按「檢查登入」 |
| 「找不到『新串文』按鈕」 | 頁面還沒載入完，或 Threads 改版。查看 `data/app.log`，並確認 `app/threads_bot.py` 的選擇器 |
| 「送出後視窗沒有關閉」 | 網路慢或附件太大，到該帳號的瀏覽器確認是否已發出 |
| 發文成功但沒有連結 | 到「發文紀錄 → 已發佈」按「補上連結」；提示抓不到使用者名稱時，先到「帳號」按「檢查登入」 |
| AI 測試失敗 | 訂閱登入：確認 CLI 已安裝並登入；API：確認金鑰正確且有額度 |
| 留言一直「失敗」 | 貼文可能已刪除或限制回覆，或帳號被限制。先降低每小時上限、暫停一段時間 |
| AI 一直判斷「不適合留言」 | 關鍵字太廣或風格描述太嚴格。調整關鍵字或留言風格 |
| 視窗沒出現 | 查看 `data/app.log`；也可以用 `python main.py` 在主控台執行看錯誤訊息 |

回報問題時請附上錯誤畫面與 `data/app.log` 的相關段落（**不要**附上 `data/` 裡的其他檔案）。

---

## 資料與隱私

| 位置 | 內容 | 注意 |
| --- | --- | --- |
| `data/threads.db` | 帳號、貼文、留言、規則、設定（**含 API 金鑰**） | 不要分享 |
| `data/profiles/` | 各帳號瀏覽器設定檔（**含 Threads 登入 cookie**） | 外流等於帳號外洩 |
| `data/uploads/` | 上傳的圖片與影片 | 無 |
| `data/app.log` | 執行記錄 | 回報問題時可附上相關段落 |

- `data/` 已列在 `.gitignore`，**絕對不要上傳到 GitHub 或分享給別人**。
- **搬到新電腦**：把整個資料夾（含 `data/`）複製過去即可。
- **重設**：關掉程式後刪除 `data/`，所有帳號都要重新登入。

---

## 開發者文件

<details>
<summary>展開開發者文件（架構、運作流程、資料庫、API、專案結構）</summary>

### 架構

```
┌──────────────────┐   HTTP (127.0.0.1)   ┌──────────────────┐   SQLite   ┌────────────┐
│ 原生 JS 單頁介面  │ ───────────────────► │ FastAPI          │ ─────────► │ threads.db │
│ pywebview 視窗   │ ◄─────────────────── │ app/server.py    │ ◄───────── │            │
└──────────────────┘                      └──────────────────┘            └─────▲──────┘
                                                                                │
                                          ┌──────────────────┐                  │
                                          │ 背景排程執行緒    │ ─────────────────┘
                                          │ app/worker.py    │
                                          └───┬──────────┬───┘
                                  AI 寫文／留言 │          │ 瀏覽器操作
                                       ┌──────▼───┐ ┌────▼────────────┐  CDP (WebSocket)  ┌───────────────────┐
                                       │ app/ai.py│ │ threads_bot.py  │ ────────────────► │ Chrome            │
                                       └──────────┘ │ cdp.py          │                   │ 每帳號獨立設定檔   │
                                                    └─────────────────┘                   └───────────────────┘
```

### 技術組成

| 層 | 技術 | 用途 |
| --- | --- | --- |
| 介面 | 原生 HTML / CSS / JS | 單頁介面，無框架、無建置步驟；圖示全為 inline SVG |
| 桌面外殼 | [pywebview](https://pywebview.flowrl.com/) | 桌面視窗，失敗時改用瀏覽器 |
| 後端 | Python + [FastAPI](https://fastapi.tiangolo.com/) + [uvicorn](https://www.uvicorn.org/) | REST API 與靜態檔 |
| 資料庫 | SQLite | 每次呼叫開新連線，寫入加鎖，避免跨執行緒問題 |
| 瀏覽器 | Chrome DevTools Protocol + [websocket-client](https://github.com/websocket-client/websocket-client) | 不用 Selenium / Playwright，直接以 `--remote-debugging-port` 操作 |
| AI | [anthropic](https://github.com/anthropics/anthropic-sdk-python)、[openai](https://github.com/openai/openai-python)、Claude Code CLI、Codex CLI | 寫文、寫留言、判斷適不適合留言 |

### 核心模組（`app/`）

| 模組 | 職責 |
| --- | --- |
| `db.py` | SQLite 結構、啟動時自動升級欄位、設定存取、記錄 |
| `server.py` | 所有 REST API 與靜態檔服務 |
| `worker.py` | 背景排程：自動發文、到點發文、海巡、留言佇列 |
| `threads_bot.py` | Threads 網頁操作：登入檢查、搜尋、發文、回覆、個人頁比對貼文網址 |
| `cdp.py` | 尋找與啟動 Chrome、DevTools Protocol 封裝（導覽、執行 JS、滑鼠鍵盤事件、上傳檔案） |
| `ai.py` | 四種 AI 來源整合、提示詞、模型清單偵測、相似度檢查 |

### 背景排程流程（`worker.py`）

常駐執行緒依序處理，一次只操作一個瀏覽器：

1. **自動發文規則**：到了 `next_at` 就請 AI 寫一篇，排進 `posts`（審核模式設為 `pending`），再隨機挑下一次時間。
2. **到點貼文**：發出 `scheduled_at` 已到的貼文 → 到個人頁比對內文 → 記下 `url`。
3. **海巡任務**：到了間隔時間 → 搜尋關鍵字 → 略過 `seen` 裡的貼文 → AI 判斷並寫留言 → 排進 `comments`。
4. **留言佇列**：依每帳號每小時上限，送出 `approved` 的留言。

程式中斷時卡在 `sending` 的項目，下次啟動會自動恢復成待發狀態。

### Threads DOM 對照（`threads_bot.py`）

選擇器於 2026-11-27 實地確認，記錄在 `threads_bot.py` 檔頭。**Threads 改版時主要調整這個檔案。**

| 操作 | 選擇器 |
| --- | --- |
| 貼文容器 | `div[data-pressable-container="true"]`，內含 `a[href="/@user/post/<code>"]` 與 `<time datetime>` |
| 搜尋排序 | `a[aria-label="最近"]` / `a[aria-label="最相關"]` |
| 發文 | 「新串文」或「有什麼新鮮事？」按鈕（必須真實滑鼠點擊）→ `div[role="dialog"]` 內的 contenteditable 與「發佈」按鈕 |
| 回覆框 | `[contenteditable][role="textbox"]`，`aria-placeholder` 以「回覆」開頭 |
| 回覆送出 | 同區塊內 svg `<title>` 為「回覆」的按鈕 |
| 附圖回覆 | `[aria-label="展開撰寫工具"]` 開完整視窗 |

### 資料庫結構（`data/threads.db`）

| 資料表 | 用途 | 重要欄位 |
| --- | --- | --- |
| `accounts` | 帳號 | `name`、`username`、`logged_in`、`checked_at` |
| `posts` | 貼文 | `text`、`images`、`scheduled_at`、`status`（`pending` / `scheduled` / `sending` / `sent` / `failed`）、`source`（`manual` / `auto`）、`posted_at`、`url` |
| `autopost` | 自動發文規則（每帳號一筆） | `topics`、`persona`、`per_day`、`start_hour`、`end_hour`、`length`、`review`、`next_at` |
| `tasks` | 海巡任務 | `keywords`、`recent`、`mode`（`auto` / `review`）、`interval_min`、`max_per_run`、`min_likes`、`last_run` |
| `comments` | 留言 | `post_url`、`author`、`post_text`、`draft`、`status`（`pending` / `approved` / `sending` / `sent` / `failed` / `skipped` / `rejected`）、`sent_at` |
| `seen` | 海巡看過的貼文 | `(account_id, post_url)` |
| `logs` | 執行紀錄 | `ts`、`level`、`msg` |
| `settings` | 鍵值設定 | AI 來源、金鑰、模型、每小時上限、品牌定位 |

欄位升級寫在 `db.init()`：用 `PRAGMA table_info` 檢查，缺了才 `ALTER TABLE`。新增欄位請照同樣模式。

### API 一覽

伺服器只監聽 `127.0.0.1`。

| 方法 | 路徑 | 說明 |
| --- | --- | --- |
| GET | `/api/state` | 總覽統計與執行狀態 |
| POST | `/api/worker/toggle` | 啟動或暫停背景排程 |
| GET / POST | `/api/accounts` | 列出或新增帳號 |
| PUT / DELETE | `/api/accounts/{id}` | 修改或刪除帳號 |
| POST | `/api/accounts/{id}/open` · `/close` · `/check` | 開或關瀏覽器、檢查登入 |
| GET / POST | `/api/posts` | 列出或新增貼文 |
| PUT / DELETE | `/api/posts/{id}` | 編輯或刪除貼文 |
| POST | `/api/posts/{id}/now` | 立即發出（或重試、核准） |
| POST | `/api/posts/find_urls` | 替沒有連結的已發佈貼文補上網址 |
| POST | `/api/upload` · GET `/api/file` | 上傳或讀取附件 |
| POST | `/api/ai/posts` | AI 產生貼文 |
| POST | `/api/schedule/plan` | 產生排程時間 |
| GET / PUT | `/api/autopost` · `/api/autopost/{account_id}` | 自動發文規則 |
| GET / POST | `/api/tasks` | 列出或新增海巡任務 |
| PUT / DELETE | `/api/tasks/{id}` | 修改或刪除海巡任務 |
| POST | `/api/tasks/{id}/run` | 立即執行海巡 |
| GET | `/api/comments?status=` | 依狀態列出留言 |
| PUT | `/api/comments/{id}` | 修改留言 |
| POST | `/api/comments/{id}/retry` · `/cancel` · `/redraft` | 核准或重試、取消、AI 重寫 |
| POST | `/api/comments/approve_all` | 全部核准 |
| GET / PUT | `/api/settings` | 設定 |
| GET | `/api/ai/status` | CLI 安裝與登入狀態 |
| POST | `/api/ai/login` · `/models` · `/test` | AI 登入、模型清單、測試 |
| GET | `/api/logs?after=` | 增量讀取執行紀錄 |

### 開發注意事項

- 改 `web/` 只要重新整理視窗；改 `app/` 要重開程式。
- 前端每隔幾秒自動重畫列表；使用者正在輸入或開著對話框時會跳過，避免打斷。
- 所有瀏覽器操作集中在 `threads_bot.py`，按鈕文字比對以**繁體中文**介面為準。
- 刪除類操作一律走 `confirmDelete()` 二次確認，不使用瀏覽器原生 `confirm()`。

### 專案結構

```
Threads自動助手/
├── 啟動.bat              # 雙擊啟動
├── launcher.py           # 檢查並安裝套件，以無主控台模式啟動 main.py
├── main.py               # 進入點：初始化 DB、啟動 worker 與 API、開視窗
├── requirements.txt
├── app/
│   ├── db.py             # SQLite 結構、自動升級、設定、記錄
│   ├── server.py         # FastAPI REST API
│   ├── worker.py         # 背景排程
│   ├── threads_bot.py    # Threads 網頁操作
│   ├── cdp.py            # Chrome DevTools Protocol 封裝
│   └── ai.py             # AI 整合
├── web/
│   ├── index.html
│   ├── app.js            # 單頁介面
│   └── app.css
└── data/                 # 執行時產生，不納入版控
    ├── threads.db
    ├── app.log
    ├── profiles/         # 各帳號瀏覽器設定檔
    └── uploads/          # 上傳的附件
```

</details>

---

## 專案性質聲明

本專案為個人使用的私人工具，不是商業產品。

- 只保證在**開發者本人的環境**（Windows 11 專業版 + Chrome + 繁體中文 Threads 介面）下運作正常；
- Threads 網頁改版可能讓部分功能暫時失效，需要更新 `threads_bot.py` 的選擇器；
- 不保證永續維護，也不承擔因使用本工具所生的任何責任。

---

## Disclaimer（免責聲明）

### 1. 平台條款與帳號風險

本工具透過瀏覽器自動化操作 Threads 網頁。自動發文、自動留言等行為可能違反 Threads／Meta 的服務條款或社群守則，導致貼文觸及降低、功能限制、帳號暫停或永久停權。**開發者對因使用本工具造成的任何帳號損失或衍生糾紛，概不負責。**

### 2. AI 產生內容

貼文與留言由第三方 AI 服務產生，可能出現事實錯誤、不當用語或與原貼文脈絡不符的內容。建議使用「審核後才發／才送出」模式，**使用者須對以自己帳號發出的所有內容負完全責任。**

### 3. 禁止用途

請勿將本工具用於垃圾訊息、騷擾、詐騙、散布不實資訊、冒充他人、操縱輿論或任何違法行為。

### 4. 資料安全

本工具將登入 cookie 與 API 金鑰以明文存在本機 `data/` 資料夾。使用者應自行保護電腦與該資料夾的安全；因電腦遭入侵、資料夾外流所造成的損失，由使用者自行承擔。

### 5. 使用者責任

使用者應自行遵守所在地之法律法規，包括但不限於《個人資料保護法》《著作權法》《公平交易法》。任何因濫用、誤用或違法使用本工具所引發之法律糾紛、民事賠償或刑事責任，均由使用者個人承擔。

---

**使用本軟體，即視為您已完整閱讀並同意上述全部免責條款。**

<p align="right"><a href="#top">回到頂端</a></p>
