@echo off
chcp 65001 >nul
echo ==========================================
echo    Cloudflare Tunnel 啟動器 (LINE Webhook)
echo ==========================================
echo 正在為本機 http://localhost:5000 建立公網 HTTPS 通道...
echo.
echo 請留意畫面中輸出的網址（格式如：https://xxxx.trycloudflare.com）
echo 取得網址後，在結尾加上 /callback，例如：
echo https://xxxx.trycloudflare.com/callback
echo 貼回 LINE 後台的 Webhook 網址欄位即可！
echo ==========================================
echo.
cloudflared tunnel --url http://localhost:5000
pause
