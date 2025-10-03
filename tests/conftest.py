"""
Pytest配置文件

这个文件包含测试的全局配置和fixture。
"""

import pytest
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# TODO: 添加全局测试fixture
#
# @pytest.fixture
# def sample_data():
#     """提供测试数据"""
#     return {"test": "data"}
