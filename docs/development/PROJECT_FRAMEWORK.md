# 🏗️ DevKit-Zero 项目框架说明

## 📋 目录
- [整体架构](#整体架构)
- [目录结构详解](#目录结构详解)
- [核心组件](#核心组件)
- [工具注册机制](#工具注册机制)
- [扩展性设计](#扩展性设计)
- [数据流](#数据流)

---

## 🎯 整体架构

### 架构图

```
┌─────────────────────────────────────────────────┐
│                  用户界面层                      │
│  ┌─────────────┐          ┌─────────────┐      │
│  │  CLI Entry  │          │  GUI Entry  │      │
│  │  (cli.py)   │          │(gui_main.py)│      │
│  └──────┬──────┘          └──────┬──────┘      │
└─────────┼─────────────────────────┼─────────────┘
          │                         │
┌─────────┼─────────────────────────┼─────────────┐
│         │      核心API层           │             │
│         └─────────┬────────────────┘             │
│                   │                              │
│         ┌─────────▼────────┐                     │
│         │   Core API       │                     │
│         │   (core.py)      │                     │
│         │  - 工具注册      │                     │
│         │  - 统一接口      │                     │
│         └─────────┬────────┘                     │
└───────────────────┼──────────────────────────────┘
                    │
┌───────────────────┼──────────────────────────────┐
│                   │      工具层                   │
│    ┌──────────────┴──────────────┐              │
│    │    Tool Registry             │              │
│    │  (tools/__init__.py)         │              │
│    └──────────────┬───────────────┘              │
│                   │                              │
│    ┌──────────────┼───────────────┐              │
│    │              │                │              │
│ ┌──▼──┐      ┌───▼────┐      ┌───▼────┐        │
│ │Tool1│      │ Tool2  │  ... │ Tool9  │        │
│ └─────┘      └────────┘      └────────┘        │
└──────────────────────────────────────────────────┘
                    │
┌───────────────────┼──────────────────────────────┐
│                   │     工具层                    │
│    ┌──────────────┴──────────────┐              │
│    │  UI Components (ui/)         │              │
│    │  Utils (utils/)              │              │
│    │  - file_ops.py               │              │
│    │  - validators.py             │              │
│    │  - helpers.py                │              │
│    └──────────────────────────────┘              │
└──────────────────────────────────────────────────┘
```

### 设计原则

1. **模块化**: 每个工具独立,互不依赖
2. **可扩展**: 轻松添加新工具
3. **零依赖**: 仅使用Python标准库
4. **统一接口**: 所有工具遵循相同规范
5. **易测试**: 每个组件可独立测试

---

## 📂 目录结构详解

```
devkit-zero/
│
├── devkit_zero/                 # 主包目录
│   ├── __init__.py             # 包初始化,导出公共API
│   ├── __version__.py          # 版本信息
│   ├── core.py                 # 核心API和工具基类
│   ├── cli.py                  # CLI入口点
│   ├── gui_main.py             # GUI入口点
│   │
│   ├── tools/                  # 工具模块目录
│   │   ├── __init__.py        # 工具注册中心
│   │   ├── formatter.py       # 代码格式化工具
│   │   ├── random_gen.py      # 随机数据生成器
│   │   ├── diff_tool.py       # 文件差异比较
│   │   ├── converter.py       # 格式转换工具
│   │   ├── linter.py          # 代码检查工具
│   │   ├── regex_tester.py    # 正则表达式测试
│   │   ├── batch_process.py   # 批量处理工具
│   │   ├── markdown_preview.py # Markdown预览
│   │   └── port_checker.py    # 端口检查工具
│   │
│   ├── ui/                     # UI组件
│   │   ├── __init__.py
│   │   ├── main_window.py     # 主窗口(待实现)
│   │   └── widgets.py         # 自定义控件(待实现)
│   │
│   └── utils/                  # 工具函数
│       ├── __init__.py
│       ├── file_ops.py        # 文件操作(待实现)
│       ├── validators.py      # 输入验证(待实现)
│       └── helpers.py         # 辅助函数(待实现)
│
├── tests/                      # 测试目录
│   ├── conftest.py            # pytest配置和fixtures
│   ├── test_core.py           # 核心API测试(待实现)
│   ├── test_cli.py            # CLI测试(待实现)
│   └── test_tools/            # 工具测试
│       ├── test_formatter.py  # 格式化工具测试
│       └── ...                # 其他工具测试(待实现)
│
├── docs/                       # 文档目录
│   ├── README.md              # 文档导航
│   ├── team/                  # 团队协作文档
│   ├── development/           # 开发技术文档
│   └── reference/             # 快速参考
│
├── assets/                     # 资源文件
│   ├── icons/                 # 图标(待添加)
│   └── images/                # 图片(待添加)
│
├── templates/                  # 模板文件
│   └── tool_template.py       # 工具模板(待添加)
│
├── static/                     # 静态文件
│   └── css/                   # 样式文件(待添加)
│
├── .github/                    # GitHub配置
│   └── workflows/             # CI/CD工作流(待添加)
│
├── .gitignore                  # Git忽略配置
├── setup.py                    # 安装配置
├── pyproject.toml             # 项目元数据
├── requirements.txt           # 运行时依赖
├── requirements-dev.txt       # 开发依赖
├── CHANGELOG.md               # 版本变更日志
└── README.md                  # 项目说明
```

---

## 🔧 核心组件

### 1. `__init__.py` - 包初始化

**作用**: 定义包的公共API

```python
"""
DevKit-Zero - 开发者工具箱

主要功能:
1. 提供多个开发工具的统一访问接口
2. 支持CLI和GUI两种使用方式
"""

from devkit_zero.__version__ import __version__
from devkit_zero.core import ToolBase, run_tool

__all__ = [
    '__version__',
    'ToolBase',
    'run_tool',
]
```

**关键点**:
- 导出版本信息
- 导出核心API
- 使用`__all__`控制公共接口

### 2. `core.py` - 核心API

**作用**: 提供工具基类和统一接口

```python
# TODO: 实现以下功能
# 1. ToolBase基类 - 所有工具的基类
# 2. 工具注册机制
# 3. run_tool()统一调用接口
# 4. 错误处理和日志记录
```

**设计要点**:
- 工具基类定义标准接口
- 注册机制管理所有工具
- 统一的错误处理
- 日志记录支持

### 3. `cli.py` - CLI入口

**作用**: 命令行界面入口

**流程**:
```
用户输入命令
    ↓
解析命令行参数
    ↓
查找对应工具
    ↓
调用工具main_function
    ↓
返回退出代码
```

**实现要点**:
```python
# 使用argparse的subparsers
# 每个工具注册自己的子命令
# 统一的错误处理和帮助信息
```

### 4. `gui_main.py` - GUI入口

**作用**: 图形界面入口

**流程**:
```
启动GUI
    ↓
显示工具列表
    ↓
用户选择工具
    ↓
显示工具界面
    ↓
调用工具功能
    ↓
显示结果
```

**实现要点**:
```python
# 使用tkinter标准库
# 主窗口包含工具列表
# 每个工具有独立的参数面板
# 结果显示区域
```

---

## 🔌 工具注册机制

### 注册流程

```python
# tools/__init__.py

# 1. 导入所有工具
from devkit_zero.tools import formatter
from devkit_zero.tools import random_gen
# ...

# 2. 工具列表
AVAILABLE_TOOLS = [
    'formatter',
    'random_gen',
    # ...
]

# 3. 注册函数
def register_all_tools(subparsers):
    """注册所有工具到CLI"""
    formatter.register_parser(subparsers)
    random_gen.register_parser(subparsers)
    # ...
```

### 工具结构

每个工具必须实现三个函数:

```python
# 1. 主功能函数
def main_function(args: argparse.Namespace) -> int:
    """工具的核心逻辑"""
    pass

# 2. CLI注册函数
def register_parser(subparsers) -> None:
    """注册到CLI"""
    pass

# 3. 独立运行入口
def main():
    """独立运行时的入口"""
    pass
```

---

## 🔄 扩展性设计

### 添加新工具的步骤

1. **创建工具文件**
   ```bash
   touch devkit_zero/tools/new_tool.py
   ```

2. **实现三个必需函数**
   ```python
   def main_function(args): ...
   def register_parser(subparsers): ...
   def main(): ...
   ```

3. **注册工具**
   ```python
   # 在 tools/__init__.py 中
   from devkit_zero.tools import new_tool
   
   AVAILABLE_TOOLS.append('new_tool')
   
   def register_all_tools(subparsers):
       # ... 现有代码
       new_tool.register_parser(subparsers)
   ```

4. **编写测试**
   ```bash
   touch tests/test_tools/test_new_tool.py
   ```

5. **更新文档**
   - 在README.md中添加工具说明
   - 更新TASK_ASSIGNMENT.md

### 扩展点

| 扩展点 | 位置 | 说明 |
|--------|------|------|
| 新工具 | `tools/` | 添加新的工具模块 |
| UI组件 | `ui/` | 自定义GUI组件 |
| 工具函数 | `utils/` | 通用辅助函数 |
| 测试fixture | `tests/conftest.py` | 共享测试资源 |

---

## 📊 数据流

### CLI模式数据流

```
用户命令行输入
    ↓
cli.py 解析参数
    ↓
tools/__init__.py 查找工具
    ↓
tool.main_function() 执行
    ↓
返回退出代码
    ↓
显示结果到终端
```

### GUI模式数据流

```
用户打开GUI
    ↓
gui_main.py 显示主窗口
    ↓
用户选择工具
    ↓
显示工具参数面板
    ↓
用户填写参数
    ↓
调用 tool.main_function()
    ↓
在GUI中显示结果
```

### 库模式数据流

```python
# 作为库使用
from devkit_zero.tools.formatter import format_code

result = format_code(source_code)
```

---

## 🎨 设计模式

### 1. 策略模式
每个工具都是一个独立的策略,通过统一接口调用。

### 2. 工厂模式
工具注册机制类似工厂模式,根据名称创建工具实例。

### 3. 模板方法
所有工具遵循相同的模板(三个必需函数)。

---

## 🔒 约束和限制

### 技术约束
- ✅ 仅使用Python标准库
- ✅ Python 3.8+兼容
- ✅ 跨平台支持(Windows/macOS/Linux)

### 设计约束
- 工具之间不应相互依赖
- 所有工具必须实现标准接口
- 错误处理统一规范

---

## 📈 未来规划

### Phase 1: 基础框架(当前)
- [x] 目录结构
- [ ] 核心API
- [ ] CLI基础
- [ ] 工具模板

### Phase 2: 核心工具
- [ ] 实现9个工具
- [ ] 完善测试
- [ ] 文档完善

### Phase 3: GUI支持
- [ ] GUI框架
- [ ] 工具GUI适配
- [ ] 主题支持

### Phase 4: 增强功能
- [ ] 插件系统
- [ ] 配置文件支持
- [ ] 国际化

---

## 📚 相关文档

- [工具开发模板](TOOL_TEMPLATE.md)
- [API设计规范](API_DESIGN.md)
- [新手开发指南](../team/BEGINNER_GUIDE.md)

---

**版本**: v1.0  
**最后更新**: 2025-XX-XX  
**维护者**: DevKit-Zero架构团队
