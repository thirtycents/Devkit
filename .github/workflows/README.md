# ⚙️ GitHub Workflows 目录

本目录用于存放GitHub Actions的CI/CD工作流配置文件。

## 📂 目录结构

```
.github/
├── workflows/              # 工作流配置
│   ├── ci.yml             # 持续集成
│   ├── release.yml        # 发布流程
│   └── docs.yml           # 文档部署
│
├── ISSUE_TEMPLATE/        # Issue模板
│   ├── bug_report.md
│   └── feature_request.md
│
└── pull_request_template.md  # PR模板
```

## 🚀 工作流说明

### ci.yml - 持续集成

**触发条件**:
- Push到main或develop分支
- 创建Pull Request

**执行步骤**:
```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -e .
          pip install -r requirements-dev.txt
      
      - name: Lint with flake8
        run: flake8 devkit_zero/
      
      - name: Test with pytest
        run: pytest --cov=devkit_zero tests/
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

**作用**:
- ✅ 多版本Python测试
- ✅ 代码风格检查
- ✅ 运行单元测试
- ✅ 生成覆盖率报告

### release.yml - 自动发布

**触发条件**:
- 推送标签: `v*.*.*`

**执行步骤**:
```yaml
name: Release

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  release:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Build package
        run: |
          pip install build
          python -m build
      
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          draft: false
          prerelease: false
      
      - name: Publish to PyPI (可选)
        run: |
          pip install twine
          twine upload dist/*
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
```

**作用**:
- 📦 自动打包
- 🏷️ 创建GitHub Release
- 📤 发布到PyPI(可选)

### docs.yml - 文档部署

**触发条件**:
- Push到main分支(docs目录变更)

**执行步骤**:
```yaml
name: Deploy Docs

on:
  push:
    branches: [main]
    paths:
      - 'docs/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

**作用**:
- 📚 自动部署文档到GitHub Pages

## 🔧 配置GitHub Actions

### 1. 创建工作流文件

```bash
# 创建目录
mkdir -p .github/workflows

# 创建CI配置
touch .github/workflows/ci.yml

# 编辑配置文件...
```

### 2. 设置Secrets

在GitHub仓库设置中添加:

- `PYPI_TOKEN`: PyPI发布令牌(如需发布)
- `CODECOV_TOKEN`: Codecov上传令牌(如需代码覆盖率)

**设置路径**:
```
GitHub仓库 → Settings → Secrets and variables → Actions
```

### 3. 启用Actions

确保Actions已启用:
```
GitHub仓库 → Settings → Actions → General
勾选 "Allow all actions and reusable workflows"
```

## 📋 常用工作流模式

### 代码质量检查

```yaml
- name: Code Quality
  run: |
    pip install black flake8 mypy
    black --check devkit_zero/
    flake8 devkit_zero/ --max-line-length=88
    mypy devkit_zero/
```

### 多操作系统测试

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: [3.8, 3.9, '3.10', 3.11]

runs-on: ${{ matrix.os }}
```

### 缓存依赖

```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

### 安全扫描

```yaml
- name: Security Check
  run: |
    pip install safety
    safety check --file requirements.txt
```

## 🎯 工作流最佳实践

### DO ✅

1. **快速失败**
   ```yaml
   jobs:
     test:
       steps:
         - name: Lint (快速检查)
           run: flake8 .
         - name: Test (较慢)
           run: pytest
   ```

2. **使用缓存**
   ```yaml
   - uses: actions/cache@v3
   ```

3. **矩阵测试**
   ```yaml
   strategy:
     matrix:
       python-version: [3.8, 3.9, '3.10']
   ```

4. **条件执行**
   ```yaml
   - name: Deploy
     if: github.ref == 'refs/heads/main'
   ```

### DON'T ❌

1. ❌ 不要在workflow中硬编码密钥
   ```yaml
   # 错误
   env:
     API_KEY: "sk-1234567890"
   
   # 正确
   env:
     API_KEY: ${{ secrets.API_KEY }}
   ```

2. ❌ 不要在每次push都运行耗时任务
   ```yaml
   # 限制触发条件
   on:
     push:
       branches: [main]
   ```

3. ❌ 不要忽略失败
   ```yaml
   # 确保失败时工作流失败
   - name: Test
     run: pytest
     # 不要使用 continue-on-error: true
   ```

## 📊 工作流状态徽章

在README.md中添加状态徽章:

```markdown
[![CI](https://github.com/username/repo/workflows/CI/badge.svg)](https://github.com/username/repo/actions)
[![Coverage](https://codecov.io/gh/username/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/username/repo)
[![License](https://img.shields.io/github/license/username/repo)](LICENSE)
```

## 🔍 调试工作流

### 查看日志

```
GitHub仓库 → Actions → 选择工作流运行 → 查看详细日志
```

### 本地测试(使用act)

```bash
# 安装act
# macOS:
brew install act

# 运行工作流
act -j test
```

### Debug模式

```yaml
- name: Debug
  run: |
    echo "Event: ${{ github.event_name }}"
    echo "Ref: ${{ github.ref }}"
    echo "Actor: ${{ github.actor }}"
```

## 📚 有用的Actions

### 官方Actions
- [actions/checkout@v3](https://github.com/actions/checkout) - 检出代码
- [actions/setup-python@v4](https://github.com/actions/setup-python) - 设置Python
- [actions/cache@v3](https://github.com/actions/cache) - 缓存依赖

### 第三方Actions
- [codecov/codecov-action@v3](https://github.com/codecov/codecov-action) - 上传覆盖率
- [peaceiris/actions-gh-pages@v3](https://github.com/peaceiris/actions-gh-pages) - 部署GitHub Pages

## 🔗 相关资源

- [GitHub Actions文档](https://docs.github.com/en/actions)
- [工作流语法](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Actions市场](https://github.com/marketplace?type=actions)

---

**注意**:
- 工作流配置文件使用YAML格式
- 注意缩进(使用空格,不用Tab)
- 测试工作流避免在生产环境频繁运行

**待添加文件**:
- [ ] `.github/workflows/ci.yml`
- [ ] `.github/workflows/release.yml`
- [ ] `.github/workflows/docs.yml`
- [ ] `.github/ISSUE_TEMPLATE/bug_report.md`
- [ ] `.github/ISSUE_TEMPLATE/feature_request.md`
- [ ] `.github/pull_request_template.md`

**最后更新**: 2025-XX-XX
