# 👥 团队协作规范

## 🎯 协作原则

### 核心价值观
- **代码质量优先**: 宁可晚交也不要低质量代码
- **及时沟通**: 遇到问题立即反馈,不要拖延
- **相互尊重**: 尊重每个人的代码和想法
- **持续学习**: 在项目中成长和提升

## 📋 Git工作流

### 分支策略

```
main (主分支,稳定版本)
  ├── develop (开发分支,日常开发)
  │     ├── feature/formatter (功能分支)
  │     ├── feature/random-gen (功能分支)
  │     └── feature/diff-tool (功能分支)
  └── hotfix/fix-bug (紧急修复)
```

### 分支命名规范

| 类型 | 命名格式 | 示例 | 说明 |
|------|---------|------|------|
| 功能开发 | `feature/工具名` | `feature/formatter` | 新工具开发 |
| Bug修复 | `bugfix/问题描述` | `bugfix/cli-crash` | 修复bug |
| 紧急修复 | `hotfix/问题描述` | `hotfix/security-issue` | 紧急问题 |
| 文档更新 | `docs/文档类型` | `docs/api-reference` | 文档修改 |
| 测试相关 | `test/测试内容` | `test/formatter` | 测试代码 |

### 工作流程

#### 1. 开始新任务

```bash
# 1. 更新本地代码
git checkout develop
git pull origin develop

# 2. 创建功能分支
git checkout -b feature/your-tool-name

# 3. 开始开发...
```

#### 2. 日常开发

```bash
# 1. 写代码...

# 2. 提交代码(频繁小提交)
git add .
git commit -m "feat(formatter): add basic formatting logic"

# 3. 定期推送到远程
git push origin feature/your-tool-name
```

#### 3. 完成功能

```bash
# 1. 确保代码通过测试
pytest tests/test_tools/test_your_tool.py

# 2. 更新develop分支
git checkout develop
git pull origin develop

# 3. 合并最新代码到功能分支
git checkout feature/your-tool-name
git merge develop

# 4. 解决冲突(如有)

# 5. 推送并创建PR
git push origin feature/your-tool-name
```

## 💬 提交信息规范

### 提交类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(formatter): add JSON formatting` |
| `fix` | Bug修复 | `fix(cli): resolve argument parsing error` |
| `docs` | 文档更新 | `docs(readme): update installation guide` |
| `style` | 代码格式 | `style(formatter): format code with black` |
| `refactor` | 重构 | `refactor(core): simplify tool registration` |
| `test` | 测试相关 | `test(formatter): add edge case tests` |
| `chore` | 构建/工具 | `chore(deps): update requirements.txt` |

### 提交格式

```
<类型>(<范围>): <简短描述>

<详细描述>(可选)

<关联Issue>(可选)
```

### 示例

```bash
# 好的提交信息 ✅
git commit -m "feat(formatter): add Python code formatting support"
git commit -m "fix(cli): handle missing config file gracefully"
git commit -m "docs(api): add docstrings to core functions"

# 不好的提交信息 ❌
git commit -m "update"
git commit -m "fix bug"
git commit -m "修改代码"
```

## 🔍 Pull Request规范

### PR标题格式

```
[类型] 简短描述 (#Issue编号)
```

示例:
- `[Feature] Add code formatter tool (#12)`
- `[Bugfix] Fix CLI argument parsing (#23)`
- `[Docs] Update API documentation (#15)`

### PR描述模板

```markdown
## 📝 变更说明
简要描述此PR的目的和内容

## 🎯 实现内容
- [ ] 实现了XXX功能
- [ ] 添加了XXX测试
- [ ] 更新了相关文档

## 🧪 测试情况
- [ ] 所有测试通过
- [ ] 新增测试覆盖率: XX%
- [ ] 手动测试场景: ...

## 📸 截图(如适用)
(如果是UI相关的改动,添加截图)

## 🔗 关联Issue
Closes #XX (或 Relates to #XX)

## ✅ 检查清单
- [ ] 代码符合PEP 8规范
- [ ] 添加了docstring
- [ ] 编写了单元测试
- [ ] 更新了CHANGELOG.md
- [ ] 更新了相关文档
```

### PR审查清单

#### 代码审查者要检查:
- [ ] 代码逻辑正确
- [ ] 符合代码规范
- [ ] 有适当的注释
- [ ] 有完整的测试
- [ ] 文档已更新
- [ ] 没有引入新的依赖(或已讨论)

#### 审查步骤:
1. **快速浏览**: 理解PR的目的
2. **详细检查**: 逐行审查代码
3. **测试验证**: 拉取分支本地测试
4. **提供反馈**: 建设性的评论
5. **批准或请求修改**

### 审查反馈示例

```markdown
# 好的反馈 ✅
"这个函数可以考虑拆分成两个,提高可读性。建议在第XX行..."

"测试用例很完善!不过建议添加一个边界情况的测试: ..."

"代码逻辑清晰,LGTM! 👍"

# 不好的反馈 ❌
"这段代码不好"
"重写这部分"
"代码有问题"
```

## 🧪 测试规范

### 测试要求
- **覆盖率**: 每个工具至少80%测试覆盖
- **测试类型**: 单元测试 + 集成测试
- **测试命名**: `test_功能_场景()`

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定文件
pytest tests/test_tools/test_formatter.py

# 查看覆盖率
pytest --cov=devkit_zero tests/

# 详细输出
pytest -v -s
```

### 测试编写示例

```python
def test_formatter_basic_formatting():
    """测试基础格式化功能"""
    # Arrange (准备)
    input_code = "x=1"
    expected = "x = 1"
    
    # Act (执行)
    result = format_code(input_code)
    
    # Assert (断言)
    assert result == expected

def test_formatter_handles_invalid_input():
    """测试处理无效输入"""
    with pytest.raises(ValueError):
        format_code(None)
```

## 📝 代码规范

### Python编码标准

#### 1. PEP 8基本规范
```python
# 好的代码 ✅
def format_code(source: str, indent: int = 4) -> str:
    """
    格式化Python代码
    
    Args:
        source: 源代码字符串
        indent: 缩进空格数
        
    Returns:
        格式化后的代码
    """
    if not source:
        raise ValueError("Source code cannot be empty")
    return formatted_code

# 不好的代码 ❌
def fmt(s,i=4):
    if not s:return None
    return s
```

#### 2. 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 模块 | 小写+下划线 | `random_gen.py` |
| 类 | 大驼峰 | `CodeFormatter` |
| 函数 | 小写+下划线 | `format_code()` |
| 常量 | 大写+下划线 | `MAX_LINE_LENGTH` |
| 私有 | 前缀下划线 | `_internal_helper()` |

#### 3. 文档字符串
```python
def main_function(args: argparse.Namespace) -> int:
    """
    工具的主要功能函数
    
    Args:
        args: 解析后的命令行参数
        
    Returns:
        退出代码,0表示成功,非0表示失败
        
    Raises:
        ValueError: 当输入参数无效时
        IOError: 当文件操作失败时
        
    Example:
        >>> args = argparse.Namespace(input='file.txt')
        >>> result = main_function(args)
        >>> print(result)
        0
    """
    pass
```

### 导入规范

```python
# 标准库
import os
import sys
from pathlib import Path

# 第三方库(如有)
# import requests

# 本地模块
from devkit_zero.utils.helpers import validate_input
from devkit_zero.core import ToolBase
```

## 🐛 问题处理流程

### 发现Bug

1. **立即报告**
   ```bash
   # 在GitHub创建Issue
   标题: [Bug] 简短描述
   标签: bug, 优先级标签
   ```

2. **提供详细信息**
   - 复现步骤
   - 错误信息
   - 系统环境
   - 预期行为

3. **认领修复**
   ```bash
   # 评论说明你要修复
   "我来修复这个bug"
   ```

4. **创建修复分支**
   ```bash
   git checkout -b bugfix/issue-XX-description
   ```

## 📅 团队会议

### 周会制度
- **时间**: 每周X下午X点
- **时长**: 30-60分钟
- **形式**: 线上/线下

### 会议议程
1. 上周进度回顾
2. 遇到的问题讨论
3. 本周计划
4. 技术分享(可选)

### 日常沟通
- **紧急问题**: 微信群 @相关人员
- **一般问题**: GitHub Issues
- **代码讨论**: Pull Request评论
- **设计讨论**: GitHub Discussions

## 🎯 最佳实践

### DO ✅
- ✅ 频繁提交小的改动
- ✅ 写清晰的提交信息
- ✅ 及时更新文档
- ✅ 积极参与代码审查
- ✅ 遇到问题及时沟通
- ✅ 保持代码整洁

### DON'T ❌
- ❌ 直接推送到main或develop
- ❌ 提交未测试的代码
- ❌ 忽略代码审查意见
- ❌ 修改他人代码不沟通
- ❌ 拖延问题不报告
- ❌ 一次性提交大量代码

## 🆘 获取帮助

### 文档资源
1. `docs/team/BEGINNER_GUIDE.md` - 新手指南
2. `docs/development/TOOL_TEMPLATE.md` - 开发模板
3. `docs/reference/QUICK_REFERENCE.md` - 快速参考

### 提问技巧
1. **先自己尝试**: 查看文档和已有Issues
2. **清楚描述**: 说明你做了什么,期望什么,实际发生了什么
3. **提供上下文**: 代码片段,错误信息,环境信息
4. **及时反馈**: 问题解决后更新Issue

---

**版本**: v1.0  
**最后更新**: 2025-XX-XX  
**维护者**: 项目管理团队

> 💡 **记住**: 良好的协作规范是项目成功的关键!
