#!/bin/bash
# DevKit-Zero GUI 启动脚本 (Linux/Mac)
# 使用方法: ./start_gui.sh

cd "$(dirname "$0")"
echo "正在启动 DevKit-Zero GUI..."
python3 -m devkit_zero.gui_main

if [ $? -ne 0 ]; then
    echo ""
    echo "启动失败! 请检查:"
    echo "1. 是否已安装 Python 3.7+"
    echo "2. 是否安装了必要的依赖: pip3 install -r requirements.txt"
    echo "3. 是否安装了 tkinter: sudo apt-get install python3-tk (Ubuntu/Debian)"
    read -p "按回车键退出..."
fi
