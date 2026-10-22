@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ==========================================
echo  學習單系統 - 更新並開啟本機預覽
echo ==========================================
echo.

echo [1/2] 正在下載最新版本 (git pull)...
git pull --ff-only
if errorlevel 1 (
    echo.
    echo  ！更新失敗：可能沒有網路，或本機檔案有未儲存的修改。
    echo  　仍會用目前的版本開啟預覽。
)
echo.

echo [2/2] 啟動預覽伺服器
echo  網址：http://localhost:8080
echo  關閉此視窗即可停止伺服器
echo.

:: 2 秒後自動開啟瀏覽器（等伺服器就緒）
start "" cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:8080"

:: 啟動本機伺服器（阻塞直到視窗關閉）
python -m http.server 8080
