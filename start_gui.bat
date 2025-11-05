@echo off
REM DevKit-Zero GUI 启动脚本 (Windows)
REM 使用方法: 双击此文件或在命令行运行 start_gui.bat

cd /d "%~dp0"
echo 正在启动 DevKit-Zero GUI...
python -m devkit_zero.gui_main

if errorlevel 1 (
    echo.
    echo 启动失败! 请检查:
    echo 1. 是否已安装 Python 3.7+
    echo 2. 是否安装了必要的依赖: pip install -r requirements.txt
    echo 3. 是否在项目根目录运行此脚本
    pause
)
