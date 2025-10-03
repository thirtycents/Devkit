# 🛠️ 工具开发模板

本文档提供标准的工具开发模板和详细说明,确保所有工具遵循统一规范。

## 📋 目录
- [快速开始](#快速开始)
- [完整代码模板](#完整代码模板)
- [逐步解析](#逐步解析)
- [常见模式](#常见模式)
- [最佳实践](#最佳实践)
- [示例工具](#示例工具)

---

## 🚀 快速开始

### 创建新工具的三个步骤

1. **复制模板文件**
   ```bash
   cp templates/tool_template.py devkit_zero/tools/your_tool.py
   ```

2. **实现三个必需函数**
   - `main_function()` - 核心功能
   - `register_parser()` - CLI注册
   - `main()` - 独立运行

3. **注册工具**
   ```python
   # 在 devkit_zero/tools/__init__.py 中添加
   from devkit_zero.tools import your_tool
   ```

---

## 📝 完整代码模板

```python
"""
工具名称 - 简短描述

详细说明:
- 功能1
- 功能2
- 功能3

作者: Your Name
创建日期: YYYY-MM-DD
"""

import argparse
import sys
from typing import Optional, List, Dict, Any
from pathlib import Path


# =============================================================================
# 核心功能函数
# =============================================================================

def core_logic(input_data: str, **options) -> Any:
    """
    工具的核心逻辑函数(可选,但推荐)
    
    将核心逻辑与CLI/GUI分离,便于:
    - 单元测试
    - 作为库使用
    - 在不同界面复用
    
    Args:
        input_data: 输入数据
        **options: 可选参数
        
    Returns:
        处理结果
        
    Raises:
        ValueError: 输入数据无效时
        RuntimeError: 处理失败时
        
    Example:
        >>> result = core_logic("sample input", option1=True)
        >>> print(result)
        'processed output'
    """
    # TODO: 实现核心逻辑
    # 1. 验证输入
    # 2. 执行处理
    # 3. 返回结果
    raise NotImplementedError("核心逻辑待实现")


# =============================================================================
# CLI接口函数(必需)
# =============================================================================

def main_function(args: argparse.Namespace) -> int:
    """
    工具的主要功能函数 - CLI入口
    
    这是必需的函数,DevKit-Zero框架会调用此函数
    
    Args:
        args: 解析后的命令行参数对象
        
    Returns:
        退出代码:
        - 0: 成功
        - 1: 一般错误
        - 2: 参数错误
        - 其他非0值: 特定错误
        
    流程:
        1. 验证参数
        2. 读取输入
        3. 调用核心逻辑
        4. 处理输出
        5. 错误处理
    """
    try:
        # 1. 参数验证
        if not validate_args(args):
            print("Error: Invalid arguments", file=sys.stderr)
            return 2
        
        # 2. 读取输入
        input_data = read_input(args)
        
        # 3. 调用核心逻辑
        result = core_logic(
            input_data,
            option1=args.option1,
            option2=args.option2
        )
        
        # 4. 输出结果
        write_output(result, args)
        
        # 5. 成功返回
        if args.verbose:
            print("✓ Operation completed successfully")
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: Invalid value - {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: Unexpected error - {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def register_parser(subparsers) -> None:
    """
    注册CLI子命令 - 必需函数
    
    在CLI框架中注册此工具,定义命令行接口
    
    Args:
        subparsers: argparse的子解析器集合
        
    示例命令:
        devkit-zero tool-name [options] input
    """
    parser = subparsers.add_parser(
        'tool-name',  # 命令名称(使用小写+连字符)
        help='工具的简短描述',
        description='工具的详细描述',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s input.txt
  %(prog)s -o output.txt input.txt
  %(prog)s --option1 --option2 value input.txt
        '''
    )
    
    # 位置参数
    parser.add_argument(
        'input',
        help='输入文件路径或数据'
    )
    
    # 可选参数
    parser.add_argument(
        '-o', '--output',
        help='输出文件路径(默认: stdout)',
        default=None
    )
    
    parser.add_argument(
        '--option1',
        action='store_true',
        help='启用选项1'
    )
    
    parser.add_argument(
        '--option2',
        type=str,
        default='default_value',
        help='选项2的值(默认: default_value)'
    )
    
    # 通用选项
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细输出'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='静默模式,仅输出错误'
    )


def main():
    """
    独立运行入口 - 必需函数
    
    允许工具作为独立脚本运行:
        python -m devkit_zero.tools.tool_name
        或
        python devkit_zero/tools/tool_name.py
    """
    parser = argparse.ArgumentParser(
        description='工具名称 - 详细描述'
    )
    
    # 创建子解析器并注册
    subparsers = parser.add_subparsers(dest='command')
    register_parser(subparsers)
    
    # 解析参数
    args = parser.parse_args()
    
    # 调用主函数
    sys.exit(main_function(args))


# =============================================================================
# 辅助函数
# =============================================================================

def validate_args(args: argparse.Namespace) -> bool:
    """
    验证参数有效性
    
    Args:
        args: 命令行参数
        
    Returns:
        True if valid, False otherwise
    """
    # TODO: 实现参数验证逻辑
    return True


def read_input(args: argparse.Namespace) -> str:
    """
    读取输入数据
    
    Args:
        args: 命令行参数
        
    Returns:
        输入数据字符串
        
    Raises:
        FileNotFoundError: 文件不存在
        IOError: 读取失败
    """
    input_path = Path(args.input)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_output(result: Any, args: argparse.Namespace) -> None:
    """
    写入输出结果
    
    Args:
        result: 处理结果
        args: 命令行参数
    """
    output_str = str(result)
    
    if args.output:
        # 输出到文件
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_str)
        if not args.quiet:
            print(f"Output written to: {args.output}")
    else:
        # 输出到stdout
        print(output_str)


# =============================================================================
# 模块入口点
# =============================================================================

if __name__ == '__main__':
    main()
```

---

## 📖 逐步解析

### 1. 文档字符串(Docstring)

```python
"""
工具名称 - 简短描述

详细说明:
- 功能点1
- 功能点2
"""
```

**要点**:
- 第一行: 简短描述(一句话)
- 空行
- 详细说明
- 功能列表

### 2. 导入语句

```python
import argparse          # 命令行参数解析
import sys              # 系统功能
from typing import ...  # 类型提示
from pathlib import Path # 路径操作
```

**规范**:
- 标准库导入
- 按字母排序
- 分组(标准库/第三方/本地)

### 3. 核心逻辑函数

```python
def core_logic(input_data: str, **options) -> Any:
    """核心功能,与界面分离"""
    # 实现核心逻辑
    pass
```

**优点**:
- 便于单元测试
- 可作为库函数调用
- 界面无关

### 4. main_function - CLI入口

```python
def main_function(args: argparse.Namespace) -> int:
    """必需函数,返回退出代码"""
    try:
        # 处理逻辑
        return 0  # 成功
    except Exception:
        return 1  # 失败
```

**返回值约定**:
- 0: 成功
- 1: 一般错误
- 2: 参数错误
- 其他: 特定错误

### 5. register_parser - 注册CLI

```python
def register_parser(subparsers) -> None:
    """注册子命令"""
    parser = subparsers.add_parser('tool-name', ...)
    parser.add_argument(...)
```

**命名规范**:
- 工具名: 小写+连字符 `tool-name`
- 短选项: `-o`
- 长选项: `--option`

### 6. main - 独立运行

```python
def main():
    """独立运行入口"""
    parser = argparse.ArgumentParser(...)
    # ...
    sys.exit(main_function(args))
```

---

## 🎯 常见模式

### 模式1: 文件处理工具

```python
def main_function(args):
    # 读取文件
    with open(args.input, 'r') as f:
        content = f.read()
    
    # 处理
    result = process(content)
    
    # 写入文件
    with open(args.output, 'w') as f:
        f.write(result)
```

### 模式2: 数据转换工具

```python
def main_function(args):
    # 加载数据
    data = load_data(args.input, format=args.input_format)
    
    # 转换
    converted = convert(data, target_format=args.output_format)
    
    # 保存
    save_data(converted, args.output)
```

### 模式3: 检查/验证工具

```python
def main_function(args):
    # 读取目标
    target = load_target(args.input)
    
    # 检查
    issues = check(target, rules=args.rules)
    
    # 报告
    if issues:
        report_issues(issues)
        return 1  # 有问题
    return 0  # 无问题
```

### 模式4: 生成器工具

```python
def main_function(args):
    # 读取配置
    config = parse_config(args.config)
    
    # 生成
    output = generate(
        template=args.template,
        **config
    )
    
    # 保存
    save_output(output, args.output)
```

---

## ✅ 最佳实践

### DO ✅

1. **清晰的文档字符串**
   ```python
   def function(arg: str) -> int:
       """
       简短描述
       
       Args:
           arg: 参数说明
           
       Returns:
           返回值说明
       """
   ```

2. **类型提示**
   ```python
   def process(data: str, count: int = 10) -> List[str]:
       pass
   ```

3. **合理的错误处理**
   ```python
   try:
       result = risky_operation()
   except SpecificError as e:
       print(f"Error: {e}", file=sys.stderr)
       return 1
   ```

4. **详细的帮助信息**
   ```python
   parser.add_argument(
       '--option',
       help='清楚说明这个选项的作用'
   )
   ```

5. **输入验证**
   ```python
   if not input_file.exists():
       raise FileNotFoundError(...)
   ```

### DON'T ❌

1. **不要硬编码路径**
   ```python
   # ❌ 错误
   file = open('C:/Users/user/file.txt')
   
   # ✅ 正确
   file = open(args.input)
   ```

2. **不要忽略异常**
   ```python
   # ❌ 错误
   try:
       risky()
   except:
       pass
   
   # ✅ 正确
   except SpecificError as e:
       handle_error(e)
   ```

3. **不要使用print调试**
   ```python
   # ❌ 错误
   print("debug:", value)
   
   # ✅ 正确
   if args.verbose:
       print(f"Processing: {value}")
   ```

---

## 📚 示例工具

### 简单示例: 行数统计

```python
"""简单的行数统计工具"""
import argparse
import sys


def count_lines(text: str) -> int:
    """统计行数"""
    return len(text.splitlines())


def main_function(args: argparse.Namespace) -> int:
    try:
        with open(args.input, 'r') as f:
            text = f.read()
        
        line_count = count_lines(text)
        print(f"Lines: {line_count}")
        return 0
    except FileNotFoundError:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        return 1


def register_parser(subparsers):
    parser = subparsers.add_parser('line-count', help='Count lines in file')
    parser.add_argument('input', help='Input file')


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    register_parser(subparsers)
    args = parser.parse_args()
    sys.exit(main_function(args))


if __name__ == '__main__':
    main()
```

### 完整示例: 参考 `devkit_zero/tools/formatter.py`

---

## 🧪 测试模板

```python
"""工具测试模板"""
import pytest
from argparse import Namespace
from devkit_zero.tools.your_tool import (
    core_logic,
    main_function,
    validate_args
)


def test_core_logic_basic():
    """测试核心逻辑 - 基础场景"""
    result = core_logic("input data")
    assert result == "expected output"


def test_core_logic_edge_case():
    """测试边界情况"""
    result = core_logic("")
    assert result is not None


def test_main_function_success(tmp_path):
    """测试主函数 - 成功场景"""
    # 准备
    input_file = tmp_path / "input.txt"
    input_file.write_text("test data")
    
    args = Namespace(
        input=str(input_file),
        output=None,
        verbose=False
    )
    
    # 执行
    exit_code = main_function(args)
    
    # 断言
    assert exit_code == 0


def test_main_function_file_not_found():
    """测试文件不存在"""
    args = Namespace(input='nonexistent.txt')
    exit_code = main_function(args)
    assert exit_code == 1
```

---

## 📋 检查清单

开发完成后,检查:

- [ ] 实现了三个必需函数
- [ ] 有完整的文档字符串
- [ ] 有类型提示
- [ ] 有错误处理
- [ ] 有输入验证
- [ ] 编写了单元测试
- [ ] 测试覆盖率 > 80%
- [ ] 注册到工具列表
- [ ] 更新了文档

---

## 📚 相关资源

- [项目框架说明](PROJECT_FRAMEWORK.md)
- [API设计规范](API_DESIGN.md)
- [新手开发指南](../team/BEGINNER_GUIDE.md)
- [快速参考](../reference/QUICK_REFERENCE.md)

---

**版本**: v1.0  
**最后更新**: 2025-XX-XX  
**维护者**: DevKit-Zero开发团队
