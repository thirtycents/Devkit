# 🔌 API设计规范

本文档定义DevKit-Zero项目的API设计标准,确保所有代码遵循统一规范。

## 📋 目录
- [命名规范](#命名规范)
- [函数签名设计](#函数签名设计)
- [参数设计原则](#参数设计原则)
- [返回值规范](#返回值规范)
- [错误处理策略](#错误处理策略)
- [文档字符串标准](#文档字符串标准)
- [类型提示规范](#类型提示规范)

---

## 📝 命名规范

### 通用原则
- **清晰胜于简洁**: `calculate_total_price()` 优于 `calc()`
- **见名知意**: 函数名应明确表达功能
- **一致性**: 整个项目使用统一的命名风格

### 具体规范

| 类型 | 规范 | 示例 | 说明 |
|------|------|------|------|
| **模块** | `lower_with_under` | `file_ops.py` | 小写+下划线 |
| **类名** | `CapWords` | `CodeFormatter` | 大驼峰 |
| **函数** | `lower_with_under()` | `format_code()` | 小写+下划线 |
| **方法** | `lower_with_under()` | `get_result()` | 小写+下划线 |
| **常量** | `UPPER_WITH_UNDER` | `MAX_LINE_LENGTH` | 大写+下划线 |
| **变量** | `lower_with_under` | `line_count` | 小写+下划线 |
| **私有** | `_leading_underscore` | `_internal_helper()` | 前置下划线 |

### 函数命名模式

```python
# 动词开头,表明动作
def calculate_total() -> int: ...
def validate_input() -> bool: ...
def parse_config() -> dict: ...
def generate_report() -> str: ...

# 检查/查询:返回bool
def is_valid() -> bool: ...
def has_errors() -> bool: ...
def can_process() -> bool: ...

# 获取:返回值
def get_config() -> dict: ...
def fetch_data() -> list: ...

# 设置:修改状态
def set_option(value): ...
def update_config(config): ...
```

### CLI命令命名

```bash
# 使用连字符分隔
devkit-zero tool-name       # ✅ 正确
devkit-zero tool_name       # ❌ 错误
devkit-zero toolName        # ❌ 错误

# 清晰的动词-名词结构
devkit-zero format-code     # ✅ 格式化代码
devkit-zero check-port      # ✅ 检查端口
devkit-zero generate-data   # ✅ 生成数据
```

---

## 🔧 函数签名设计

### 基本原则

1. **参数顺序**: 必需参数 → 可选参数 → 关键字参数
2. **默认值**: 使用不可变对象作为默认值
3. **类型提示**: 所有公共函数必须有类型提示

### 标准签名模式

```python
def function_name(
    required_param: str,              # 必需参数
    optional_param: int = 0,           # 可选参数
    *,                                 # 强制关键字参数
    keyword_param: bool = False,       # 关键字参数
    **kwargs                           # 额外关键字参数
) -> ReturnType:
    """函数文档"""
    pass
```

### 示例

```python
# ✅ 好的设计
def format_code(
    source: str,                    # 必需: 源代码
    indent: int = 4,                 # 可选: 缩进
    *,
    max_line_length: int = 79,       # 关键字: 最大行长
    use_tabs: bool = False           # 关键字: 使用tab
) -> str:
    """格式化代码"""
    pass

# ❌ 不好的设计
def format(s, i=4, m=79, t=False):  # 参数名不清晰
    pass
```

### 参数数量建议

- **0-3个参数**: 理想 ✅
- **4-5个参数**: 可接受 ⚠️
- **6个以上**: 考虑重构 ❌

重构方法:
```python
# ❌ 参数太多
def create_user(name, age, email, phone, address, city, country):
    pass

# ✅ 使用配置对象
def create_user(user_data: dict):
    pass

# ✅ 使用类
class UserBuilder:
    def with_name(self, name): ...
    def with_contact(self, email, phone): ...
    def build(self): ...
```

---

## 📊 参数设计原则

### 1. 使用类型提示

```python
# ✅ 清晰的类型
def process_file(
    path: Path,                    # 使用Path而非str
    encoding: str = 'utf-8',
    max_size: Optional[int] = None
) -> List[str]:
    pass

# ❌ 没有类型提示
def process_file(path, encoding='utf-8', max_size=None):
    pass
```

### 2. 避免可变默认值

```python
# ❌ 危险:可变默认值
def append_to_list(item, list=[]):
    list.append(item)
    return list

# ✅ 安全:使用None
def append_to_list(item, list=None):
    if list is None:
        list = []
    list.append(item)
    return list
```

### 3. 布尔参数命名

```python
# ✅ 清晰的布尔参数
def save_file(
    path: Path,
    *,
    overwrite: bool = False,      # 是否覆盖
    create_backup: bool = True,    # 是否备份
    validate_content: bool = True  # 是否验证
):
    pass

# ❌ 不清晰
def save_file(path, flag1=False, flag2=True):
    pass
```

### 4. 使用枚举而非字符串

```python
from enum import Enum

# ✅ 使用枚举
class OutputFormat(Enum):
    JSON = 'json'
    XML = 'xml'
    YAML = 'yaml'

def export_data(data: dict, format: OutputFormat):
    pass

# ❌ 使用字符串
def export_data(data, format='json'):  # 容易拼写错误
    pass
```

---

## 🎯 返回值规范

### 返回值原则

1. **一致性**: 同一函数总是返回相同类型
2. **明确性**: 返回值类型要清晰
3. **错误处理**: 使用异常而非特殊返回值

### 返回类型模式

```python
# 单一返回值
def calculate_sum(numbers: List[int]) -> int:
    return sum(numbers)

# 元组返回多个值
def get_min_max(numbers: List[int]) -> tuple[int, int]:
    return min(numbers), max(numbers)

# 可选返回值
def find_user(user_id: int) -> Optional[dict]:
    # 找到返回dict,找不到返回None
    pass

# 返回自定义类型
from dataclasses import dataclass

@dataclass
class Result:
    success: bool
    data: Any
    error: Optional[str] = None

def process_data(data: str) -> Result:
    pass
```

### CLI函数的返回值

```python
def main_function(args: argparse.Namespace) -> int:
    """
    CLI函数必须返回int退出代码
    
    Returns:
        0: 成功
        1: 一般错误
        2: 参数错误
        其他: 特定错误代码
    """
    try:
        # 处理逻辑
        return 0
    except ValueError:
        return 2
    except Exception:
        return 1
```

### 不要返回None表示错误

```python
# ❌ 错误: 使用None表示错误
def divide(a: int, b: int) -> Optional[float]:
    if b == 0:
        return None  # 错误情况
    return a / b

# ✅ 正确: 使用异常
def divide(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("Division by zero")
    return a / b
```

---

## ⚠️ 错误处理策略

### 异常层次

```python
# 自定义异常基类
class DevKitError(Exception):
    """DevKit-Zero 基础异常"""
    pass

class InputError(DevKitError):
    """输入错误"""
    pass

class ProcessingError(DevKitError):
    """处理错误"""
    pass

class ConfigError(DevKitError):
    """配置错误"""
    pass
```

### 错误处理模式

```python
def main_function(args: argparse.Namespace) -> int:
    """标准错误处理模式"""
    try:
        # 1. 验证输入
        validate_input(args)
        
        # 2. 执行处理
        result = process(args)
        
        # 3. 输出结果
        output_result(result, args)
        
        return 0
        
    except FileNotFoundError as e:
        # 特定错误处理
        print(f"Error: File not found - {e}", file=sys.stderr)
        return 1
        
    except ValueError as e:
        # 参数错误
        print(f"Error: Invalid value - {e}", file=sys.stderr)
        return 2
        
    except KeyboardInterrupt:
        # 用户中断
        print("\nOperation cancelled by user", file=sys.stderr)
        return 130
        
    except Exception as e:
        # 未预期错误
        print(f"Error: Unexpected error - {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
```

### 错误信息格式

```python
# ✅ 好的错误信息
raise ValueError(
    f"Invalid input: expected positive integer, got {value}"
)

# ❌ 不好的错误信息
raise ValueError("error")  # 信息不足
```

---

## 📖 文档字符串标准

### Google风格文档字符串(推荐)

```python
def complex_function(
    param1: str,
    param2: int,
    param3: Optional[list] = None
) -> dict:
    """
    函数的简短描述(一行)
    
    更详细的描述可以在这里展开,说明函数的用途、
    行为特点、注意事项等。
    
    Args:
        param1: 第一个参数的描述
        param2: 第二个参数的描述  
        param3: 第三个参数的描述(可选,默认为None)
        
    Returns:
        返回值的描述,包含类型和结构说明
        
    Raises:
        ValueError: 当param1为空时抛出
        IOError: 当文件操作失败时抛出
        
    Example:
        >>> result = complex_function("test", 42)
        >>> print(result)
        {'status': 'success'}
        
    Note:
        这里可以添加额外的注意事项
    """
    pass
```

### 类的文档字符串

```python
class DataProcessor:
    """
    数据处理器类
    
    这个类用于处理各种格式的数据,提供统一的
    处理接口。
    
    Attributes:
        config: 配置字典
        logger: 日志记录器
        
    Example:
        >>> processor = DataProcessor(config)
        >>> result = processor.process(data)
    """
    
    def __init__(self, config: dict):
        """
        初始化数据处理器
        
        Args:
            config: 配置字典,包含处理选项
        """
        self.config = config
```

### 模块的文档字符串

```python
"""
工具模块名称 - 简短描述

这个模块提供XXX功能,用于...

主要功能:
    - 功能1: 描述
    - 功能2: 描述
    - 功能3: 描述

使用示例:
    from devkit_zero.tools import module_name
    
    result = module_name.main_function(args)

作者: Your Name
创建日期: 2025-XX-XX
"""
```

---

## 🏷️ 类型提示规范

### 基本类型

```python
from typing import (
    Optional, List, Dict, Tuple, Set,
    Any, Union, Callable
)

# 基本类型
def func(
    text: str,
    count: int,
    ratio: float,
    flag: bool
) -> None:
    pass

# 容器类型
def process(
    items: List[str],
    mapping: Dict[str, int],
    coords: Tuple[float, float],
    unique: Set[int]
) -> List[dict]:
    pass

# 可选类型
def find(key: str) -> Optional[dict]:
    pass

# 联合类型
def parse(value: Union[str, int, float]) -> str:
    pass

# 任意类型(尽量避免)
def debug(data: Any) -> None:
    pass
```

### 复杂类型

```python
from typing import Callable, TypeVar, Generic

# 回调函数
Callback = Callable[[str], bool]

def process_items(
    items: List[str],
    filter_fn: Callback
) -> List[str]:
    pass

# 泛型
T = TypeVar('T')

def first(items: List[T]) -> Optional[T]:
    return items[0] if items else None

# 类型别名
FilePath = str
Config = Dict[str, Any]

def load_config(path: FilePath) -> Config:
    pass
```

### Python 3.10+ 新语法

```python
# 联合类型简化
def process(value: str | int | float) -> str:
    pass

# 内置容器类型
def func(items: list[str], mapping: dict[str, int]) -> tuple[int, int]:
    pass
```

---

## ✅ 最佳实践清单

### 函数设计
- [ ] 函数职责单一
- [ ] 参数数量合理(≤5个)
- [ ] 有清晰的类型提示
- [ ] 有完整的文档字符串
- [ ] 返回值类型一致
- [ ] 错误处理完善

### 命名规范
- [ ] 遵循PEP 8命名约定
- [ ] 函数名清晰表达意图
- [ ] 变量名见名知意
- [ ] 避免单字母变量(除循环变量)

### 文档
- [ ] 所有公共API有文档字符串
- [ ] 文档包含使用示例
- [ ] 说明可能抛出的异常
- [ ] 注明重要的注意事项

### 类型
- [ ] 所有公共函数有类型提示
- [ ] 使用合适的类型(避免Any)
- [ ] Optional用于可能为None的值
- [ ] 复杂类型使用类型别名

---

## 📚 参考资源

- [PEP 8 - Python代码风格指南](https://pep8.org/)
- [PEP 257 - 文档字符串约定](https://www.python.org/dev/peps/pep-0257/)
- [PEP 484 - 类型提示](https://www.python.org/dev/peps/pep-0484/)
- [Google Python风格指南](https://google.github.io/styleguide/pyguide.html)

---

**版本**: v1.0  
**最后更新**: 2025-XX-XX  
**维护者**: DevKit-Zero架构团队
