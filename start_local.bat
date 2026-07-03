@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ==========================================
echo  學習單系統 - 本機預覽伺服器
echo  網址：http://localhost:8080
echo  關閉此視窗即可停止伺服器
echo ==========================================
echo.

:: 2 秒後自動開啟瀏覽器（等伺服器就緒）
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:8080"

:: 啟動本機伺服器（阻塞直到視窗關閉）
python -m http.server 8080
