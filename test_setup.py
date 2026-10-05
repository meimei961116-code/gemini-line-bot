import os
from dotenv import load_dotenv

load_dotenv(override=True)

def test_imports():
    print("=== 測試套件引用 ===")
    try:
        import flask
        print(f"Flask 版本: {flask.__version__} [OK]")
    except Exception as e:
        print(f"Flask 引用失敗: {e}")

    try:
        import linebot.v3
        print("line-bot-sdk v3 [OK]")
    except Exception as e:
        print(f"line-bot-sdk 引用失敗: {e}")

    try:
        import google.genai
        print("google.genai [OK]")
    except Exception as e:
        print(f"google.genai 引用失敗: {e}")

def test_gemini_api():
    print("\n=== 測試 Gemini API 連線 ===")
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key or api_key.startswith("your_"):
        print("[SKIP] .env 中尚未填入 GEMINI_API_KEY，略過連線測試。")
        return

    try:
        from gemini_service import GeminiService
        service = GeminiService()
        reply = service.generate_reply("test_user_001", "請用一句話介紹你自己")
        print(f"Gemini 回應測試成功: {reply}")
    except Exception as e:
        print(f"Gemini 連線測試失敗: {e}")

if __name__ == "__main__":
    test_imports()
    test_gemini_api()
