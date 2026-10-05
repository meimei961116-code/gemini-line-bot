import os
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.system_prompt = os.getenv(
            "AI_SYSTEM_PROMPT",
            "你是一位親切、聰明且熱心助人的繁體中文 AI 助理。請用生動、有條理且自然的繁體中文回答使用者的問題。"
        )
        self.chat_history = defaultdict(list)
        self.max_history_turns = 6
        self.client = None
        self._init_client()

    def _init_client(self):
        if not self.api_key or self.api_key.startswith("your_"):
            logger.warning("GEMINI_API_KEY 未設定或為預設值。")
            return

        # 優先嘗試最新 Google GenAI SDK
        try:
            from google import genai
            self.client_type = "genai"
            self.client = genai.Client(api_key=self.api_key)
            logger.info("成功初始化 google.genai Client")
            return
        except ImportError:
            pass

        # 退回嘗試 google-generativeai SDK
        try:
            import google.generativeai as genai_legacy
            self.client_type = "generativeai"
            genai_legacy.configure(api_key=self.api_key)
            self.legacy_model = genai_legacy.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=self.system_prompt
            )
            logger.info("成功初始化 google.generativeai Legacy Client")
            return
        except Exception as e:
            logger.error(f"初始化 Gemini Client 失敗: {e}")
            self.client_type = "none"

    def generate_reply(self, user_id: str, user_message: str) -> str:
        # 動態重新讀取金鑰（方便使用者剛填寫後無須重啟服務）
        current_key = os.getenv("GEMINI_API_KEY", "")
        if current_key != self.api_key:
            self.api_key = current_key
            self._init_client()

        if not self.api_key or self.api_key.startswith("your_"):
            return "【系統提醒】尚未設定 GEMINI_API_KEY，請在 .env 檔案中填入正確的金鑰後再試。"

        if not hasattr(self, "client_type") or self.client_type == "none":
            self._init_client()

        try:
            if getattr(self, "client_type", None) == "genai":
                from google.genai import types
                history = self.chat_history[user_id]
                history.append(types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=user_message)]
                ))

                # 維護最近 N 輪對話
                if len(history) > self.max_history_turns * 2:
                    history = history[-self.max_history_turns * 2:]
                    self.chat_history[user_id] = history

                # 優先使用官方最新 flash 模型
                model_candidates = ["gemini-flash-latest", "gemini-3.5-flash", "gemini-3.8-flash", "gemini-flash-lite-latest"]
                response = None
                for candidate in model_candidates:
                    try:
                        response = self.client.models.generate_content(
                            model=candidate,
                            contents=history,
                            config=types.GenerateContentConfig(
                                system_instruction=self.system_prompt,
                                temperature=0.7,
                            )
                        )
                        break
                    except Exception as me:
                        logger.warning(f"嘗試模型 {candidate} 失敗: {me}，嘗試下一個備援模型")
                        continue

                if response is None:
                    raise RuntimeError("所有可用 Gemini 模型皆未能回應")


                reply_text = response.text.strip() if response.text else "抱歉，AI 未能產出內容。"
                self.chat_history[user_id].append(types.Content(
                    role="model",
                    parts=[types.Part.from_text(text=reply_text)]
                ))
                return reply_text

            elif getattr(self, "client_type", None) == "generativeai":
                history = self.chat_history[user_id]
                chat = self.legacy_model.start_chat(history=history)
                response = chat.send_message(user_message)
                self.chat_history[user_id] = chat.history[-self.max_history_turns * 2:]
                return response.text.strip() if response.text else "抱歉，AI 未能產出內容。"

            else:
                return "Gemini SDK 初始化失敗，請檢查環境套件安裝狀態。"

        except Exception as e:
            logger.error(f"Gemini API 呼叫失敗: {e}", exc_info=True)
            return f"抱歉，AI 暫時無法處理您的訊息（錯誤訊息: {e}）"
