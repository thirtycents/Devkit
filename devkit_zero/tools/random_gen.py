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


def generate_random_hex_color() -> str:
    """
    生成随机十六进制颜色代码

    Returns:
        颜色代码 (如 #FF5733)
    """
    return f"#{random.randint(0, 0xFFFFFF):06X}"


def register_parser(subparsers):
    """注册 random-gen 命令的参数解析器"""
    parser = subparsers.add_parser('random', help='随机数据生成工具')

    subcommands = parser.add_subparsers(dest='type', help='生成类型')

    # UUID 生成
    uuid_parser = subcommands.add_parser('uuid', help='生成 UUID')
    uuid_parser.add_argument('--version', '-v', type=int, choices=[1, 4], default=4,
                             help='UUID 版本 (默认: 4)')

    # 随机字符串生成
    string_parser = subcommands.add_parser('string', help='生成随机字符串')
    string_parser.add_argument('--length', '-l', type=int, default=8, help='字符串长度 (默认: 8)')
    string_parser.add_argument('--no-numbers', action='store_true', help='不包含数字')
    string_parser.add_argument('--no-uppercase', action='store_true', help='不包含大写字母')
    string_parser.add_argument('--no-lowercase', action='store_true', help='不包含小写字母')
    string_parser.add_argument('--symbols', action='store_true', help='包含特殊符号')
    string_parser.add_argument('--custom', help='自定义字符集')

    # 安全密码生成
    password_parser = subcommands.add_parser('password', help='生成安全密码')
    password_parser.add_argument('--length', '-l', type=int, default=16, help='密码长度 (默认: 16)')

    # 随机数生成
    number_parser = subcommands.add_parser('number', help='生成随机数')
    number_parser.add_argument('--min', type=int, default=0, help='最小值 (默认: 0)')
    number_parser.add_argument('--max', type=int, default=100, help='最大值 (默认: 100)')
    number_parser.add_argument('--float', action='store_true', help='生成浮点数')
    number_parser.add_argument('--precision', type=int, default=2, help='浮点数精度 (默认: 2)')

    # 颜色代码生成
    color_parser = subcommands.add_parser('color', help='生成随机颜色代码')

    parser.set_defaults(func=main)


def main(args):
    """random-gen 工具的主函数"""
    try:
        if args.type == 'uuid':
            return generate_uuid(args.version)

        elif args.type == 'string':
            return generate_random_string(
                length=args.length,
                include_numbers=not args.no_numbers,
                include_uppercase=not args.no_uppercase,
                include_lowercase=not args.no_lowercase,
                include_symbols=args.symbols,
                custom_chars=args.custom
            )

        elif args.type == 'password':
            return generate_secure_password(args.length)

        elif args.type == 'number':
            if args.float:
                min_val = float(args.min)
                max_val = float(args.max)
                return str(generate_random_float(min_val, max_val, args.precision))
            else:
                return str(generate_random_number(args.min, args.max))

        elif args.type == 'color':
            return generate_random_hex_color()

        else:
            raise ValueError("请选择生成类型: uuid, string, password, number, color")

    except Exception as e:
        raise RuntimeError(f"生成失败: {e}")


if __name__ == "__main__":
    # 用于独立测试
    print("UUID:", generate_uuid())
    print("随机字符串:", generate_random_string(12))
    print("安全密码:", generate_secure_password(16))
    print("随机数:", generate_random_number(1, 100))
    print("颜色代码:", generate_random_hex_color())