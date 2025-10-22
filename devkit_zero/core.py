"""
DevKit-Zero 核心类
提供统一的 API 接口和工具管理
"""

from typing import Any, Dict, List, Optional
from . import tools


class DevKitCore:
    """DevKit-Zero 核心类，提供统一的工具访问接口"""
    
    def __init__(self):
        self._tools = {
            'formatter': tools.formatter,
            'random_gen': tools.random_gen,
            'diff_tool': tools.diff_tool,
            'converter': tools.converter,
            'linter': tools.linter,
            'regex_tester': tools.regex_tester,
            'batch_process': tools.batch_process,
            'markdown_preview': tools.markdown_preview,
            'port_checker': tools.port_checker,
        }
    
    def get_tool(self, name: str):
        """获取指定工具模块"""
        if name not in self._tools:
            raise ValueError(f"未知工具: {name}. 可用工具: {list(self._tools.keys())}")
        return self._tools[name]
    
    def list_tools(self) -> List[str]:
        """列出所有可用工具"""
        return list(self._tools.keys())
    
    def format_code(self, code: str, language: str) -> str:
        """快捷方法：格式化代码"""
        return self._tools['formatter'].format_code(code, language)
    
    def generate_uuid(self) -> str:
        """快捷方法：生成 UUID"""
        return self._tools['random_gen'].generate_uuid()
    
    def generate_password(self, length: int = 16) -> str:
        """快捷方法：生成安全密码"""
        return self._tools['random_gen'].generate_secure_password(length)
    
    def compare_texts(self, text1: str, text2: str) -> List[str]:
        """快捷方法：对比文本差异"""
        return self._tools['diff_tool'].compare_texts(text1, text2)
    
    def lint_code(self, code: str, filename: str = "<string>") -> List[Dict[str, Any]]:
        """快捷方法：检查代码"""
        return self._tools['linter'].lint_code(code, filename)
    
    def test_regex(self, pattern: str, text: str) -> Dict[str, Any]:
        """快捷方法：测试正则表达式"""
        return self._tools['regex_tester'].test_regex(pattern, text)
    
    def markdown_to_html(self, markdown_text: str) -> str:
        """快捷方法：转换 Markdown 到 HTML"""
        return self._tools['markdown_preview'].markdown_to_html(markdown_text)
    
    def check_port(self, host: str, port: int) -> Dict[str, Any]:
        """快捷方法：检查端口"""
        return self._tools['port_checker'].check_port(host, port)


# 创建全局实例
devkit = DevKitCore()