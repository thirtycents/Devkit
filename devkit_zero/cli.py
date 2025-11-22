#!/usr/bin/env python3
"""
DevKit-Zero Command Line Interface
Provides a unified CLI entry point
"""

import argparse
import sys
import os
from typing import Optional

# Handle relative import and fallback for direct execution
try:
    # Try relative import (when running as a module: python -m devkit_zero.cli)
    from .tools import formatter, random_gen, diff_tool, converter, linter, port_checker, unused_func_detector, api_contract_diff, Robot_checker, regex_tester
    from .__version__ import __version__, __description__
except ImportError:
    # Fallback: add parent directory to path and use absolute imports
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from devkit_zero.tools import formatter, random_gen, diff_tool, converter, linter, port_checker, unused_func_detector, api_contract_diff, Robot_checker, regex_tester
    from devkit_zero.__version__ import __version__, __description__


def create_parser() -> argparse.ArgumentParser:
    """Create main command line parser"""
    parser = argparse.ArgumentParser(
        prog='devkit-zero',
        description=__description__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example Usage:
  devkit-zero format --input "def hello(): print('hi')" --language python
  devkit-zero random uuid
  devkit-zero diff --text1 "hello" --text2 "world"
  devkit-zero lint --code "def bad_function(): pass"
  
For more information, visit: https://github.com/devkit-zero/devkit-zero
        """
    )
    
    parser.add_argument(
        '--version', '-V',
        action='version',
        version=f'DevKit-Zero {__version__}'
    )
    
    # Create subcommands
    subparsers = parser.add_subparsers(
        dest='tool',
        help='Available Tools',
        metavar='TOOL'
    )
    subparsers.required = True
    
    # Register subcommands for all tools
    formatter.register_parser(subparsers)
    random_gen.register_parser(subparsers)
    diff_tool.register_parser(subparsers)
    converter.register_parser(subparsers)
    linter.register_parser(subparsers)
    regex_tester.register_parser(subparsers)
    # batch_process only supports GUI
    # markdown_preview only supports GUI
    port_checker.register_parser(subparsers)
    unused_func_detector.register_parser(subparsers)
    api_contract_diff.register_parser(subparsers)
    Robot_checker.register_parser(subparsers)
    
    return parser


def main(argv: Optional[list] = None) -> int:
    """Main entry function"""
    parser = create_parser()
    
    try:
        args = parser.parse_args(argv)
        
        # Execute corresponding tool
        result = args.func(args)
        
        if result is not None:
            print(result)
        
        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        return 130
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cli() -> int:
    """CLI entry point (for entry_points)"""
    return main()


if __name__ == '__main__':
    sys.exit(main())