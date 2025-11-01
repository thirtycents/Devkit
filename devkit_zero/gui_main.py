#!/usr/bin/env python3
"""
DevKit-Zero GUI 主程序入口
"""

import sys
import os
from typing import Optional


def main(argv: Optional[list] = None) -> int:
    """GUI 主入口函数"""
    try:
        # 延迟导入 tkinter，避免在无 GUI 环境中出错
        try:
            import tkinter as tk
        except ImportError:
            print("错误: 无法导入 tkinter。请确保安装了 Python 的 tkinter 支持。", file=sys.stderr)
            print("在某些 Linux 发行版中，您可能需要安装 python3-tkinter 包。", file=sys.stderr)
            return 1
        
        from .ui.gui_app import DevKitZeroGUI
        
        app = DevKitZeroGUI()
        app.run()
        return 0
        
    except KeyboardInterrupt:
        return 130
        
    except Exception as e:
        print(f"GUI 启动错误: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())