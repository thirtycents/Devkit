"""
DevKit-Zero: Zero Dependency Developer Toolkit

A lightweight, zero-dependency, powerful developer toolkit providing a unified API
and CLI to solve high-frequency needs in code processing, text manipulation, and environment assistance.

Basic Usage:
    # Import as a library
    from devkit_zero import formatter, random_gen, diff_tool

    # Format code
    result = formatter.format_code("def hello(): print('hi')", "python")

    # Generate random data
    uuid = random_gen.generate_uuid()
    password = random_gen.generate_secure_password()

    # Compare text differences
    diff = diff_tool.compare_text("text1", "text2")


Command Line Usage:
    # Run directly
    devkit-zero format --input "code" --language python
    devkit-zero random uuid
    devkit-zero diff --text1 "hello" --text2 "world"

    # Or use short alias
    devkit format --help
    devkit random --help
"""

__version__ = "0.1.0"
from .__version__ import __version__, __author__, __email__, __description__

# Import all tool modules to make them directly importable from the package
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
    unused_func_detector,
    api_contract_diff,
    Robot_checker,
)

# Import core classes and functions (for advanced users)
from .core import DevKitCore

__all__ = [
    # Version Information
    '__version__',
    '__author__', 
    '__email__',
    '__description__',
    
    # Tool Modules
    'formatter',
    'random_gen',
    'diff_tool', 
    'converter',
    'linter',
    'regex_tester',
    'batch_process',
    'markdown_preview',
    'port_checker',
    'unused_func_detector',
    'api_contract_diff',
    'Robot_checker',
    
    # Core Classes
    'DevKitCore',
]


def get_version():
    """Get version information"""
    return __version__


def get_available_tools():
    """Get list of available tools"""
    return [
        'formatter',           # Code Formatting
        'random_gen',          # Random Data Generation
        'diff_tool',           # Text Difference Comparison
        'converter',           # Data Format Conversion
        'linter',              # Static Code Analysis
        'regex_tester',        # Regex Testing
        'batch_process',       # Batch File Processing
        'markdown_preview',    # Markdown Preview
        'port_checker',        # Port Checking
        'unused_func_detector', # Unused Function Detection
        'api_contract_diff',   # API Contract Comparison
        'Robot_checker',       # Robots.txt Checker
    ]


def info():
    """Show package information"""
    return {
        'name': 'DevKit-Zero',
        'version': __version__,
        'description': __description__,
        'author': __author__,
        'email': __email__,
        'tools': get_available_tools(),
        'python_requires': '>=3.7'
    }
