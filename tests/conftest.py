"""
Pytest配置文件

这个文件包含测试的全局配置和fixture。
"""

import pytest
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture
def sample_python_code():
    """示例 Python 代码"""
    return """def hello_world():
print("Hello, World!")
if True:
print("This is true")
return "done"
"""

@pytest.fixture
def sample_javascript_code():
    """示例 JavaScript 代码"""
    return """function helloWorld() {
console.log("Hello, World!");
if (true) {
console.log("This is true");
}
return "done";
}
"""
