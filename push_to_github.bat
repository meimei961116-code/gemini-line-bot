@echo off
chcp 65001 >nul
echo ==========================================
echo    GitHub 上傳工具 (Git Push)
echo ==========================================
echo 目標儲存庫: https://github.com/meimei961116-code/gemini-line-bot.git
echo.
echo [說明] 如果這是本機第一次連接 GitHub，系統可能會跳出瀏覽器要求登入授權。
echo 請在瀏覽器中點擊綠色授權按鈕即可！
echo ==========================================
echo.

git push -u origin main

echo.
if %errorlevel% equ 0 (
    echo ==========================================
    echo [成功] 專案程式碼已成功推播至 GitHub！
    echo 網址: https://github.com/meimei961116-code/gemini-line-bot
    echo ==========================================
) else (
    echo ==========================================
    echo [提醒] 若出現權限錯誤，請確認：
    echo 1. 是否已在 GitHub 建立名稱為 gemini-line-bot 的儲存庫
    echo 2. 是否已在彈出的瀏覽器視窗中完成授權
    echo ==========================================
)
pause
