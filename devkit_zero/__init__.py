"""
DevKit-Zero 包初始化文件

这个文件定义了包的公共API接口。
"""

__version__ = "0.1.0"
from .__version__ import __version__, __author__, __email__, __description__

# 导入所有工具模块，使其可直接从包导入
from .tools import (
    formatter,
    random_gen, 
    diff_tool,
    converter,
    linter,
    regex_tester,
    batch_process,
    markdown_preview,
    port_checker
)

# 导入核心类和函数（便于高级用户使用）
from .core import DevKitCore

__all__ = [
    # 版本信息
    '__version__',
    '__author__', 
    '__email__',
    '__description__',
    
    # 工具模块
    'formatter',
    'random_gen',
    'diff_tool', 
    'converter',
    'linter',
    'regex_tester',
    'batch_process',
    'markdown_preview',
    'port_checker',
    
    # 核心类
    'DevKitCore',
]


def get_version():
    """获取版本信息"""
    return __version__


def get_available_tools():
    """获取可用工具列表"""
    return [
        'formatter',      # 代码格式化
        'random_gen',     # 随机数据生成
        'diff_tool',      # 文本差异对比
        'converter',      # 数据格式转换
        'linter',         # 代码静态检查
        'regex_tester',   # 正则表达式测试
        'batch_process',  # 批量文件处理
        'markdown_preview', # Markdown 预览
        'port_checker',   # 端口检查
    ]


def info():
    """显示包信息"""
    return {
        'name': 'DevKit-Zero',
        'version': __version__,
        'description': __description__,
        'author': __author__,
        'email': __email__,
        'tools': get_available_tools(),
        'python_requires': '>=3.7'
    }
