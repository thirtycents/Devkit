#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
导入测试脚本

用途：验证项目结构和导入是否正确配置
使用：python test_imports.py (从项目根目录)
"""

import sys
from pathlib import Path


def test_imports():
    """测试各项导入"""
    print("=" * 60)
    print("DevKit-Zero 导入测试")
    print("=" * 60)
    
    # 测试1: 检查项目结构
    print("\n[测试1] 检查项目结构...")
    root_dir = Path(__file__).parent
    required_files = [
        "devkit_zero/__init__.py",
        "devkit_zero/tools/__init__.py",
        "devkit_zero/ui/__init__.py",
        "setup.py",
        "requirements.txt",
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = root_dir / file_path
        exists = full_path.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {file_path}")
        if not exists:
            all_exist = False
    
    if not all_exist:
        print("\n❌ 错误: 缺少必要的文件")
        return False
    
    # 测试2: 导入核心模块
    print("\n[测试2] 导入核心模块...")
    try:
        import devkit_zero
        print("  ✅ import devkit_zero")
    except ImportError as e:
        print(f"  ❌ import devkit_zero 失败: {e}")
        return False
    
    # 测试3: 导入工具模块
    print("\n[测试3] 导入工具模块...")
    try:
        from devkit_zero.tools import formatter
        print("  ✅ from devkit_zero.tools import formatter")
    except ImportError as e:
        print(f"  ❌ 导入formatter失败: {e}")
        return False
    
    # 测试4: 导入UI模块
    print("\n[测试4] 导入UI模块...")
    try:
        from devkit_zero.ui import gui_app
        print("  ✅ from devkit_zero.ui import gui_app")
    except ImportError as e:
        print(f"  ❌ 导入gui_app失败: {e}")
        return False
    
    # 测试5: 测试formatter功能
    print("\n[测试5] 测试formatter功能...")
    try:
        test_code = "x=1\ny=2"
        result = formatter.format_python_code(test_code)
        if result:
            print("  ✅ formatter.format_python_code() 可用")
        else:
            print("  ⚠️  formatter返回空结果")
    except Exception as e:
        print(f"  ❌ formatter测试失败: {e}")
        return False
    
    # 测试6: 创建GUI实例
    print("\n[测试6] 创建GUI实例...")
    try:
        # 不实际运行GUI，只创建实例
        app = gui_app.DevKitZeroGUI()
        print("  ✅ DevKitZeroGUI 实例创建成功")
        # 不调用app.run()避免窗口显示
    except Exception as e:
        print(f"  ❌ GUI实例创建失败: {e}")
        return False
    
    # 测试完成
    print("\n" + "=" * 60)
    print("✅ 所有导入测试通过!")
    print("=" * 60)
    print("\n下一步:")
    print("  1. 运行GUI: python -m devkit_zero.ui.gui_app")
    print("  2. 或安装后运行: pip install -e . && devkit-zero-gui")
    print("  3. 运行CLI: devkit-zero --help")
    
    return True


if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
