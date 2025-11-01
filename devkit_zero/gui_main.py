"""
DevKit-Zero GUI主入口

这个模块实现图形界面的启动入口。
"""

# 兼容：作为包导入时使用相对导入，直接作为脚本运行时使用绝对导入
try:
    from .ui.gui_app import DevKitZeroGUI
except Exception:
    # 当直接运行脚本 (__package__ 为 None) 时，尝试绝对导入
    from devkit_zero.ui.gui_app import DevKitZeroGUI


def main():
    """启动GUI界面"""
    app = DevKitZeroGUI()
    app.run()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
