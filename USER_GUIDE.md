# DevKit-Zero 使用指南 | DevKit-Zero User Guide

> 🎯 **一个轻量级、零依赖的开发者工具箱**  
> 🎯 **A Lightweight, Zero-Dependency Developer Toolkit**

[![Python Support](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📖 目录 | Table of Contents

- [快速开始 | Quick Start](#快速开始--quick-start)
- [安装方法 | Installation](#安装方法--installation)
- [三种使用方式 | Three Usage Methods](#三种使用方式--three-usage-methods)
- [工具详解 | Tool Reference](#工具详解--tool-reference)
- [CLI 命令参考 | CLI Command Reference](#cli-命令参考--cli-command-reference)
- [包导入使用 | Package Import Usage](#包导入使用--package-import-usage)
- [GUI 使用指南 | GUI User Guide](#gui-使用指南--gui-user-guide)
- [常见问题 | FAQ](#常见问题--faq)
- [高级用法 | Advanced Usage](#高级用法--advanced-usage)

---

## 🚀 快速开始 | Quick Start

### 中文版

DevKit-Zero 是一个功能强大的开发者工具箱，提供 10 个实用工具，支持 GUI、CLI 和 Python 包导入三种使用方式。

**核心特性：**
- ✅ **零依赖** - 仅使用 Python 标准库
- ✅ **三种用法** - GUI 界面、命令行、Python 导入
- ✅ **10 个工具** - 代码格式化、正则测试、端口检查等
- ✅ **跨平台** - Windows、Linux、macOS 全支持

### English Version

DevKit-Zero is a powerful developer toolkit that provides 10 practical tools, supporting GUI, CLI, and Python package import usage methods.

**Core Features:**
- ✅ **Zero Dependencies** - Uses only Python standard library
- ✅ **Three Methods** - GUI interface, command line, Python import
- ✅ **10 Tools** - Code formatting, regex testing, port checking, etc.
- ✅ **Cross-Platform** - Full support for Windows, Linux, macOS

---

## 💾 安装方法 | Installation

### 方法 1: 从源码安装 | Method 1: Install from Source

```bash
# 克隆仓库 | Clone repository
git clone https://github.com/thirtycents/Devkit.git
cd Devkit

# 创建虚拟环境（可选）| Create virtual environment (optional)
python -m venv venv

# Windows 激活 | Windows activation
venv\Scripts\activate

# Linux/Mac 激活 | Linux/Mac activation
source venv/bin/activate

# 安装开发模式 | Install in development mode
pip install -e .
```

### 方法 2: 直接使用（无需安装）| Method 2: Direct Use (No Installation)

```bash
# 克隆仓库 | Clone repository
git clone https://github.com/thirtycents/Devkit.git
cd Devkit

# 直接运行 | Run directly
python -m devkit_zero.gui_main
```

---

## 🎨 三种使用方式 | Three Usage Methods

### 1. 🖥️ GUI 图形界面 | GUI Interface

#### 中文说明
GUI 提供直观的图形界面，适合不熟悉命令行的用户。

**启动方法：**

```bash
# Windows 用户 - 双击启动脚本
start_gui.bat

# 或使用命令行启动
python -m devkit_zero.gui_main

# 或直接运行 GUI 应用
python -m devkit_zero.ui.gui_app
```

**特点：**
- ✅ 友好的图形界面
- ✅ 实时结果预览
- ✅ 无需记忆命令
- ✅ 支持文件拖放（部分工具）

#### English Description
GUI provides an intuitive graphical interface, suitable for users unfamiliar with command line.

**Launch Methods:**

```bash
# Windows users - Double-click startup script
start_gui.bat

# Or launch via command line
python -m devkit_zero.gui_main

# Or run GUI app directly
python -m devkit_zero.ui.gui_app
```

**Features:**
- ✅ Friendly graphical interface
- ✅ Real-time result preview
- ✅ No need to memorize commands
- ✅ Supports file drag & drop (some tools)

---

### 2. ⌨️ CLI 命令行 | CLI Command Line

#### 中文说明
CLI 适合自动化脚本和批处理任务，可与其他命令行工具集成。

**基本语法：**

```bash
python -m devkit_zero.cli <命令> [选项]
```

**查看帮助：**

```bash
# 查看所有可用命令
python -m devkit_zero.cli --help

# 查看特定命令的帮助
python -m devkit_zero.cli format --help
python -m devkit_zero.cli diff --help
```

**快速示例：**

```bash
# 格式化代码
python -m devkit_zero.cli format --file test.py

# 比较文本
python -m devkit_zero.cli diff --text1 "hello" --text2 "world"

# 测试正则表达式
python -m devkit_zero.cli regex "\d+" "Hello 123 World"

# 生成 UUID
python -m devkit_zero.cli random uuid

# 检查端口
python -m devkit_zero.cli port --port 8080
```

#### English Description
CLI is suitable for automation scripts and batch tasks, can integrate with other command-line tools.

**Basic Syntax:**

```bash
python -m devkit_zero.cli <command> [options]
```

**View Help:**

```bash
# View all available commands
python -m devkit_zero.cli --help

# View help for specific command
python -m devkit_zero.cli format --help
python -m devkit_zero.cli diff --help
```

**Quick Examples:**

```bash
# Format code
python -m devkit_zero.cli format --file test.py

# Compare text
python -m devkit_zero.cli diff --text1 "hello" --text2 "world"

# Test regular expression
python -m devkit_zero.cli regex "\d+" "Hello 123 World"

# Generate UUID
python -m devkit_zero.cli random uuid

# Check port
python -m devkit_zero.cli port --port 8080
```

---

### 3. 📦 Python 包导入 | Package Import

#### 中文说明
作为 Python 包导入，适合在自己的 Python 项目中集成这些工具。

**基本导入：**

```python
# 导入单个工具
from devkit_zero import formatter, diff_tool, regex_tester

# 导入多个工具
from devkit_zero import (
    formatter,
    random_gen,
    diff_tool,
    converter,
    linter
)

# 查看可用工具
import devkit_zero
print(devkit_zero.get_available_tools())
```

**使用示例：**

```python
from devkit_zero import formatter, diff_tool, regex_tester

# 1. 格式化代码
code = """
def hello():
print("world")
"""
formatted_code, error = formatter.format_code(code, 'python', ignore_errors=True)
print(formatted_code)

# 2. 比较文本差异
result = diff_tool.diff_text("Hello World", "Hello Python")
print(f"相似度: {result['similarity_percent']}")
print(result['diff'])

# 3. 测试正则表达式
tester = regex_tester.RegexTester()
result = tester.test_pattern(r'\d+', 'Order 123 and 456')
print(f"找到 {result['match_count']} 个匹配")
for match in result['matches']:
    print(f"  - {match['group']} at position {match['start']}")
```

#### English Description
Import as a Python package, suitable for integrating these tools into your own Python projects.

**Basic Import:**

```python
# Import single tool
from devkit_zero import formatter, diff_tool, regex_tester

# Import multiple tools
from devkit_zero import (
    formatter,
    random_gen,
    diff_tool,
    converter,
    linter
)

# View available tools
import devkit_zero
print(devkit_zero.get_available_tools())
```

**Usage Examples:**

```python
from devkit_zero import formatter, diff_tool, regex_tester

# 1. Format code
code = """
def hello():
print("world")
"""
formatted_code, error = formatter.format_code(code, 'python', ignore_errors=True)
print(formatted_code)

# 2. Compare text differences
result = diff_tool.diff_text("Hello World", "Hello Python")
print(f"Similarity: {result['similarity_percent']}")
print(result['diff'])

# 3. Test regular expression
tester = regex_tester.RegexTester()
result = tester.test_pattern(r'\d+', 'Order 123 and 456')
print(f"Found {result['match_count']} matches")
for match in result['matches']:
    print(f"  - {match['group']} at position {match['start']}")
```

---

## 🛠️ 工具详解 | Tool Reference

### 1. 📝 代码格式化工具 | Code Formatter

#### 功能说明 | Description

**中文：** 自动格式化 Python 和 JavaScript 代码，改善代码可读性，支持错误容忍模式。

**English:** Automatically format Python and JavaScript code to improve readability, supports error-tolerant mode.

#### CLI 使用 | CLI Usage

```bash
# 格式化文件 | Format file
python -m devkit_zero.cli format --file test.py

# 格式化代码字符串 | Format code string
python -m devkit_zero.cli format --input "def test():pass" --language python

# 直接修改原文件 | Modify file in-place
python -m devkit_zero.cli format --file test.py --in-place

# 保存到新文件 | Save to new file
python -m devkit_zero.cli format --file test.py --output formatted.py

# 忽略语法错误继续格式化 | Ignore syntax errors and format anyway
python -m devkit_zero.cli format --file test.py --ignore-errors

# JavaScript 格式化 | JavaScript formatting
python -m devkit_zero.cli format --file script.js --language javascript
```

#### 包导入使用 | Package Import Usage

```python
from devkit_zero import formatter

# 格式化 Python 代码 | Format Python code
code = "def hello():print('hi')"
formatted, error = formatter.format_code(code, 'python')

if error:
    print(f"警告 | Warning: {error}")
print(formatted)

# 格式化文件 | Format file
formatted, error = formatter.format_file('test.py', ignore_errors=True)

# 格式化 JavaScript | Format JavaScript
js_code = "function test(){console.log('hello');}"
formatted, error = formatter.format_code(js_code, 'javascript')
```

#### 参数说明 | Parameters

| 参数 | Parameter | 说明 | Description |
|------|-----------|------|-------------|
| `--file, -f` | | 文件路径 | File path |
| `--input, -i` | | 代码字符串 | Code string |
| `--language, -l` | | 语言类型 | Language type |
| `--output, -o` | | 输出文件 | Output file |
| `--in-place` | | 直接修改原文件 | Modify file in-place |
| `--ignore-errors` | | 忽略语法错误 | Ignore syntax errors |

---

### 2. 🎲 随机数据生成器 | Random Data Generator

#### 功能说明 | Description

**中文：** 生成各种随机数据，包括 UUID、密码、随机数、字符串等。

**English:** Generate various random data including UUID, passwords, random numbers, strings, etc.

#### CLI 使用 | CLI Usage

```bash
# 生成 UUID | Generate UUID
python -m devkit_zero.cli random uuid

# 生成密码 | Generate password
python -m devkit_zero.cli random password --length 16

# 生成随机数 | Generate random number
python -m devkit_zero.cli random number --min 1 --max 100

# 生成随机字符串 | Generate random string
python -m devkit_zero.cli random string --length 20

# 生成十六进制字符串 | Generate hex string
python -m devkit_zero.cli random hex --length 32
```

#### 包导入使用 | Package Import Usage

```python
from devkit_zero import random_gen

# 生成 UUID | Generate UUID
uuid = random_gen.generate_uuid()
print(f"UUID: {uuid}")

# 生成安全密码 | Generate secure password
password = random_gen.generate_secure_password(length=16)
print(f"密码 | Password: {password}")

# 生成随机整数 | Generate random integer
number = random_gen.generate_random_number(1, 100)
print(f"随机数 | Random number: {number}")

# 生成随机字符串 | Generate random string
string = random_gen.generate_random_string(20)
print(f"字符串 | String: {string}")
```

---

### 3. 🔍 文本差异对比工具 | Text Diff Tool

#### 功能说明 | Description

**中文：** 比较两个文本或文件的差异，显示详细的差异报告和相似度。

**English:** Compare differences between two texts or files, showing detailed diff report and similarity.

#### CLI 使用 | CLI Usage

```bash
# 比较文本 | Compare texts
python -m devkit_zero.cli diff --text1 "Hello World" --text2 "Hello Python"

# 比较文件 | Compare files
python -m devkit_zero.cli diff --file1 old.txt --file2 new.txt

# 指定上下文行数 | Specify context lines
python -m devkit_zero.cli diff --file1 old.txt --file2 new.txt --context 5
```

#### 包导入使用 | Package Import Usage

```python
from devkit_zero import diff_tool

# 比较文本 | Compare texts
result = diff_tool.diff_text("Hello World", "Hello Python")
print(f"相似度 | Similarity: {result['similarity_percent']}")
print(result['diff'])

# 比较文件 | Compare files
diff = diff_tool.compare_files('file1.txt', 'file2.txt')
print(diff)

# 计算相似度 | Calculate similarity
similarity = diff_tool.get_similarity("text1", "text2")
print(f"相似度 | Similarity: {similarity * 100:.2f}%")
```

---

### 4. 🔄 数据格式转换器 | Data Format Converter

#### 功能说明 | Description

**中文：** 在 JSON、CSV、YAML 等数据格式之间进行转换。

**English:** Convert between data formats like JSON, CSV, YAML, etc.

#### CLI 使用 | CLI Usage

```bash
# JSON 转 CSV | JSON to CSV
python -m devkit_zero.cli convert --input data.json --output data.csv --from json --to csv

# CSV 转 JSON | CSV to JSON
python -m devkit_zero.cli convert --input data.csv --output data.json --from csv --to json

# 字符串转换 | String conversion
python -m devkit_zero.cli convert --data '{"name":"test"}' --from json --to yaml
```

#### 包导入使用 | Package Import Usage

```python
from devkit_zero import converter

# JSON 转 CSV | JSON to CSV
result = converter.json_to_csv('[{"name":"John","age":30}]')
print(result)

# CSV 转 JSON | CSV to JSON
csv_data = "name,age\nJohn,30\nJane,25"
result = converter.csv_to_json(csv_data)
print(result)

# 字典转 JSON | Dict to JSON
data = {"name": "test", "value": 123}
json_str = converter.dict_to_json(data)
```

---

### 5. 🔍 代码静态检查工具 | Code Linter

#### 功能说明 | Description

**中文：** 检查 Python 代码的语法错误、代码风格问题和潜在 bug。

**English:** Check Python code for syntax errors, style issues, and potential bugs.

#### CLI 使用 | CLI Usage

```bash
# 检查代码字符串 | Check code string
python -m devkit_zero.cli lint --code "def test():pass"

# 检查文件 | Check file
python -m devkit_zero.cli lint --file test.py

# 详细输出 | Verbose output
python -m devkit_zero.cli lint --file test.py --verbose
```

#### 包导入使用 | Package Import Usage

```python
from devkit_zero import linter

# 检查代码 | Check code
code = """
def hello():
    x = 1
    return x
"""
issues = linter.check_code(code)

for issue in issues:
    print(f"{issue['type']}: {issue['message']} (行 | line {issue['line']})")
```

---

### 6. 🎯 正则表达式测试器 | Regex Tester

#### 功能说明 | Description

**中文：** 测试正则表达式模式，查看匹配结果，支持多种正则标志。

**English:** Test regular expression patterns, view match results, supports multiple regex flags.

#### CLI 使用 | CLI Usage

```bash
# 基本测试 | Basic test
python -m devkit_zero.cli regex "\d+" "Hello 123 World 456"

# 忽略大小写 | Ignore case
python -m devkit_zero.cli regex "[a-z]+" "Hello World" --ignorecase

# 多行模式 | Multiline mode
python -m devkit_zero.cli regex "^test" "line1\ntest" --multiline

# 显示替换预览 | Show replacement preview
python -m devkit_zero.cli regex "\d+" "Hello 123" --show-replacement
```

#### 包导入使用 | Package Import Usage

```python
from devkit_zero import regex_tester
import re

# 创建测试器实例 | Create tester instance
tester = regex_tester.RegexTester()

# 测试模式 | Test pattern
result = tester.test_pattern(
    pattern=r'\d+',
    text='Order 123 and 456',
    flags=re.IGNORECASE
)

print(f"匹配数量 | Match count: {result['match_count']}")
for match in result['matches']:
    print(f"  内容 | Content: {match['group']}")
    print(f"  位置 | Position: {match['start']}-{match['end']}")

# 获取常用模式 | Get common patterns
patterns = tester.get_common_patterns()
print(f"Email 模式 | Email pattern: {patterns['Email']}")
```

---

### 7. 🔌 端口检查工具 | Port Checker

#### 功能说明 | Description

**中文：** 检查指定端口是否被占用，显示占用进程信息。

**English:** Check if specified port is in use, show process information.

#### CLI 使用 | CLI Usage

```bash
# 检查单个端口 | Check single port
python -m devkit_zero.cli port --port 8080

# 检查端口范围 | Check port range
python -m devkit_zero.cli port --start 8000 --end 9000

# 仅显示占用的端口 | Show only used ports
python -m devkit_zero.cli port --start 8000 --end 8100 --show-used
```

#### 包导入使用 | Package Import Usage

```python
from devkit_zero import port_checker

# 检查端口是否可用 | Check if port is available
if port_checker.is_port_available(8080):
    print("端口 8080 可用 | Port 8080 is available")
else:
    print("端口 8080 已被占用 | Port 8080 is in use")

# 查找可用端口 | Find available port
port = port_checker.find_available_port(8000, 9000)
print(f"找到可用端口 | Found available port: {port}")

# 获取端口信息 | Get port information
info = port_checker.get_port_info(8080)
if info:
    print(f"进程 | Process: {info['process']}")
    print(f"PID: {info['pid']}")
```

---

### 8. 🧹 未使用函数检测器 | Unused Function Detector

#### 功能说明 | Description

**中文：** 扫描 Python 项目，查找未被调用的函数和方法。

**English:** Scan Python projects to find uncalled functions and methods.

#### CLI 使用 | CLI Usage

```bash
# 扫描单个文件 | Scan single file
python -m devkit_zero.cli unused-func --file test.py

# 扫描整个目录 | Scan entire directory
python -m devkit_zero.cli unused-func --directory ./src

# 排除测试文件 | Exclude test files
python -m devkit_zero.cli unused-func --directory ./src --exclude-pattern "test_*.py"
```

#### 包导入使用 | Package Import Usage

```python
from devkit_zero import unused_func_detector

# 检测未使用的函数 | Detect unused functions
unused = unused_func_detector.find_unused_functions('./src')

for func in unused:
    print(f"未使用 | Unused: {func['name']} in {func['file']}")
    print(f"  行号 | Line: {func['line']}")
```

---

### 9. 📊 API 契约对比器 | API Contract Diff

#### 功能说明 | Description

**中文：** 比较 API 接口的变化，检测不兼容的修改。

**English:** Compare API interface changes, detect incompatible modifications.

#### CLI 使用 | CLI Usage

```bash
# 比较 API 定义 | Compare API definitions
python -m devkit_zero.cli api-diff --old api_v1.json --new api_v2.json

# 输出 JSON 格式 | Output JSON format
python -m devkit_zero.cli api-diff --old api_v1.json --new api_v2.json --format json
```

#### 包导入使用 | Package Import Usage

```python
from devkit_zero import api_contract_diff

# 比较 API | Compare APIs
old_api = {"endpoints": ["/api/users"]}
new_api = {"endpoints": ["/api/users", "/api/posts"]}

diff = api_contract_diff.compare_apis(old_api, new_api)
print(f"新增接口 | New endpoints: {diff['added']}")
print(f"删除接口 | Removed endpoints: {diff['removed']}")
print(f"修改接口 | Modified endpoints: {diff['modified']}")
```

---

### 10. 🤖 Robots.txt 检查器 | Robots Checker

#### 功能说明 | Description

**中文：** 检查网站的 robots.txt 文件，解析爬虫规则。

**English:** Check website's robots.txt file, parse crawler rules.

#### CLI 使用 | CLI Usage

```bash
# 检查网站 | Check website
python -m devkit_zero.cli robots_checker https://www.google.com

# 显示原始内容 | Show raw content
python -m devkit_zero.cli robots_checker https://www.google.com --raw

# 设置超时 | Set timeout
python -m devkit_zero.cli robots_checker https://www.google.com --timeout 30
```

#### 包导入使用 | Package Import Usage

```python
from devkit_zero.tools.Robot_checker import core_logic

# 检查 robots.txt | Check robots.txt
result = core_logic('https://www.google.com')
print(result)

# 解析规则 | Parse rules
from devkit_zero.tools.Robot_checker import parse_robots_txt
rules = parse_robots_txt(robots_content)
```

---

## 🎯 CLI 命令参考 | CLI Command Reference

### 完整命令列表 | Complete Command List

```bash
# 查看所有命令 | View all commands
python -m devkit_zero.cli --help

# 查看版本 | View version
python -m devkit_zero.cli --version
```

### 命令对照表 | Command Reference Table

| 命令 | Command | 功能 | Function | 示例 | Example |
|------|---------|------|----------|------|---------|
| `format` | | 代码格式化 | Code formatting | `format --file test.py` |
| `random` | | 随机数据生成 | Random data generation | `random uuid` |
| `diff` | | 文本差异对比 | Text difference | `diff --text1 "a" --text2 "b"` |
| `convert` | | 格式转换 | Format conversion | `convert --from json --to csv` |
| `lint` | | 代码检查 | Code linting | `lint --file test.py` |
| `regex` | | 正则测试 | Regex testing | `regex "\d+" "test 123"` |
| `port` | | 端口检查 | Port checking | `port --port 8080` |
| `unused-func` | | 未使用函数检测 | Unused function detection | `unused-func --directory ./src` |
| `api-diff` | | API 对比 | API comparison | `api-diff --old v1 --new v2` |
| `robots_checker` | | Robots 检查 | Robots checking | `robots_checker https://site.com` |

---

## 📚 包导入使用 | Package Import Usage

### 基本导入模式 | Basic Import Patterns

```python
# 方式 1: 导入单个工具 | Method 1: Import single tool
from devkit_zero import formatter
code, err = formatter.format_code("code", "python")

# 方式 2: 导入多个工具 | Method 2: Import multiple tools
from devkit_zero import formatter, diff_tool, regex_tester

# 方式 3: 导入全部 | Method 3: Import all
import devkit_zero
tools = devkit_zero.get_available_tools()

# 方式 4: 从子模块导入 | Method 4: Import from submodule
from devkit_zero.tools import formatter
from devkit_zero.tools.Robot_checker import core_logic
```

### 完整示例程序 | Complete Example Program

```python
#!/usr/bin/env python3
"""
DevKit-Zero 综合示例程序
DevKit-Zero Comprehensive Example Program
"""

from devkit_zero import (
    formatter,
    random_gen,
    diff_tool,
    regex_tester,
    port_checker
)

def main():
    print("=" * 60)
    print("DevKit-Zero 示例程序 | Example Program")
    print("=" * 60)
    
    # 1. 代码格式化 | Code formatting
    print("\n1. 代码格式化 | Code Formatting")
    code = "def test():print('hello')"
    formatted, error = formatter.format_code(code, 'python')
    print(f"原始 | Original: {code}")
    print(f"格式化 | Formatted:\n{formatted}")
    
    # 2. 生成随机数据 | Generate random data
    print("\n2. 随机数据生成 | Random Data Generation")
    uuid = random_gen.generate_uuid()
    password = random_gen.generate_secure_password(12)
    print(f"UUID: {uuid}")
    print(f"密码 | Password: {password}")
    
    # 3. 文本对比 | Text comparison
    print("\n3. 文本差异对比 | Text Difference")
    result = diff_tool.diff_text("Hello World", "Hello Python")
    print(f"相似度 | Similarity: {result['similarity_percent']}")
    
    # 4. 正则测试 | Regex testing
    print("\n4. 正则表达式测试 | Regex Testing")
    tester = regex_tester.RegexTester()
    result = tester.test_pattern(r'\d+', 'Order 123 and 456')
    print(f"找到 | Found {result['match_count']} 个匹配 | matches")
    
    # 5. 端口检查 | Port checking
    print("\n5. 端口检查 | Port Checking")
    if port_checker.is_port_available(8080):
        print("✓ 端口 8080 可用 | Port 8080 is available")
    else:
        print("✗ 端口 8080 已占用 | Port 8080 is in use")
    
    print("\n" + "=" * 60)
    print("示例程序结束 | Example Program End")
    print("=" * 60)

if __name__ == "__main__":
    main()
```

---

## 🖼️ GUI 使用指南 | GUI User Guide

### 启动 GUI | Launch GUI

**Windows:**
```bash
# 双击启动 | Double-click to launch
start_gui.bat

# 或命令行启动 | Or launch via command line
python -m devkit_zero.gui_main
```

**Linux/Mac:**
```bash
# 运行启动脚本 | Run startup script
chmod +x start_gui.sh
./start_gui.sh

# 或直接运行 | Or run directly
python3 -m devkit_zero.gui_main
```

### GUI 界面说明 | GUI Interface Guide

#### 主界面布局 | Main Interface Layout

```
┌─────────────────────────────────────────────────────────┐
│  DevKit-Zero - 零依赖开发者工具箱                         │
├─────────────────────────────────────────────────────────┤
│  [工具选择栏 | Tool Selection Bar]                       │
│  ○ 格式化 ○ 随机 ○ 差异 ○ 转换 ... ○ Robots            │
├───────────────────┬─────────────────────────────────────┤
│  控制面板          │  结果输出                             │
│  Control Panel    │  Result Output                       │
│                   │                                      │
│  [输入区域]        │  [输出区域]                          │
│  [Input Area]     │  [Output Area]                       │
│                   │                                      │
│  [选项设置]        │  [显示结果]                          │
│  [Options]        │  [Show Results]                      │
│                   │                                      │
│  [执行按钮]        │                                      │
│  [Execute Button] │                                      │
└───────────────────┴─────────────────────────────────────┘
```

### 使用步骤 | Usage Steps

1. **选择工具 | Select Tool**
   - 点击顶部工具选择栏中的工具
   - Click on tool in top selection bar

2. **输入数据 | Input Data**
   - 在左侧控制面板输入数据或选择文件
   - Input data or select files in left control panel

3. **设置选项 | Set Options**
   - 配置工具特定的选项
   - Configure tool-specific options

4. **执行操作 | Execute Operation**
   - 点击执行按钮运行工具
   - Click execute button to run tool

5. **查看结果 | View Results**
   - 在右侧结果面板查看输出
   - View output in right result panel

---

## ❓ 常见问题 | FAQ

### Q1: 如何在不同 Python 版本中使用？ | How to use with different Python versions?

**中文答案：**
DevKit-Zero 支持 Python 3.7+。如果系统有多个 Python 版本，使用完整路径指定：

```bash
# Windows
C:\Python39\python.exe -m devkit_zero.gui_main

# Linux/Mac
python3.9 -m devkit_zero.gui_main
```

**English Answer:**
DevKit-Zero supports Python 3.7+. If your system has multiple Python versions, specify the full path:

```bash
# Windows
C:\Python39\python.exe -m devkit_zero.gui_main

# Linux/Mac
python3.9 -m devkit_zero.gui_main
```

---

### Q2: CLI 命令太长怎么办？ | CLI commands are too long?

**中文答案：**
可以创建别名（alias）或批处理脚本：

**Windows (批处理文件):**
```batch
@echo off
python -m devkit_zero.cli %*
```
保存为 `devkit.bat` 并添加到 PATH，然后使用：
```bash
devkit format --file test.py
```

**Linux/Mac (bash 别名):**
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
alias devkit='python3 -m devkit_zero.cli'

# 使用
devkit format --file test.py
```

**English Answer:**
You can create aliases or batch scripts:

**Windows (Batch file):**
```batch
@echo off
python -m devkit_zero.cli %*
```
Save as `devkit.bat` and add to PATH, then use:
```bash
devkit format --file test.py
```

**Linux/Mac (bash alias):**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias devkit='python3 -m devkit_zero.cli'

# Usage
devkit format --file test.py
```

---

### Q3: 如何在脚本中使用？ | How to use in scripts?

**中文答案：**
作为 Python 包导入是最佳方式：

```python
#!/usr/bin/env python3
import sys
from devkit_zero import formatter

# 格式化所有参数中的 Python 文件
for file_path in sys.argv[1:]:
    if file_path.endswith('.py'):
        code, err = formatter.format_file(file_path, ignore_errors=True)
        if err:
            print(f"警告: {file_path} - {err}", file=sys.stderr)
        with open(file_path, 'w') as f:
            f.write(code)
        print(f"✓ 格式化完成: {file_path}")
```

**English Answer:**
Importing as a Python package is the best approach:

```python
#!/usr/bin/env python3
import sys
from devkit_zero import formatter

# Format all Python files in arguments
for file_path in sys.argv[1:]:
    if file_path.endswith('.py'):
        code, err = formatter.format_file(file_path, ignore_errors=True)
        if err:
            print(f"Warning: {file_path} - {err}", file=sys.stderr)
        with open(file_path, 'w') as f:
            f.write(code)
        print(f"✓ Formatted: {file_path}")
```

---

### Q4: GUI 启动失败怎么办？ | What if GUI fails to launch?

**中文答案：**
1. 检查是否安装了 tkinter：
```bash
python -c "import tkinter"
```

2. Ubuntu/Debian 系统安装 tkinter：
```bash
sudo apt-get install python3-tk
```

3. 检查错误信息：
```bash
python -m devkit_zero.gui_main 2>&1
```

**English Answer:**
1. Check if tkinter is installed:
```bash
python -c "import tkinter"
```

2. Install tkinter on Ubuntu/Debian:
```bash
sudo apt-get install python3-tk
```

3. Check error messages:
```bash
python -m devkit_zero.gui_main 2>&1
```

---

### Q5: 如何贡献代码？ | How to contribute?

**中文答案：**
1. Fork 仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -am 'Add some feature'`
4. 推送到分支：`git push origin feature/your-feature`
5. 创建 Pull Request

**English Answer:**
1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add some feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Create Pull Request

---

## 🚀 高级用法 | Advanced Usage

### 批处理自动化 | Batch Automation

**中文示例：批量格式化项目中的所有 Python 文件**

```python
#!/usr/bin/env python3
"""
批量格式化脚本
Batch formatting script
"""
import os
from pathlib import Path
from devkit_zero import formatter

def format_project(project_path):
    """格式化项目中的所有 Python 文件"""
    python_files = Path(project_path).rglob('*.py')
    
    success_count = 0
    error_count = 0
    
    for file_path in python_files:
        try:
            code, err = formatter.format_file(str(file_path), ignore_errors=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            
            if err:
                print(f"⚠️  {file_path}: {err}")
            else:
                print(f"✓ {file_path}")
            success_count += 1
        except Exception as e:
            print(f"✗ {file_path}: {e}")
            error_count += 1
    
    print(f"\n总结: {success_count} 成功, {error_count} 失败")
    print(f"Summary: {success_count} success, {error_count} failed")

if __name__ == "__main__":
    import sys
    project_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    format_project(project_path)
```

### 集成到 CI/CD | CI/CD Integration

**GitHub Actions 示例：**

```yaml
name: Code Quality Check

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install DevKit-Zero
        run: |
          git clone https://github.com/thirtycents/Devkit.git
          cd Devkit
          pip install -e .
      
      - name: Format Check
        run: |
          python -m devkit_zero.cli format --file src/*.py --check
      
      - name: Lint Check
        run: |
          python -m devkit_zero.cli lint --directory src
```

### 自定义工具包装器 | Custom Tool Wrapper

```python
"""
自定义工具包装器
Custom tool wrapper
"""
from devkit_zero import formatter, linter, diff_tool

class CodeQualityChecker:
    """代码质量检查器 | Code quality checker"""
    
    def __init__(self):
        self.issues = []
    
    def check_file(self, file_path):
        """
        检查文件的代码质量
        Check file code quality
        """
        # 1. 格式化检查 | Format check
        formatted, err = formatter.format_file(file_path)
        if err:
            self.issues.append({
                'file': file_path,
                'type': 'format',
                'message': err
            })
        
        # 2. 语法检查 | Syntax check
        with open(file_path, 'r') as f:
            code = f.read()
        
        lint_issues = linter.check_code(code)
        self.issues.extend([
            {
                'file': file_path,
                'type': 'lint',
                'line': issue['line'],
                'message': issue['message']
            }
            for issue in lint_issues
        ])
        
        return len(self.issues) == 0
    
    def get_report(self):
        """
        获取检查报告
        Get check report
        """
        return {
            'total_issues': len(self.issues),
            'issues': self.issues
        }

# 使用示例 | Usage example
checker = CodeQualityChecker()
if checker.check_file('test.py'):
    print("✓ 代码质量良好 | Code quality is good")
else:
    report = checker.get_report()
    print(f"发现 {report['total_issues']} 个问题")
    print(f"Found {report['total_issues']} issues")
```

---

## 📞 支持与反馈 | Support & Feedback

### 获取帮助 | Get Help

**中文：**
- 📖 查看文档：[docs/](docs/)
- 💬 提出问题：[GitHub Issues](https://github.com/thirtycents/Devkit/issues)
- 📧 联系作者：查看 [__version__.py](__version__.py) 中的联系方式

**English:**
- 📖 Read docs: [docs/](docs/)
- 💬 Ask questions: [GitHub Issues](https://github.com/thirtycents/Devkit/issues)
- 📧 Contact: See contact info in [__version__.py](__version__.py)

### 报告 Bug | Report Bugs

**提交 Bug 时请包含：| When reporting bugs, please include:**
1. Python 版本 | Python version
2. 操作系统 | Operating system
3. 完整错误信息 | Complete error message
4. 复现步骤 | Steps to reproduce

---

## 📄 许可证 | License

MIT License - 查看 [LICENSE](LICENSE) 文件了解详情

MIT License - See [LICENSE](LICENSE) file for details

---

## 🙏 致谢 | Acknowledgments

**中文：**
感谢所有贡献者和使用者的支持！

**English:**
Thanks to all contributors and users for your support!

---

**最后更新 | Last Updated:** 2025-11-01

**版本 | Version:** 0.1.0

**仓库 | Repository:** https://github.com/thirtycents/Devkit
