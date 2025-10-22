#!/usr/bin/env python3
"""
DevKit-Zero 命令行界面
提供统一的 CLI 入口点
"""

import argparse
import sys
from typing import Optional

from .tools import formatter, random_gen, diff_tool, converter, linter, regex_tester, batch_process, markdown_preview, port_checker
from .__version__ import __version__, __description__


def create_parser() -> argparse.ArgumentParser:
    """创建主命令行解析器"""
    parser = argparse.ArgumentParser(
        prog='devkit-zero',
        description=__description__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  devkit-zero format --input "def hello(): print('hi')" --language python
  devkit-zero random uuid
  devkit-zero diff --text1 "hello" --text2 "world"
  devkit-zero lint --code "def bad_function(): pass"
  
更多信息请访问: https://github.com/devkit-zero/devkit-zero
        """
    )
    
    parser.add_argument(
        '--version', '-V',
        action='version',
        version=f'DevKit-Zero {__version__}'
    )
    
    # 创建子命令
    subparsers = parser.add_subparsers(
        dest='tool',
        help='可用工具',
        metavar='TOOL'
    )
    subparsers.required = True
    
    # 注册所有工具的子命令
    formatter.register_parser(subparsers)
    random_gen.register_parser(subparsers)
    diff_tool.register_parser(subparsers)
    converter.register_parser(subparsers)
    linter.register_parser(subparsers)
    regex_tester.register_parser(subparsers)
    batch_process.register_parser(subparsers)
    markdown_preview.register_parser(subparsers)
    port_checker.register_parser(subparsers)
    
    return parser


def main(argv: Optional[list] = None) -> int:
    """主入口函数"""
    parser = create_parser()
    
    try:
        args = parser.parse_args(argv)
        
        # 执行对应的工具
        result = args.func(args)
        
        if result is not None:
            print(result)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n操作被用户取消", file=sys.stderr)
        return 130
        
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1


def cli() -> int:
    """CLI 入口点（用于 entry_points）"""
    return main()


if __name__ == '__main__':
    sys.exit(main())