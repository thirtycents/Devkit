"""
随机数据生成工具

功能：生成UUID、密码、随机数等
负责人：待分配
优先级：高
"""

# TODO: 实现随机数据生成功能
# 参考 formatter.py 的结构实现

import random
import string
import uuid
import secrets
from typing import Optional


def generate_uuid(version: int = 4) -> str:
    """
    生成 UUID

    Args:
        version: UUID 版本 (1, 4)

    Returns:
        UUID 字符串
    """
    if version == 1:
        return str(uuid.uuid1())
    elif version == 4:
        return str(uuid.uuid4())
    else:
        raise ValueError(f"不支持的 UUID 版本: {version}")


def generate_random_string(length: int = 8,
                           include_numbers: bool = True,
                           include_uppercase: bool = True,
                           include_lowercase: bool = True,
                           include_symbols: bool = False,
                           custom_chars: Optional[str] = None) -> str:
    """
    生成随机字符串

    Args:
        length: 字符串长度
        include_numbers: 是否包含数字
        include_uppercase: 是否包含大写字母
        include_lowercase: 是否包含小写字母
        include_symbols: 是否包含特殊符号
        custom_chars: 自定义字符集

    Returns:
        随机字符串
    """
    if custom_chars:
        chars = custom_chars
    else:
        chars = ""
        if include_lowercase:
            chars += string.ascii_lowercase
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_numbers:
            chars += string.digits
        if include_symbols:
            chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"

    if not chars:
        raise ValueError("至少需要选择一种字符类型")

    return ''.join(secrets.choice(chars) for _ in range(length))

