import os
import logging
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ShowLoadingAnimationRequest,
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)
from gemini_service import GeminiService

logger = logging.getLogger(__name__)

gemini_service = GeminiService()

def get_handler():
    channel_secret = os.getenv("LINE_CHANNEL_SECRET", "").strip()
    if not channel_secret or channel_secret.startswith("your_"):
        return None
    
    handler = WebhookHandler(channel_secret)

    @handler.add(MessageEvent, message=TextMessageContent)
    def handle_text_message(event):
        user_id = event.source.user_id
        user_text = event.message.text.strip()
        logger.info(f"收到來自用戶 [{user_id}] 的訊息: {user_text}")

        access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "").strip()
        if not access_token or access_token.startswith("your_"):
            logger.error("尚未設定 LINE_CHANNEL_ACCESS_TOKEN，無法發送回覆。")
            return

        config = Configuration(access_token=access_token)
        with ApiClient(config) as api_client:
            line_bot_api = MessagingApi(api_client)

            # 1. 嘗試顯示載入中動畫 (LINE 官方功能，若帳號權限支援)
            try:
                line_bot_api.show_loading_animation(
                    ShowLoadingAnimationRequest(chatId=user_id, loadingSeconds=20)
                )
            except Exception as e:
                logger.debug(f"Loading animation optional call note: {e}")

            # 2. 獲取 Gemini AI 回覆
            ai_reply = gemini_service.generate_reply(user_id, user_text)

            # 3. 處理 LINE 單則訊息 5000 字上限，切分長訊息
            reply_messages = []
            max_len = 4900
            for i in range(0, len(ai_reply), max_len):
                reply_messages.append(TextMessage(text=ai_reply[i:i + max_len]))

            # LINE API 單次回覆最多 5 則訊息限制
            try:
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=reply_messages[:5]
                    )
                )
                logger.info(f"已成功回覆用戶 [{user_id}]")
            except Exception as e:
                logger.error(f"LINE reply_message 呼叫失敗: {e}", exc_info=True)

    return handler
