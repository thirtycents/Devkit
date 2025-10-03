# 📄 Templates 目录

本目录用于存放代码模板和配置模板文件。

## 📂 目录结构

```
templates/
├── tool_template.py          # 工具开发模板
├── test_template.py          # 测试文件模板  
├── github/                   # GitHub模板
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md
├── config/                   # 配置文件模板
│   ├── .vscode/
│   │   ├── settings.json
│   │   └── launch.json
│   └── pyproject.toml
└── docs/                     # 文档模板
    └── tool_documentation.md
```

## 📋 模板说明

### tool_template.py
**用途**: 创建新工具时的代码模板

**使用方法**:
```bash
# 复制模板
cp templates/tool_template.py devkit_zero/tools/your_tool.py

# 修改工具名称和功能
# 参考: docs/development/TOOL_TEMPLATE.md
```

**包含内容**:
- 标准的三个必需函数
- 完整的文档字符串
- 错误处理框架
- 参数解析示例

### test_template.py
**用途**: 创建测试文件的模板

**使用方法**:
```bash
cp templates/test_template.py tests/test_tools/test_your_tool.py
```

**包含内容**:
- 基础测试用例结构
- pytest fixture示例
- 参数化测试示例
- Mock使用示例

### GitHub模板

#### bug_report.md
**用途**: Bug报告Issue模板

**触发**: 在GitHub创建Issue时选择"Bug Report"

**包含**:
- 问题描述
- 复现步骤
- 期望行为
- 实际行为
- 环境信息

#### feature_request.md
**用途**: 功能请求Issue模板

**触发**: 在GitHub创建Issue时选择"Feature Request"

**包含**:
- 功能描述
- 使用场景
- 预期效果
- 替代方案

#### pull_request_template.md
**用途**: Pull Request描述模板

**触发**: 创建PR时自动加载

**包含**:
- 变更说明
- 测试情况
- 检查清单
- 关联Issue

### 配置模板

#### .vscode/settings.json
**用途**: VS Code项目设置

**包含**:
- Python解释器配置
- 代码格式化设置
- Linter配置

#### .vscode/launch.json
**用途**: VS Code调试配置

**包含**:
- Python文件调试配置
- 模块调试配置
- 测试调试配置

## 🔧 使用模板

### 1. 创建新工具

```bash
# 1. 复制工具模板
cp templates/tool_template.py devkit_zero/tools/my_tool.py

# 2. 复制测试模板
cp templates/test_template.py tests/test_tools/test_my_tool.py

# 3. 修改文件内容
# - 更新工具名称
# - 实现核心功能
# - 编写测试用例

# 4. 注册工具
# 在 devkit_zero/tools/__init__.py 中添加导入和注册
```

### 2. 设置开发环境

```bash
# 复制VS Code配置
cp -r templates/config/.vscode .vscode/

# 或手动创建并参考模板内容
```

### 3. 配置GitHub

```bash
# 复制GitHub模板到项目根目录
cp -r templates/github/.github .github/

# GitHub会自动识别这些模板
```

## 📝 创建自定义模板

### 添加新模板

1. **创建模板文件**
   ```bash
   touch templates/your_template.py
   ```

2. **编写模板内容**
   - 使用占位符: `{{PLACEHOLDER}}`
   - 添加清晰的注释
   - 包含使用说明

3. **更新此README**
   - 说明模板用途
   - 提供使用示例

### 模板最佳实践

✅ **应该包含的内容**:
- 完整的框架结构
- TODO标记需要修改的地方
- 清晰的注释说明
- 使用示例

❌ **避免的内容**:
- 具体的业务逻辑
- 硬编码的值
- 过于复杂的实现

## 🎨 模板变量约定

在模板中使用占位符时,遵循以下约定:

```python
"""
{{TOOL_NAME}} - {{TOOL_DESCRIPTION}}

Author: {{AUTHOR_NAME}}
Date: {{CREATION_DATE}}
"""

class {{CLASS_NAME}}:
    """{{CLASS_DESCRIPTION}}"""
    
    def __init__(self):
        self.{{ATTRIBUTE_NAME}} = {{DEFAULT_VALUE}}
```

**约定**:
- 使用大写: `{{PLACEHOLDER}}`
- 见名知意: `{{TOOL_NAME}}` 而非 `{{VAR1}}`
- 在注释中说明每个占位符的含义

## 🔄 模板更新

### 更新流程

1. 修改模板文件
2. 测试模板可用性
3. 更新文档
4. 通知团队成员

### 版本控制

模板文件应纳入版本控制:
```bash
git add templates/
git commit -m "docs(templates): update tool template"
```

## 📚 相关文档

- [工具开发模板文档](../docs/development/TOOL_TEMPLATE.md)
- [新手开发指南](../docs/team/BEGINNER_GUIDE.md)
- [API设计规范](../docs/development/API_DESIGN.md)

---

**提示**: 模板是为了提高效率,不是限制创造力。根据实际需求灵活调整!

**最后更新**: 2025-XX-XX
