"""
DevKit-Zero 核心类
提供统一的 API 接口和工具管理
"""

from typing import List
from . import tools


class DevKitCore:
    """DevKit-Zero 核心类，提供统一的工具访问接口"""

    def __init__(self):
        self._tools = {
            'random_gen': tools.random_gen
        }

    def get_tool(self, name: str):
        """获取指定工具模块"""
        if name not in self._tools:
            raise ValueError(f"未知工具: {name}. 可用工具: {list(self._tools.keys())}")
        return self._tools[name]

    def list_tools(self) -> List[str]:
        """列出所有可用工具"""
        return list(self._tools.keys())

    def generate_uuid(self) -> str:
        """快捷方法：生成 UUID"""
        return self._tools['random_gen'].generate_uuid()

    def generate_password(self, length: int = 16) -> str:
        """快捷方法：生成安全密码"""
        return self._tools['random_gen'].generate_secure_password(length)

# 创建全局实例
devkit = DevKitCore()