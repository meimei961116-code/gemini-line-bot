@echo off
chcp 65001 >nul
echo ==========================================
echo    Gemini LINE Bot 啟動器
echo ==========================================
echo 正在檢查 Python 環境...

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [錯誤] 找不到 Python，請確認已安裝 Python 並加入 PATH。
    pause
    exit /b
)

echo 正在啟動 Flask Webhook 伺服器...
python app.py
pause
