# DevKit-Zero 项目框架

> 🎯 **团队协作项目** - 这是一个为团队协作准备的项目框架，包含完整的开发规范和指导文档

[![Python Support](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 项目简介

**DevKit-Zero** 是一个轻量级、零依赖的开发者工具箱项目框架。本仓库提供完整的项目结构和开发规范，适合团队协作开发。

### 🎯 项目目标
- 开发9个实用的开发者工具
- 支持CLI、GUI和库导入三种使用方式
- 零依赖设计（仅使用Python标准库）
- 完整的文档和测试体系

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd devkit
```

### 2. 创建虚拟环境
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. 安装开发依赖
```bash
pip install -r requirements-dev.txt
pip install -e .
```

### 4. 运行测试
```bash
pytest
```

## 📁 项目结构

```
devkit/
├── devkit_zero/              # 主包目录
│   ├── __init__.py          # 包初始化（需要实现）
│   ├── __version__.py       # 版本信息（需要实现）
│   ├── core.py              # 核心API（需要实现）
│   ├── cli.py               # CLI入口（需要实现）
│   ├── gui_main.py          # GUI入口（需要实现）
│   ├── tools/               # 工具模块目录
│   │   ├── __init__.py      # 工具注册（需要实现）
│   │   ├── formatter.py     # 待实现
│   │   ├── random_gen.py    # 待实现
│   │   ├── diff_tool.py     # 待实现
│   │   ├── converter.py     # 待实现
│   │   ├── linter.py        # 待实现
│   │   ├── regex_tester.py  # 待实现
│   │   ├── batch_process.py # 待实现
│   │   ├── markdown_preview.py # 待实现
│   │   └── port_checker.py  # 待实现
│   ├── ui/                  # UI模块
│   │   ├── __init__.py
│   │   └── gui_app.py       # 待实现
│   └── utils/               # 工具函数
│       └── __init__.py
├── tests/                   # 测试目录
│   ├── conftest.py         # 测试配置（需要实现）
│   └── test_tools/         # 工具测试
│       └── （为每个工具创建测试文件）
├── docs/                    # 📚 文档中心
│   ├── README.md           # 文档导航
│   ├── team/               # 团队协作文档
│   │   ├── BEGINNER_GUIDE.md
│   │   ├── TEAM_GUIDELINES.md
│   │   └── TASK_ASSIGNMENT.md
│   ├── development/        # 开发文档
│   │   ├── PROJECT_FRAMEWORK.md
│   │   ├── TOOL_TEMPLATE.md
│   │   └── API_DESIGN.md
│   └── reference/          # 参考文档
│       └── QUICK_REFERENCE.md
├── assets/                  # 资源文件
├── templates/               # 代码模板
├── static/                  # 静态文件
├── .github/                # GitHub配置
│   └── workflows/          # CI/CD（可选）
├── .gitignore              # Git忽略配置
├── setup.py                # 安装配置
├── pyproject.toml          # 项目元数据
├── requirements.txt        # 运行依赖
├── requirements-dev.txt    # 开发依赖
├── CHANGELOG.md            # 版本记录
└── README.md               # 本文件
```

## 🛠️ 需要实现的工具

### 1. formatter (代码格式化器)
- **负责人**: 待分配
- **功能**: Python/JavaScript代码格式化
- **优先级**: 高

### 2. random_gen (随机数据生成器)
- **负责人**: 待分配
- **功能**: 生成UUID、密码、随机数
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
