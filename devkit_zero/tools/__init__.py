"""
工具模块包

这个包包含所有的开发工具模块。
每个工具模块都需要实现三个标准函数：
1. main_function() - 核心功能实现
2. register_parser() - 注册CLI参数
3. main() - CLI入口函数
"""

from . import formatter
from . import random_gen
from . import diff_tool
from . import converter
from . import linter
from . import regex_tester
from . import batch_process
from . import markdown_preview
from . import port_checker

# 工具注册字典
AVAILABLE_TOOLS = {
    'formatter': formatter,
    'random_gen': random_gen,
    'diff_tool': diff_tool,
    'converter': converter,
    'linter': linter,
    'regex_tester': regex_tester,
    'batch_process': batch_process,
    'markdown_preview': markdown_preview,
    'port_checker': port_checker,
}

__all__ = [ 'formatter',
    'random_gen', 
    'diff_tool',
    'converter',
    'linter',
    'regex_tester',
    'batch_process',
    'markdown_preview',
    'port_checker'
    ]
