# DevKit-Zero Project Framework

> 🎯 **Team Collaboration Project** - A project framework designed for team collaboration, including complete development standards and documentation.

[![Python Support](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Introduction

**DevKit-Zero** is a lightweight, zero-dependency developer toolkit framework. This repository provides a complete project structure and development standards, suitable for collaborative development.

### 🎯 Project Goals
- Develop 9 practical developer tools
- Support **CLI**, **GUI**, and **Library Import** modes
- Zero-dependency design (using only Python standard library)
- Complete documentation and testing system

## 🚀 Quick Start

### 1. Clone Project
```bash
git clone <your-repo-url>
cd devkit
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Install Development Dependencies
```bash
pip install -r requirements-dev.txt
pip install -e .
```

### 4. Run Project

#### 🖥️ GUI Mode
```bash
# Windows: Double click to run
start_gui.bat

# Or use command line
python -m devkit_zero.gui_main
```

#### ⌨️ CLI Mode
```bash
# View all available commands
python -m devkit_zero.cli --help

# Use specific tools
python -m devkit_zero.cli format --file test.py
python -m devkit_zero.cli random uuid
python -m devkit_zero.cli regex "\d+" "Hello 123"
python -m devkit_zero.cli robots_checker https://google.com
```

#### 📦 Library Usage
```python
from devkit_zero.tools import formatter, regex_tester

# Format code
code, error = formatter.format_code("def test():pass", "python")
print(code)

# Test regex
tester = regex_tester.RegexTester()
result = tester.test_pattern(r'\d+', 'Hello 123')
print(result)
```

### 5. Run Tests
```bash
pytest
```

## 📁 Project Structure

```
devkit/
├── devkit_zero/              # Main package directory
│   ├── __init__.py          # Package init
│   ├── __version__.py       # Version info
│   ├── core.py              # Core API
│   ├── cli.py               # CLI entry point
│   ├── gui_main.py          # GUI entry point
│   ├── tools/               # Tool modules
│   │   ├── __init__.py      # Tool registration
│   │   ├── formatter.py     # Code formatter
│   │   ├── random_gen.py    # Random generator
│   │   ├── diff_tool.py     # Diff tool
│   │   ├── converter.py     # Format converter
│   │   ├── linter.py        # Linter
│   │   ├── regex_tester.py  # Regex tester
│   │   ├── batch_process.py # Batch processor
│   │   ├── markdown_preview.py # Markdown preview
│   │   └── port_checker.py  # Port checker
│   ├── ui/                  # UI modules
│   │   ├── __init__.py
│   │   └── gui_app.py       # GUI application
│   └── utils/               # Utility functions
│       └── __init__.py
├── tests/                   # Tests directory
│   ├── conftest.py         # Test configuration
│   └── test_tools/         # Tool tests
│       └── (Create test file for each tool)
├── docs/                    # 📚 Documentation Center
│   ├── README.md           # Documentation navigation
│   ├── team/               # Team collaboration docs
│   │   ├── BEGINNER_GUIDE.md
│   │   ├── TEAM_GUIDELINES.md
│   │   └── TASK_ASSIGNMENT.md
│   ├── development/        # Development docs
│   │   ├── PROJECT_FRAMEWORK.md
│   │   ├── TOOL_TEMPLATE.md
│   │   └── API_DESIGN.md
│   └── reference/          # Reference docs
│       └── QUICK_REFERENCE.md
├── assets/                  # Assets
├── templates/               # Code templates
├── static/                  # Static files
├── .github/                # GitHub config
│   └── workflows/          # CI/CD (Optional)
├── .gitignore              # Git ignore
├── setup.py                # Setup script
├── pyproject.toml          # Project metadata
├── requirements.txt        # Runtime dependencies
├── requirements-dev.txt    # Dev dependencies
├── CHANGELOG.md            # Changelog
└── README.md               # This file
```

## 🛠️ Tools to Implement

### 1. formatter (Code Formatter)
- **Owner**: TBD
- **Function**: Python/JavaScript code formatting
- **Priority**: High

### 2. random_gen (Random Data Generator)
- **Owner**: TBD
- **Function**: Generate UUID, passwords, random numbers
- **优先级**: 高

### 3. diff_tool (文件差异比较)
- **负责人**: 待分配
- **功能**: 比较文本/文件差异
- **优先级**: 中

### 4. converter (格式转换器)
- **负责人**: 待分配
- **功能**: JSON/CSV/YAML格式转换
- **优先级**: 中

### 5. linter (代码检查器)
- **负责人**: 待分配
- **功能**: 基础的Python代码检查
- **优先级**: 中

### 6. regex_tester (正则表达式测试器)
- **负责人**: 待分配
- **功能**: 正则表达式匹配测试
- **优先级**: 低

### 7. batch_process (批量处理器)
- **负责人**: 待分配
- **功能**: 批量文件重命名/处理
- **优先级**: 低

### 8. markdown_preview (Markdown预览)
- **负责人**: 待分配
- **功能**: Markdown转HTML
- **优先级**: 低

### 9. port_checker (端口检查器)
- **负责人**: 待分配
- **功能**: 检查端口占用情况
- **优先级**: 低

## 📚 重要文档

### 👥 团队必读
- **[新手开发指南](docs/team/BEGINNER_GUIDE.md)** - 从零开始的完整教程
- **[团队协作规范](docs/team/TEAM_GUIDELINES.md)** - Git工作流和代码规范
- **[任务分配表](docs/team/TASK_ASSIGNMENT.md)** - 谁负责什么功能

### 🔧 开发参考
- **[项目框架说明](docs/development/PROJECT_FRAMEWORK.md)** - 架构设计详解
- **[工具开发模板](docs/development/TOOL_TEMPLATE.md)** - 标准开发流程
- **[API设计规范](docs/development/API_DESIGN.md)** - 接口设计标准

### 🚀 快速参考
- **[快速参考卡](docs/reference/QUICK_REFERENCE.md)** - 常用命令和模板

## 🎯 开发流程

### Step 1: 选择任务
1. 查看 [任务分配表](docs/team/TASK_ASSIGNMENT.md)
2. 选择一个未分配的工具
3. 在GitHub Issue中认领任务

### Step 2: 创建分支
```bash
git checkout -b feature/tool-name
```

### Step 3: 开发功能
1. 按照 [工具开发模板](docs/development/TOOL_TEMPLATE.md) 实现功能
2. 编写测试用例
3. 更新文档

### Step 4: 提交代码
```bash
git add .
git commit -m "feat: implement tool-name"
git push origin feature/tool-name
```

### Step 5: 创建Pull Request
- 填写PR描述
- 等待代码审查
- 根据反馈修改

## ✅ 代码提交规范

```bash
feat: 新功能
fix: 修复bug
docs: 文档更新
test: 测试相关
refactor: 重构代码
style: 代码格式
chore: 构建/工具
```

示例：
```bash
git commit -m "feat: add formatter tool with Python support"
git commit -m "test: add unit tests for random_gen"
git commit -m "docs: update README with usage examples"
```

## 🧪 测试规范

每个工具模块都需要：
- 单元测试（至少3个测试用例）
- 边界测试（空值、异常输入）
- 文档字符串

运行测试：
```bash
# 所有测试
pytest

# 特定模块
pytest tests/test_tools/test_formatter.py

# 测试覆盖率
pytest --cov=devkit_zero
```

## 🤝 团队协作

### 沟通渠道
- **GitHub Issues**: 任务跟踪和bug报告
- **Pull Request**: 代码审查和讨论
- **微信群**: 日常沟通

### 代码审查
- 每个PR至少需要1人审查
- 所有测试必须通过
- 遵循代码规范

### 遇到问题？
1. 查看 [新手开发指南](docs/team/BEGINNER_GUIDE.md)
2. 查看 [快速参考卡](docs/reference/QUICK_REFERENCE.md)
3. 在团队群提问
4. 创建GitHub Issue

## 📊 项目进度

- [ ] 项目框架搭建
- [ ] 文档编写完成
- [ ] 任务分配
- [ ] 工具开发（0/9）
- [ ] 测试覆盖（0%）
- [ ] GUI界面
- [ ] 发布v1.0

## 📝 License

MIT License - 详见 LICENSE 文件

## 🌟 贡献者

感谢所有为这个项目做出贡献的同学！

<!-- 项目完成后添加贡献者列表 -->

---

**准备好开始了吗？** 从 [新手开发指南](docs/team/BEGINNER_GUIDE.md) 开始你的开发之旅！🚀
