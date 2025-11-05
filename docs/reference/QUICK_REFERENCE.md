# ⚡ 快速参考手册

开发过程中的速查宝典,收录常用命令、代码片段和配置。

## 📋 目录
- [Git常用命令](#git常用命令)
- [Python开发](#python开发)
- [pytest测试](#pytest测试)
- [代码片段模板](#代码片段模板)
- [常见问题快速解决](#常见问题快速解决)

---

## 🔧 Git常用命令

### 日常工作流

```bash
# 1. 更新本地代码
git checkout develop
git pull origin develop

# 2. 创建功能分支
git checkout -b feature/tool-name

# 3. 查看状态
git status

# 4. 添加更改
git add file.py          # 添加单个文件
git add .                # 添加所有文件

# 5. 提交更改
git commit -m "feat(tool): add new feature"

# 6. 推送到远程
git push origin feature/tool-name

# 7. 创建Pull Request(在GitHub网页操作)
```

### 分支操作

```bash
# 查看分支
git branch              # 本地分支
git branch -a           # 所有分支

# 切换分支
git checkout branch-name

# 创建并切换
git checkout -b new-branch

# 删除分支
git branch -d branch-name      # 删除本地
git push origin --delete branch-name  # 删除远程

# 合并分支
git checkout develop
git merge feature/tool-name
```

### 撤销操作

```bash
# 撤销未提交的更改
git checkout -- file.py        # 单个文件
git checkout -- .              # 所有文件

# 撤销已add的文件
git reset HEAD file.py

# 修改最后一次提交
git commit --amend

# 回退到某个提交
git reset --soft HEAD~1        # 保留更改
git reset --hard HEAD~1        # 丢弃更改
```

### 解决冲突

```bash
# 1. 拉取最新代码时发生冲突
git pull origin develop

# 2. 查看冲突文件
git status

# 3. 编辑冲突文件,搜索并解决标记:
#    <<<<<<< HEAD
#    你的代码
#    =======
#    别人的代码
#    >>>>>>> branch-name

# 4. 标记为已解决
git add conflicted-file.py

# 5. 完成合并
git commit
```

### 提交信息模板

```bash
# 新功能
git commit -m "feat(scope): add new feature"

# Bug修复
git commit -m "fix(scope): resolve issue with X"

# 文档更新
git commit -m "docs(readme): update installation guide"

# 代码重构
git commit -m "refactor(core): simplify tool registration"

# 测试相关
git commit -m "test(formatter): add edge case tests"

# 样式调整
git commit -m "style(formatter): format code with black"
```

---

## 🐍 Python开发

### 虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 退出虚拟环境
deactivate

# 安装项目(开发模式)
pip install -e .

# 安装开发依赖
pip install -r requirements-dev.txt

# 导出依赖
pip freeze > requirements.txt
```

### 代码格式化

```bash
# Black - 代码格式化
black devkit_zero/tools/your_tool.py
black devkit_zero/                    # 整个目录

# Flake8 - 代码检查
flake8 devkit_zero/tools/your_tool.py
flake8 devkit_zero/ --max-line-length=88

# isort - 导入排序
isort devkit_zero/tools/your_tool.py
```

### 运行工具

```bash
# 方式1: CLI命令
devkit-zero tool-name [options]

# 方式2: Python模块
python -m devkit_zero.tools.tool_name [options]

# 方式3: 直接运行
python devkit_zero/tools/tool_name.py [options]

# 查看帮助
devkit-zero tool-name --help
devkit-zero --version
```

---

## 🧪 pytest测试

### 基本命令

```bash
# 运行所有测试
pytest

# 运行特定文件
pytest tests/test_tools/test_formatter.py

# 运行特定测试
pytest tests/test_tools/test_formatter.py::test_format_basic

# 详细输出
pytest -v

# 显示print输出
pytest -s

# 详细+print
pytest -v -s

# 只运行失败的测试
pytest --lf

# 运行到第一个失败就停止
pytest -x
```

### 测试覆盖率

```bash
# 查看覆盖率
pytest --cov=devkit_zero tests/

# 详细覆盖率报告
pytest --cov=devkit_zero --cov-report=html tests/

# 查看HTML报告
# Windows:
start htmlcov/index.html
# macOS:
open htmlcov/index.html
# Linux:
xdg-open htmlcov/index.html
```

### 测试过滤

```bash
# 按名称过滤
pytest -k "format"               # 运行包含"format"的测试
pytest -k "not slow"             # 排除标记为"slow"的测试

# 按标记过滤
pytest -m "unit"                 # 只运行单元测试
pytest -m "not integration"      # 排除集成测试
```

---

## 📝 代码片段模板

### 新建工具文件

```python
"""
工具名称 - 简短描述

功能说明...

作者: Your Name
日期: 2025-XX-XX
"""

import argparse
import sys
from typing import Optional


def main_function(args: argparse.Namespace) -> int:
    """工具主函数"""
    try:
        # TODO: 实现功能
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def register_parser(subparsers) -> None:
    """注册CLI子命令"""
    parser = subparsers.add_parser(
        'tool-name',
        help='简短描述'
    )
    parser.add_argument('input', help='输入文件')
    parser.add_argument('-o', '--output', help='输出文件')


def main():
    """独立运行入口"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    register_parser(subparsers)
    args = parser.parse_args()
    sys.exit(main_function(args))


if __name__ == '__main__':
    main()
```

### 测试文件模板

```python
"""测试XXX工具"""
import pytest
from argparse import Namespace
from devkit_zero.tools.your_tool import main_function


def test_basic_functionality():
    """测试基础功能"""
    args = Namespace(input='test.txt', output=None)
    result = main_function(args)
    assert result == 0


def test_error_handling():
    """测试错误处理"""
    args = Namespace(input='nonexistent.txt')
    result = main_function(args)
    assert result != 0


@pytest.fixture
def sample_data():
    """测试数据fixture"""
    return {"key": "value"}


def test_with_fixture(sample_data):
    """使用fixture的测试"""
    assert sample_data["key"] == "value"
```

### 文件读写模板

```python
from pathlib import Path

# 读取文件
def read_file(path: str) -> str:
    """读取文本文件"""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return file_path.read_text(encoding='utf-8')


# 写入文件
def write_file(path: str, content: str) -> None:
    """写入文本文件"""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding='utf-8')


# JSON操作
import json

def read_json(path: str) -> dict:
    """读取JSON文件"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(path: str, data: dict) -> None:
    """写入JSON文件"""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
```

### 参数验证模板

```python
def validate_args(args: argparse.Namespace) -> bool:
    """验证参数"""
    # 检查文件存在
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}")
        return False
    
    # 检查文件扩展名
    if not args.input.endswith('.txt'):
        print("Error: Input must be a .txt file")
        return False
    
    # 检查数值范围
    if hasattr(args, 'count') and args.count < 1:
        print("Error: Count must be positive")
        return False
    
    return True
```

---

## 🚨 常见问题快速解决

### Python相关

```bash
# ModuleNotFoundError
pip install -e .                # 重新安装项目

# 导入错误
pip install -r requirements-dev.txt

# 虚拟环境问题
deactivate                      # 退出当前环境
rm -rf venv                     # 删除旧环境
python -m venv venv             # 重新创建
```

### Git相关

```bash
# 忘记切换分支就修改了代码
git stash                       # 暂存更改
git checkout feature/tool-name  # 切换分支
git stash pop                   # 恢复更改

# 提交到错误的分支
git reset --soft HEAD~1         # 撤销提交
git stash                       # 暂存更改
git checkout correct-branch     # 切换到正确分支
git stash pop                   # 恢复更改
git commit -m "message"         # 重新提交

# 拉取代码冲突
git stash                       # 暂存本地更改
git pull origin develop         # 拉取远程代码
git stash pop                   # 恢复更改
# 手动解决冲突...
```

### 测试相关

```bash
# 测试失败查看详情
pytest -v -s tests/test_tools/test_your_tool.py

# 测试超时
pytest --timeout=30 tests/      # 设置超时

# 清除缓存
pytest --cache-clear tests/
rm -rf .pytest_cache __pycache__
```

---

## 🔍 VS Code快捷键

### 编辑

- `Ctrl + /`: 注释/取消注释
- `Alt + ↑/↓`: 移动行
- `Shift + Alt + ↑/↓`: 复制行
- `Ctrl + D`: 选择下一个相同内容
- `Ctrl + Shift + L`: 选择所有相同内容

### 导航

- `Ctrl + P`: 快速打开文件
- `Ctrl + Shift + F`: 全局搜索
- `F12`: 跳转到定义
- `Alt + ←/→`: 前进/后退

### 调试

- `F5`: 开始调试
- `F9`: 设置断点
- `F10`: 单步跳过
- `F11`: 单步进入

---

## 📦 项目结构速查

```
devkit_zero/
├── __init__.py          # 包初始化
├── core.py              # 核心API
├── cli.py               # CLI入口
├── gui_main.py          # GUI入口
├── tools/               # 工具模块
│   ├── __init__.py     # 工具注册
│   └── tool_name.py    # 具体工具
├── ui/                  # UI组件
└── utils/               # 工具函数
    ├── file_ops.py     # 文件操作
    ├── validators.py   # 验证函数
    └── helpers.py      # 辅助函数
```

---

## 📞 快速联系

- 📖 详细文档: `docs/README.md`
- 🆘 新手指南: `docs/team/BEGINNER_GUIDE.md`
- 🛠️ 工具模板: `docs/development/TOOL_TEMPLATE.md`
- 👥 团队规范: `docs/team/TEAM_GUIDELINES.md`

---

**版本**: v1.0  
**最后更新**: 2025-XX-XX

> 💡 **提示**: 建议打印或保存到本地,方便随时查阅!
