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


def generate_secure_password(length: int = 16) -> str:
    """
    生成安全密码

    Args:
        length: 密码长度

    Returns:
        安全密码字符串
    """
    if length < 8:
        raise ValueError("密码长度至少为 8 位")

    # 确保密码包含所有字符类型
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"

    # 至少包含一个每种类型的字符
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*()-_=+")
    ]

    # 填充剩余长度
    for _ in range(length - 4):
        password.append(secrets.choice(chars))

    # 打乱顺序
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)


def generate_random_number(min_val: int = 0, max_val: int = 100) -> int:
    """
    生成随机整数

    Args:
        min_val: 最小值
        max_val: 最大值

    Returns:
        随机整数
    """
    return secrets.randbelow(max_val - min_val + 1) + min_val


def generate_random_float(min_val: float = 0.0, max_val: float = 1.0, precision: int = 2) -> float:
    """
    生成随机浮点数

    Args:
        min_val: 最小值
        max_val: 最大值
        precision: 小数位数

    Returns:
        随机浮点数
    """
    random_float = random.uniform(min_val, max_val)
    return round(random_float, precision)

