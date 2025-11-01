"""
DevKit-Zero: 零依赖开发者工具箱

这是一个轻量级、零依赖、功能强大的开发者工具箱，提供统一的 API 接口
和命令行界面，解决开发者在代码处理、文本操作和环境辅助方面的高频需求。

基本用法:
    # 作为库使用
    from devkit_zero import formatter, random_gen, diff_tool

    # 格式化代码
    result = formatter.format_code("def hello(): print('hi')", "python")

    # 生成随机数据
    uuid = random_gen.generate_uuid()
    password = random_gen.generate_secure_password()

    # 对比文本差异
    diff = diff_tool.compare_texts("text1", "text2")

命令行用法:
    # 直接运行
    devkit-zero format --input "code" --language python
    devkit-zero random uuid
    devkit-zero diff --text1 "hello" --text2 "world"

    # 或使用简短别名
    devkit format --help
    devkit random --help
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
    port_checker,
    
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
