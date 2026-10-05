import os
import logging
from flask import Flask, request, abort, jsonify
from dotenv import load_dotenv
from linebot.v3.exceptions import InvalidSignatureError

# 載入 .env 環境變數
load_dotenv(override=True)

# 設定 Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("line_bot_app")

from bot_handler import get_handler

app = Flask(__name__)

@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def health_check():
    secret_set = bool(os.getenv("LINE_CHANNEL_SECRET") and not os.getenv("LINE_CHANNEL_SECRET").startswith("your_"))
    token_set = bool(os.getenv("LINE_CHANNEL_ACCESS_TOKEN") and not os.getenv("LINE_CHANNEL_ACCESS_TOKEN").startswith("your_"))
    gemini_set = bool(os.getenv("GEMINI_API_KEY") and not os.getenv("GEMINI_API_KEY").startswith("your_"))

    return jsonify({
        "status": "healthy",
        "service": "line-bot-gemini",
        "configured": {
            "channel_secret": secret_set,
            "channel_access_token": token_set,
            "gemini_api_key": gemini_set
        },
        "tips": "請確保 configured 內各項皆為 true。若為 false，請至 .env 填寫正確金鑰後重啟服務。"
    }), 200

@app.route("/callback", methods=["POST"])
def callback():
    load_dotenv(override=True)
    handler = get_handler()
    if handler is None:
        logger.error("尚未在 .env 設定有效的 LINE_CHANNEL_SECRET！")
        return "LINE_CHANNEL_SECRET not set in .env", 500

    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.warning("無效的簽章 (InvalidSignatureError)！請檢查 .env 中的 LINE_CHANNEL_SECRET 是否正確。")
        abort(400)
    except Exception as e:
        logger.error(f"處理 Webhook 事件時發生未預期錯誤: {e}", exc_info=True)
        return "Internal Server Error", 500

    return "OK", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    logger.info(f"正在啟動 LINE Bot 伺服器，監聽 port {port}...")
    app.run(host="0.0.0.0", port=port, debug=debug)
