# Gemini LINE Bot (Python Flask + line-bot-sdk v3)

這是一個以 Python Flask 與 LINE Bot SDK v3 為基礎，串接 Google Gemini API 打造的多輪對話 AI 智慧助理。

---

## 快速啟動指南

### 1. 填寫金鑰 `.env`
請以文字編輯器打開專案目錄下的 `.env` 檔案，填入以下三項資訊：
- `LINE_CHANNEL_SECRET`：LINE 後台或 Developers 的 Channel Secret
- `LINE_CHANNEL_ACCESS_TOKEN`：LINE Developers 的 Messaging API 分頁發行的 Channel Access Token
- `GEMINI_API_KEY`：Google AI Studio 取得的 API Key

### 2. 安裝依賴套件
```bash
pip install -r requirements.txt
```

### 3. 測試環境與金鑰
```bash
python test_setup.py
```

### 4. 啟動伺服器
```bash
python app.py
```
預設會監聽 `http://localhost:5000`。
打開瀏覽器訪問 `http://localhost:5000/health`，可檢查設定是否完整。

---

## 本機測試 Webhook (使用 ngrok 或 Cloudflare Tunnel)

### 方式 A：使用 ngrok
1. 下載並安裝 [ngrok](https://ngrok.com/)
2. 執行：
   ```bash
   ngrok http 5000
   ```
3. 複製得到的 Forwarding 網址（例如：`https://xxxx.ngrok-free.app`）
4. 回到 LINE 後台的 **Webhook 網址** 欄位填入：
   `https://xxxx.ngrok-free.app/callback`
5. 點擊「儲存」並進行「驗證」。

### 方式 B：使用 Cloudflare Tunnel (免登入免費臨時通道)
```bash
cloudflared tunnel --url http://localhost:5000
```
同樣將產生的 `https://xxxx.trycloudflare.com/callback` 填入 Webhook 網址即可。
