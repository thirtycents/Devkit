"""
DevKit-Zero Core Class
Provides unified API interface and tool management
"""

from typing import Any, Dict, List, Optional
from . import tools


class DevKitCore:
    """DevKit-Zero Core Class, providing unified tool access interface"""
    
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
        """Get specified tool module"""
        if name not in self._tools:
            raise ValueError(f"Unknown tool: {name}. Available tools: {list(self._tools.keys())}")
        return self._tools[name]
    
    def list_tools(self) -> List[str]:
        """List all available tools"""
        return list(self._tools.keys())
    
    def format_code(self, code: str, language: str) -> str:
        """Shortcut: Format code"""
        return self._tools['formatter'].format_code(code, language)
    
    def generate_uuid(self) -> str:
        """Shortcut: Generate UUID"""
        return self._tools['random_gen'].generate_uuid()
    
    def generate_password(self, length: int = 16) -> str:
        """Shortcut: Generate secure password"""
        return self._tools['random_gen'].generate_secure_password(length)
    
    def compare_texts(self, text1: str, text2: str) -> List[str]:
        """Shortcut: Compare text differences"""
        return self._tools['diff_tool'].compare_text(text1, text2)
    
    def lint_code(self, code: str, filename: str = "<string>") -> List[Dict[str, Any]]:
        """Shortcut: Lint code"""
        return self._tools['linter'].lint_code(code, filename)
    
    def test_regex(self, pattern: str, text: str) -> Dict[str, Any]:
        """Shortcut: Test regex"""
        return self._tools['regex_tester'].test_regex(pattern, text)
    
    def markdown_to_html(self, markdown_text: str) -> str:
        """Shortcut: Convert Markdown to HTML"""
        return self._tools['markdown_preview'].markdown_to_html(markdown_text)
    
    def check_port(self, host: str, port: int) -> Dict[str, Any]:
        """Shortcut: Check port"""
        return self._tools['port_checker'].check_port(host, port)


# Create global instance
devkit = DevKitCore()