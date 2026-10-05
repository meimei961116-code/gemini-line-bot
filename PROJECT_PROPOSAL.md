# 【專案計畫書】LINE Bot × Google Gemini 智慧對話助理建置案

---

## 📌 一、 專案摘要 (Executive Summary)

* **專案名稱**：LINE 官方智慧對話助理（LINE Bot Powered by Google Gemini AI）
* **專案定位**：新一代生成式 AI 企業/個人客服與智慧諮詢助理
* **核心技術**：Python 3.12、Flask、LINE Messaging API SDK v3、Google Gemini 3.5 Flash 旗艦模型、Cloudflare Tunneling
* **專案目標**：打造具備高邏輯思考能力、上下文多輪對話記憶、即時時空感知與資安防護的 24 小時無間斷 LINE 智慧對話系統。

---

## 🎯 二、 專案背景與效益目標 (Background & Objectives)

### 2.1 專案背景
傳統 LINE 官方帳號的「關鍵字回覆」或「規則式問答」彈性極低，一旦用戶用詞稍微偏離設定即無法回答，造成極高的維護成本與不良的使用者體驗。本專案引進 **Google 旗艦級大型語言模型（LLM）**，將傳統死板的關鍵字回覆升級為具有強大自然語言理解、深度邏輯推論與流暢繁體中文對話能力的 AI 全功能助理。

### 2.2 核心目標 (SMART Goals)
1. **即時回應能力**：整合 LINE SDK v3 規範，透過 Webhook 在數秒內提供高品質的生成式回應。
2. **思維深度升級**：注入高階結構化思考架構（Prompt Engineering），杜絕表面空話，直擊問題核心。
3. **時空認知校正**：動態注入真實世界時空資料，避免模型出現「時空停滯（停留於 2024/2025 或過去）」之幻覺。
4. **安全與合規性**：遵循 HMAC-SHA256 簽章安全比對，嚴格隔離敏感 API 金鑰（.env），符合資安最佳實踐。

---

## 🏗️ 三、 系統架構與流程設計 (Architecture & Flow)

```text
📱 LINE 使用者
      │
      ▼ (傳送文字訊息)
☁️ LINE Messaging API Platform
      │
      ▼ (POST Webhook HTTPS)
🌐 Cloudflare Tunnel (安全公網穿透通道)
      │
      ▼ (轉發至本機 Port 5000)
⚙️ Flask Webhook 伺服器 (app.py)
      │
      ▼ (簽章驗證與事件派發)
🛡️ LINE 事件處理器 (bot_handler.py)
      │  ├─ 顯示 LINE Loading 動畫
      │  └─ 處理長訊息 5000 字上限安全切分
      ▼
🧠 AI 大腦核心 (gemini_service.py)
      │  ├─ 動態注入 2026 當前真實時間
      │  ├─ 維護 10 輪上下文多輪記憶
      │  └─ 自動容錯與備援機制
      ▼
✨ Google Gemini 3.5 Flash 旗艦模型
      │
      ▼ (生成專業結構化內容)
📱 回傳給 LINE 使用者
```

---

## 🛠️ 四、 技術規格與模組劃分 (Technical Specifications)

| 模組名稱 | 採用技術 | 核心職責 |
| :--- | :--- | :--- |
| **Web 伺服端** | Python 3.12 / Flask 3.1.3 | 負責監聽本機 5000 埠、路由分發、提供 `/health` 健康檢查端點。 |
| **通訊與事件處理** | `line-bot-sdk v3.26+` | 處理 LINE Webhook 事件、執行簽章驗證、發送「輸入中動畫 (Loading)」及回覆訊息。 |
| **AI 推理引擎** | `google-genai` SDK | 封裝 Google Gemini API 調用，動態管理用戶上下文記憶、時空提示詞注入與容錯備援。 |
| **外網通道** | Cloudflare Tunnel (`cloudflared`) | 提供企業級加密的臨時/永久公網 HTTPS 域名，免複雜防火牆與 Port Forwarding 設定。 |
| **組態與資安隔離** | `python-dotenv` / Git | 透過 `.env` 本地保存 Channel Secret 與 API Key，`.gitignore` 阻斷敏感資訊外洩。 |

---

## 🔒 五、 資安與隱私控制策略 (Security & Compliance)

1. **Webhook 簽章驗證 (HMAC-SHA256)**：
   每次 LINE 平台發送請求時皆會附帶 `X-Line-Signature`，伺服端透過 `LINE_CHANNEL_SECRET` 即時計算比對，徹底阻絕惡意偽造請求與重放攻擊。
2. **機敏憑證徹底隔離 (Secret Isolation)**：
   - 所有的私密 Token（LINE Channel Secret、Access Token、Gemini API Key）均存放於本地 `.env` 檔案中。
   - 專案已預先配置 `.gitignore`，將 `.env`、快取與環境檔列為最高黑名單，確保 Git/GitHub 協作時 100% 不外洩。
3. **短期對話隔離與隱私安全**：
   - 用戶歷史對話以 `user_id` 作為 Key 暫存於記憶體結構中，僅維護最近 10 輪上下文，不私自留存硬碟敏感明文記錄。

---

## 📅 六、 實施歷程與里程碑 (Milestones & Roadmap)

* **階段一：基礎建設（已達成 ✅）**
  - 完成 Python 3.12 與 Cloudflare Tunnel 部署。
  - 完成模組化程式架構設計 (`app.py`, `bot_handler.py`, `gemini_service.py`)。
* **階段二：LINE Messaging API 深度串接（已達成 ✅）**
  - 遵循 2024 年 9 月新制流程，成功從 LINE Official Account Manager 啟用 Messaging API。
  - 正確配置 Webhook URL，雙向通道與安全簽章驗證測試通過。
* **階段三：模型優化與時空校準（已達成 ✅）**
  - 成功解決 LLM 訓練截止時空問題，完成動態年份與日期動態注入。
  - 升級為 **Gemini 3.5 Flash** 旗艦推論模型，調整 Temperature 為 0.4，記憶長度擴充至 10 輪。
* **階段四：資安加固與文件交付（已達成 ✅）**
  - 建立 Git 版本控制與安全防護機制。
  - 交付本專案完整計畫書與啟動文檔。

---

## 📈 七、 效益評估 (Value & Impact)

| 評估維度 | 導入前（傳統客服/無 AI） | 導入後（Gemini AI LINE Bot） | 效益提升 |
| :--- | :--- | :--- | :--- |
| **回應即時性** | 依賴人工手動回覆，非上班時間無法處理 | 7×24 小時全年無休秒級回應 | **提升 95% 以上** |
| **問題解決覆蓋率** | 僅能回答預設關鍵字，稍有錯字即失效 | 具備語意理解與邏輯推理，能回答多元複雜問題 | **提升 80% 以上** |
| **人工客服成本** | 需配置專人看守後台回答重複性問題 | 攔截 80% 以上常規問題，人工僅需處理高價值個案 | **大幅節省人力時間成本** |
| **互動體驗與專業度** | 死板罐頭文字 | 結構化分析、排版精美、主動提供洞察與建議 | **大幅提升品牌形象與滿意度** |

---

## 🚀 八、 未來進階擴充建議 (Future Recommendations)

1. **圖文選單 (Rich Menu) 導航**：在 LINE 底部客製化圖文功能按鈕（常見問題、聯絡專人、官方網站）。
2. **外部私有知識庫 (RAG - 檢索增強生成)**：掛載向量資料庫（如 Chroma / Pinecone），讓 Gemini 能查閱內部手冊、價目表後精準作答。
3. **長期資料庫與用戶標籤**：將短期對話記憶移至 SQLite 或 PostgreSQL，並記錄用戶喜好，實現深度個人化推播。
4. **雲端全天候託管 (Cloud Deployment)**：一鍵部屬至 Zeabur、Render 或 Google Cloud Run，電腦關機時機器人依然能 24 小時線上運作。
