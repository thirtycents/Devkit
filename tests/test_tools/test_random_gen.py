"""
测试随机数据生成工具
"""

import unittest
import re
from devkit_zero.tools import random_gen


class TestRandomGen(unittest.TestCase):
    """随机数据生成工具测试类"""
    
    def test_generate_uuid(self):
        """测试 UUID 生成"""
        # 测试 UUID4
        uuid4 = random_gen.generate_uuid(4)
        self.assertIsInstance(uuid4, str)
        self.assertEqual(len(uuid4), 36)  # UUID 标准长度
        self.assertRegex(uuid4, r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')
        
        # 测试 UUID1
        uuid1 = random_gen.generate_uuid(1)
        self.assertIsInstance(uuid1, str)
        self.assertEqual(len(uuid1), 36)

    def test_generate_uuid_invalid_version(self):
        """测试无效 UUID 版本"""
        with self.assertRaises(ValueError):
            random_gen.generate_uuid(5)

    def test_generate_random_string_default(self):
        """测试默认随机字符串生成"""
        result = random_gen.generate_random_string()
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 8)  # 默认长度
        
    def test_generate_random_string_custom_length(self):
        """测试自定义长度随机字符串"""
        length = 16
        result = random_gen.generate_random_string(length=length)
        self.assertEqual(len(result), length)
        
    def test_generate_random_string_only_numbers(self):
        """测试只包含数字的随机字符串"""
        result = random_gen.generate_random_string(
            length=10,
            include_numbers=True,
            include_uppercase=False,
            include_lowercase=False,
            include_symbols=False
        )
        self.assertTrue(result.isdigit())
        
    def test_generate_random_string_no_characters(self):
        """测试没有字符类型的情况"""
        with self.assertRaises(ValueError):
            random_gen.generate_random_string(
                include_numbers=False,
                include_uppercase=False,
                include_lowercase=False,
                include_symbols=False
            )

    def test_generate_secure_password(self):
        """测试安全密码生成"""
        password = random_gen.generate_secure_password(16)
        self.assertIsInstance(password, str)
        self.assertEqual(len(password), 16)
        
        # 检查是否包含各种字符类型
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in "!@#$%^&*()-_=+" for c in password)
        
        self.assertTrue(has_lower, "密码应包含小写字母")
        self.assertTrue(has_upper, "密码应包含大写字母")
        self.assertTrue(has_digit, "密码应包含数字")
        self.assertTrue(has_symbol, "密码应包含特殊符号")

    def test_generate_secure_password_short(self):
        """测试短密码长度限制"""
        with self.assertRaises(ValueError):
            random_gen.generate_secure_password(7)

    def test_generate_random_number(self):
        """测试随机整数生成"""
        min_val, max_val = 10, 20
        result = random_gen.generate_random_number(min_val, max_val)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, min_val)
        self.assertLessEqual(result, max_val)

    def test_generate_random_float(self):
        """测试随机浮点数生成"""
        min_val, max_val = 1.0, 2.0
        result = random_gen.generate_random_float(min_val, max_val, precision=2)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, min_val)
        self.assertLessEqual(result, max_val)

    def test_generate_random_hex_color(self):
        """测试随机十六进制颜色生成"""
        color = random_gen.generate_random_hex_color()
        self.assertIsInstance(color, str)
        self.assertTrue(color.startswith('#'))
        self.assertEqual(len(color), 7)  # #RRGGBB 格式
        self.assertRegex(color, r'^#[0-9A-F]{6}$')

    def test_multiple_generations_different(self):
        """测试多次生成结果不同"""
        results = [random_gen.generate_uuid() for _ in range(10)]
        unique_results = set(results)
        self.assertEqual(len(unique_results), len(results), "生成的 UUID 应该都不相同")


if __name__ == '__main__':
    unittest.main()