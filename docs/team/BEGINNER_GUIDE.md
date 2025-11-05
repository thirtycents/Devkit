# 🌟 DevKit-Zero 新手开发指南

欢迎加入DevKit-Zero开发团队!本指南将帮助你从零开始,快速上手项目开发。

## 📚 目录
- [开发环境配置](#开发环境配置)
- [获取代码](#获取代码)
- [理解项目结构](#理解项目结构)
- [开发你的第一个工具](#开发你的第一个工具)
- [测试与调试](#测试与调试)
- [提交代码](#提交代码)
- [常见问题](#常见问题)

---

## 🛠️ 开发环境配置

### 1. 安装Python

确保已安装Python 3.8或更高版本:

```bash
# 检查Python版本
python --version  # 应显示 Python 3.8.x 或更高

# 如果没有安装,请访问: https://www.python.org/downloads/
```

### 2. 安装Git

```bash
# 检查Git版本
git --version  # 应显示 git version 2.x.x

# 如果没有安装,请访问: https://git-scm.com/downloads
```

### 3. 配置Git(首次使用)

```bash
# 设置用户名和邮箱
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 验证配置
git config --list
```

### 4. 推荐IDE/编辑器

| 编辑器 | 优点 | 推荐插件 |
|--------|------|----------|
| **VS Code** | 轻量、插件丰富 | Python, Pylance, GitLens |
| **PyCharm** | 功能强大、智能提示好 | 自带完整功能 |
| **Vim/Neovim** | 高效、可定制 | coc-python, vim-gitgutter |

---

## 📥 获取代码

### 1. Fork项目(推荐)

```bash
# 1. 在GitHub上点击Fork按钮
# 2. Clone你fork的仓库
git clone https://github.com/你的用户名/devkit-zero.git
cd devkit-zero

# 3. 添加上游仓库
git remote add upstream https://github.com/原项目/devkit-zero.git

# 4. 验证远程仓库
git remote -v
```

### 2. 直接Clone(团队成员)

```bash
# Clone主仓库
git clone https://github.com/团队/devkit-zero.git
cd devkit-zero
```

### 3. 创建虚拟环境(推荐)

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 你应该看到命令行前缀变为 (venv)
```

### 4. 安装开发依赖

```bash
# 以可编辑模式安装项目
pip install -e .

# 安装开发工具
pip install -r requirements-dev.txt

# 验证安装
devkit-zero --version
```

---

## 📂 理解项目结构

### 目录结构

```
devkit-zero/
├── devkit_zero/              # 主要源代码目录
│   ├── __init__.py          # 包初始化
│   ├── __version__.py       # 版本信息
│   ├── core.py              # 核心API和工具注册
│   ├── cli.py               # 命令行入口
│   ├── gui_main.py          # 图形界面入口
│   ├── tools/               # 工具模块目录
│   │   ├── __init__.py      # 工具注册中心
│   │   ├── formatter.py     # 代码格式化工具
│   │   ├── random_gen.py    # 随机数据生成器
│   │   └── ...              # 其他工具
│   ├── ui/                  # UI组件
│   └── utils/               # 工具函数
├── tests/                    # 测试代码
│   ├── conftest.py          # pytest配置
│   └── test_tools/          # 工具测试
├── docs/                     # 文档
├── assets/                   # 资源文件
└── setup.py                  # 安装配置
```

### 关键文件说明

| 文件 | 作用 | 何时修改 |
|------|------|----------|
| `setup.py` | 安装配置 | 添加新依赖时 |
| `devkit_zero/tools/__init__.py` | 工具注册 | 添加新工具时 |
| `devkit_zero/core.py` | 核心API | 添加公共功能时 |
| `tests/conftest.py` | 测试配置 | 添加测试fixture时 |

---

## 🚀 开发你的第一个工具

让我们以开发一个简单的"文本统计"工具为例:

### 步骤1: 创建功能分支

```bash
# 确保在develop分支
git checkout develop
git pull origin develop

# 创建你的功能分支
git checkout -b feature/text-stats
```

### 步骤2: 创建工具文件

在 `devkit_zero/tools/` 下创建 `text_stats.py`:

```python
"""
文本统计工具 - 统计文本的行数、字数、字符数
"""
import argparse
from typing import Dict


def count_text(text: str) -> Dict[str, int]:
    """
    统计文本信息
    
    Args:
        text: 要统计的文本
        
    Returns:
        包含统计信息的字典
    """
    lines = text.split('\n')
    words = text.split()
    chars = len(text)
    
    return {
        'lines': len(lines),
        'words': len(words),
        'chars': chars
    }


def main_function(args: argparse.Namespace) -> int:
    """
    工具的主要功能
    
    Args:
        args: 命令行参数
        
    Returns:
        0表示成功,非0表示失败
    """
    try:
        # 读取输入文件
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # 统计
        stats = count_text(text)
        
        # 输出结果
        print(f"Lines:  {stats['lines']}")
        print(f"Words:  {stats['words']}")
        print(f"Chars:  {stats['chars']}")
        
        return 0
        
    except FileNotFoundError:
        print(f"Error: File '{args.input}' not found")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 2


def register_parser(subparsers) -> None:
    """
    注册CLI子命令
    
    Args:
        subparsers: argparse子解析器
    """
    parser = subparsers.add_parser(
        'text-stats',
        help='统计文本信息',
        description='统计文本的行数、字数、字符数'
    )
    
    parser.add_argument(
        'input',
        help='输入文件路径'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细信息'
    )


def main():
    """独立运行入口"""
    parser = argparse.ArgumentParser(description='文本统计工具')
    register_parser(parser.add_subparsers())
    args = parser.parse_args()
    return main_function(args)


if __name__ == '__main__':
    import sys
    sys.exit(main())
```

### 步骤3: 注册工具

编辑 `devkit_zero/tools/__init__.py`,添加你的工具:

```python
# ... 现有代码 ...

# 导入你的工具
from devkit_zero.tools import text_stats

# 在AVAILABLE_TOOLS列表中添加
AVAILABLE_TOOLS = [
    'formatter',
    'random_gen',
    'text_stats',  # 添加这一行
    # ... 其他工具
]

# 在register_all_tools函数中注册
def register_all_tools(subparsers):
    """注册所有工具到CLI"""
    formatter.register_parser(subparsers)
    random_gen.register_parser(subparsers)
    text_stats.register_parser(subparsers)  # 添加这一行
    # ... 其他工具
```

### 步骤4: 测试你的工具

创建测试文件 `tests/test_tools/test_text_stats.py`:

```python
"""文本统计工具测试"""
import pytest
from devkit_zero.tools.text_stats import count_text, main_function
from argparse import Namespace
import tempfile
import os


def test_count_text_basic():
    """测试基础文本统计"""
    text = "Hello World\nSecond Line"
    result = count_text(text)
    
    assert result['lines'] == 2
    assert result['words'] == 3
    assert result['chars'] == 23


def test_count_text_empty():
    """测试空文本"""
    result = count_text("")
    assert result['lines'] == 1  # 空文本也算一行
    assert result['words'] == 0
    assert result['chars'] == 0


def test_main_function_success():
    """测试主函数成功场景"""
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("Test content\nLine 2")
        temp_file = f.name
    
    try:
        args = Namespace(input=temp_file, verbose=False)
        result = main_function(args)
        assert result == 0
    finally:
        os.unlink(temp_file)


def test_main_function_file_not_found():
    """测试文件不存在的情况"""
    args = Namespace(input='nonexistent.txt', verbose=False)
    result = main_function(args)
    assert result == 1  # 错误代码
```

---

## 🧪 测试与调试

### 运行测试

```bash
# 运行所有测试
pytest

# 运行你的工具测试
pytest tests/test_tools/test_text_stats.py

# 详细输出
pytest -v -s

# 查看覆盖率
pytest --cov=devkit_zero tests/
```

### 手动测试

```bash
# 方式1: 使用CLI
devkit-zero text-stats test.txt

# 方式2: 直接运行模块
python -m devkit_zero.tools.text_stats test.txt

# 方式3: 作为脚本运行
python devkit_zero/tools/text_stats.py test.txt
```

### 调试技巧

#### 1. 使用print调试
```python
def main_function(args):
    print(f"DEBUG: args = {args}")  # 调试输出
    # ... 你的代码
```

#### 2. 使用pdb调试器
```python
import pdb

def main_function(args):
    pdb.set_trace()  # 在这里暂停
    # ... 你的代码
```

#### 3. 使用VS Code调试
创建 `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug Tool",
            "type": "python",
            "request": "launch",
            "module": "devkit_zero.tools.text_stats",
            "args": ["test.txt"],
            "console": "integratedTerminal"
        }
    ]
}
```

---

## 📤 提交代码

### 1. 检查代码质量

```bash
# 代码格式化
black devkit_zero/tools/text_stats.py

# 代码检查
flake8 devkit_zero/tools/text_stats.py

# 运行测试
pytest tests/test_tools/test_text_stats.py
```

### 2. 提交更改

```bash
# 查看修改
git status

# 添加文件
git add devkit_zero/tools/text_stats.py
git add devkit_zero/tools/__init__.py
git add tests/test_tools/test_text_stats.py

# 提交
git commit -m "feat(text-stats): add text statistics tool"
```

### 3. 推送到GitHub

```bash
# 推送分支
git push origin feature/text-stats
```

### 4. 创建Pull Request

1. 访问GitHub仓库
2. 点击 "Compare & pull request"
3. 填写PR描述(参考模板)
4. 等待代码审查

---

## ❓ 常见问题

### Q1: 虚拟环境激活失败?

**Windows PowerShell执行策略问题**:
```powershell
# 以管理员身份运行PowerShell
Set-ExecutionPolicy RemoteSigned

# 然后重试激活
venv\Scripts\activate
```

### Q2: pip install失败?

```bash
# 尝试升级pip
python -m pip install --upgrade pip

# 如果网络问题,使用国内镜像
pip install -e . -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: 测试失败怎么办?

```bash
# 详细查看失败原因
pytest -v -s tests/test_tools/test_your_tool.py

# 只运行失败的测试
pytest --lf
```

### Q4: 如何同步最新代码?

```bash
# 更新develop分支
git checkout develop
git pull origin develop

# 合并到你的分支
git checkout feature/your-tool
git merge develop
```

### Q5: Git冲突怎么解决?

```bash
# 1. 拉取最新代码
git pull origin develop

# 2. 查看冲突文件
git status

# 3. 编辑冲突文件,解决标记
# 搜索 <<<<<< 和 >>>>>>

# 4. 标记为已解决
git add 冲突文件

# 5. 完成合并
git commit
```

---

## 📖 延伸学习

### 推荐资源

#### Python学习
- [Python官方文档](https://docs.python.org/3/)
- [Real Python教程](https://realpython.com/)
- [Effective Python](https://effectivepython.com/)

#### Git学习
- [Git官方文档](https://git-scm.com/doc)
- [Pro Git书籍](https://git-scm.com/book/zh/v2)
- [Learn Git Branching](https://learngitbranching.js.org/)

#### 测试学习
- [pytest文档](https://docs.pytest.org/)
- [Python测试指南](https://realpython.com/pytest-python-testing/)

### 项目文档
- `docs/development/TOOL_TEMPLATE.md` - 工具开发模板
- `docs/development/API_DESIGN.md` - API设计规范
- `docs/reference/QUICK_REFERENCE.md` - 快速参考

---

## 🎯 下一步

完成第一个工具后,你可以:

1. **认领更复杂的任务**: 查看 `docs/team/TASK_ASSIGNMENT.md`
2. **参与代码审查**: 在GitHub上review其他人的PR
3. **改进文档**: 帮助完善项目文档
4. **优化现有工具**: 重构或增强已有功能

---

## 🆘 获取帮助

遇到问题时:

1. **查看文档**: 先查看相关文档
2. **搜索Issues**: GitHub Issues中可能已有答案
3. **询问团队**: 在团队群提问
4. **创建Issue**: 描述清楚问题并创建Issue

---

**祝你开发愉快! 🚀**

> 💡 记住: 每个高手都是从新手开始的,不要害怕提问!

---

**最后更新**: 2025-XX-XX  
**维护者**: DevKit-Zero团队
