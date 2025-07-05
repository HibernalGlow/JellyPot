@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo =====================================================
echo    PPJF 自动配置和运行工具
echo    Jellyfin + PotPlayer 整合系统
echo =====================================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到 Python，请先安装 Python 3.7 或更高版本
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM 检查配置文件是否存在
if not exist "config.json" (
    echo 🛠️  首次运行，启动配置向导...
    echo.
    python setup.py
    echo.
    if errorlevel 1 (
        echo ❌ 配置失败
        pause
        exit /b 1
    )
) else (
    echo 📋 检测到现有配置，启动管理界面...
    echo.
    python run.py
)

echo.
echo 操作完成
pause
