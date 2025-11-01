# DevKit-Zero: 项目章程与开发计划

**文档版本:** 1.0
**最后更新:** 2025-09-26

---

## 目录

1. [项目概览](#1-项目概览)
   * [1.1 项目愿景](#11-项目愿景)
   * [1.2 灵感来源](#12-灵感来源)
   * [1.3 核心技术栈](#13-核心技术栈)
2. [团队角色与职责](#2-团队角色与职责)
3. [开发与协作规范](#3-开发与协作规范)
   * [3.1 代码规范](#31-代码规范)
   * [3.2 Git 工作流](#32-git-工作流)
   * [3.3 测试与质量保证](#33-测试与质量保证)
4. [敏捷开发计划](#4-敏捷开发计划)
   * [4.1 产品待办事项列表 (Product Backlog)](#41-产品待办事项列表-product-backlog)
   * [4.2 冲刺计划 (Sprints)](#42-冲刺计划-sprints)
5. [打包与交付计划](#5-打包与交付计划)
   * [5.1 打包工具](#51-打包工具)
   * [5.2 打包策略](#52-打包策略)

---

## 1. 项目概览

### 1.1 项目愿景

打造一个轻量级、零依赖、功能强大的 **开发者工具箱 (`DevKit-Zero`)**，通过统一的命令行界面 (CLI) 和最终的图形界面 (GUI/Web)，解决开发者在代码处理、文本操作和环境辅助方面的高频需求。

### 1.2 核心技术栈

* **核心语言:** Python 3
* **核心库:** `argparse`, `pytest`, `difflib`, `psutil`
* **集成库:** `black`, `js-beautify`, `flake8`, `markdown`
* **UI 方案:** `PyQt/Tkinter` (桌面端), `Flask` (Web端)
* **打包工具:** `PyInstaller`

## 2. 团队角色与职责

* **同学 A (产品主导 & 开发者):** #产品 #测试 #核心开发
* **同学 B (技术主导 & 开发者):** #架构 #DevOps #核心开发
* **同学 C, D, E, F (核心开发者):** #核心开发

## 3. 开发与协作规范

### 3.1 代码规范

* **Python:** 严格遵循 **PEP 8** 风格。提交代码前必须使用 `black` 进行自动格式化，并使用 `flake8` 进行静态检查。
* **JavaScript:** 遵循 **Prettier** 的默认风格，使用 `js-beautify` 进行格式化。

### 3.2 Git 工作流

采用基于功能分支的 Git 工作流。

* **分支说明:**

  * `main`: **主分支**，始终保持可发布状态。
  * `develop`: **开发分支**，所有新功能的集成点。
  * `feature/<feature-name>`: **功能分支** (例如 `feature/formatter`)，用于开发新功能。
  * `fix/<fix-name>`: **修复分支**，用于修复 `develop` 分支的 Bug。
* **提交信息规范 (Conventional Commits):**

  * 格式: `<类型>: <主题>`
  * **类型:** `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
  * **示例:** `feat: Add python formatting support for formatter tool`

### 3.3 测试与质量保证

* **单元测试:** 所有核心功能必须编写 `pytest` 单元测试。
* **代码审查:** 所有向 `develop` 分支合并的 Pull Request 必须由至少一名其他成员审查通过。
* **持续集成 (CI):** 使用 GitHub Actions 自动化执行代码检查和单元测试，确保只有通过检查的代码才能被合并。

## 4. 敏捷开发计划

### 4.1 产品待办事项列表 (Product Backlog)

| 优先级         | 用户故事 (User Story)                                          | 涉及工具             | 估算 (Story Points) |
| :------------- | :------------------------------------------------------------- | :------------------- | :------------------ |
| **高**   | 作为开发者，我希望能快速格式化 Python 和 JS 代码               | `formatter`        | 8                   |
| **高**   | 作为开发者，我希望能快速生成 UUID 或随机字符串                 | `random-gen`       | 5                   |
| **高**   | 作为开发者，我希望能方便地对比两段文本或代码片段的差异         | `diff-tool`        | 5                   |
| **高**   | 作为项目负责人，我希望项目有自动化测试和 CI/CD 流程来保证质量  | CI/CD                | 8                   |
| **中**   | 作为开发者，我希望能在不同格式（如 JSON, YAML, CSV）间转换数据 | `converter`        | 8                   |
| **中**   | 作为开发者，我希望能对 Python 代码进行静态检查，发现潜在问题   | `linter`           | 5                   |
| **中**   | 作为开发者，我希望能交互式地测试正则表达式                     | `regex-tester`     | 5                   |
| **低**   | 作为开发者，我希望能批量重命名文件                             | `batch-process`    | 8                   |
| **低**   | 作为开发者，我希望能实时预览 Markdown 文件的渲染效果           | `markdown-preview` | 8                   |
| **低**   | 作为开发者，我希望能快速检查某个端口是否被占用，并找出对应进程 | `port-checker`     | 5                   |
| **待定** | 作为普通用户，我希望能通过图形界面（GUI/Web）使用这些工具      | UI                   | 13                  |
| **待定** | 作为用户，我希望能一键安装和运行整个工具集（如 .exe 文件）     | 打包                 | 8                   |

### 4.2 冲刺计划 (Sprints)

采用为期 2 周的 Sprint 周期。

* **Sprint 1: MVP & 流程建立**

  * **目标:** 交付首批核心工具 (`formatter`, `diff-tool`, `random-gen`)，并搭建项目骨架和测试环境。
* **Sprint 2: 增强工具集 & 自动化**

  * **目标:** 开发 `converter`, `linter`, `regex-tester`，并建立 CI/CD 自动化流程。
* **Sprint 3: 高级辅助工具**

  * **目标:** 开发 `batch-process`, `port-checker`, `markdown-preview`，并进行 UI 技术预研。
* **Sprint 4: UI 集成与打包发布**

  * **目标:** 根据技术预研结果，为工具集开发图形界面 (GUI 或 Web)，并完成最终打包。

## 5. 打包与交付计划

### 5.1 打包工具

我们将使用 **`PyInstaller`** 将 Python 项目打包成独立的可执行文件（例如 Windows 上的 `.exe`），实现真正的“零依赖”交付。

### 5.2 打包策略

1. **安装:**

   ```bash
   pip install pyinstaller
   ```
2. **打包纯 CLI 应用:**

   ```bash
   pyinstaller --onefile --name DevKit-Zero main.py
   ```
3. **打包 GUI 桌面应用:**

   * 使用 `--noconsole` 参数隐藏运行时控制台。
   * 使用 `--icon` 参数指定应用图标。

   ```bash
   pyinstaller --onefile --noconsole --name DevKit-Zero --icon=assets/app.ico main_gui.py
   ```
4. **打包 Web 应用 (Flask):**

   * 使用 `--add-data` 参数包含 `templates` 和 `static` 等非代码资源。
   * **Windows:**
     ```bash
     pyinstaller --onefile --name DevKit-Zero --add-data "templates;templates" --add-data "static;static" main_web.py
     ```
   * **macOS/Linux:**
     ```bash
     pyinstaller --onefile --name DevKit-Zero --add-data "templates:templates" --add-data "static:static" main_web.py
     ```

最终的可执行文件将在 `dist` 目录下生成。
