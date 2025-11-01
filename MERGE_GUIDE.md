# 🔀 Git 分支合并指南 - 保留分支版本

## 📋 你的分支情况

根据截图,你的远程分支有:

- ✅ `main` (0036040) - 主分支
- ✅ `Lyh` (61626ea) - 你当前的分支
- 其他成员的分支:
  - `origin/Lyh` (61626ea)
  - `origin/LBY` (6dde6c3)
  - `origin/Yangdh` (283dcc7)
  - `origin/LGC` (c5640ed)
  - `origin/LUWEI` (3c2bd24)
  - `origin/LinJunyu` (52fe740)
  - `origin/main` (0036040)

## 🎯 目标

合并这些分支到 `main`,但**不删除原分支**。

---

## ✅ 解决方案

### 步骤1: 切换到main分支

```powershell
# 切换到main分支
git checkout main

# 更新main分支(拉取最新代码)
git pull origin main
```

### 步骤2: 依次合并每个分支

#### 方式A: 使用 merge (推荐 - 保留分支历史)

```powershell
# 合并Lyh分支
git merge origin/Lyh --no-ff -m "Merge: Merge Lyh branch into main"

# 合并LBY分支
git merge origin/LBY --no-ff -m "Merge: Merge LBY branch into main"

# 合并Yangdh分支
git merge origin/Yangdh --no-ff -m "Merge: Merge Yangdh branch into main"

# 合并LGC分支
git merge origin/LGC --no-ff -m "Merge: Merge LGC branch into main"

# 合并LUWEI分支
git merge origin/LUWEI --no-ff -m "Merge: Merge LUWEI branch into main"

# 合并LinJunyu分支
git merge origin/LinJunyu --no-ff -m "Merge: Merge LinJunyu branch into main"
```

**选项说明**:
- `--no-ff`: 创建merge commit(而不是fast-forward),保留分支历史
- `-m "message"`: 提交信息

#### 方式B: 使用 rebase (历史更清晰)

```powershell
# 变基(如果没有冲突)
git rebase origin/Lyh

# 继续其他分支...
git rebase origin/LBY
```

### 步骤3: 解决冲突(如果有)

如果合并时有冲突:

```powershell
# 1. 查看冲突的文件
git status

# 2. 手动编辑冲突文件,保留需要的代码

# 3. 标记为已解决
git add 冲突文件名

# 4. 继续合并
git merge --continue

# 或中止合并
git merge --abort
```

### 步骤4: 推送到远程

```powershell
# 推送合并后的main分支
git push origin main
```

### 步骤5: 验证(可选)

```powershell
# 查看合并后的日志
git log --oneline --graph --all

# 确认main分支包含所有合并
git log main --oneline | head -20
```

---

## 📊 完整自动化脚本

创建一个PowerShell脚本 `merge_branches.ps1`:

```powershell
# merge_branches.ps1
# 用途: 自动合并所有分支到main

$branches = @(
    "origin/Lyh",
    "origin/LBY",
    "origin/Yangdh",
    "origin/LGC",
    "origin/LUWEI",
    "origin/LinJunyu"
)

# 1. 切换到main
Write-Host "切换到main分支..." -ForegroundColor Green
git checkout main
git pull origin main

# 2. 依次合并
foreach ($branch in $branches) {
    Write-Host "`n合并分支: $branch" -ForegroundColor Cyan
    $branchName = $branch -replace "origin/", ""
    
    # 尝试合并
    git merge $branch --no-ff -m "Merge: Merge $branchName into main"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "警告: 合并 $branch 时出错,请手动处理!" -ForegroundColor Yellow
        Write-Host "解决冲突后,运行: git merge --continue" -ForegroundColor Yellow
        break
    }
}

# 3. 推送
Write-Host "`n推送合并结果..." -ForegroundColor Green
git push origin main

Write-Host "`n✅ 合并完成!" -ForegroundColor Green
```

运行脚本:

```powershell
# PowerShell中
.\merge_branches.ps1
```

---

## ⚠️ 冲突处理

### 如果出现冲突

```powershell
# 1. 查看冲突
git status

# 2. 编辑文件(查找 <<<<<<< 和 >>>>>>>)
# 3. 选择保留的代码
# 4. 保存文件

# 5. 标记为已解决
git add .

# 6. 完成合并
git merge --continue

# 或中止
git merge --abort
```

### 冲突示例

```python
# 冲突的文件
<<<<<<< HEAD
# main分支的代码
def function_v1():
    pass
=======
# 其他分支的代码
def function_v2():
    pass
>>>>>>> origin/Lyh
```

**解决**: 手动选择保留哪个版本,或合并两个版本

---

## 🔍 查看合并情况

### 查看分支图

```powershell
# 查看所有分支和合并历史
git log --oneline --graph --all --decorate

# 输出示例:
# * 1234567 Merge: Merge LinJunyu into main
# |\
# | * abcdefg LinJunyu分支提交
# |/
# * 1234567 Merge: Merge LUWEI into main
# |\
# | * hijklmn LUWEI分支提交
```

### 查看合并了哪些分支

```powershell
# 查看已合并到main的分支
git branch --merged main

# 查看未合并到main的分支
git branch --no-merged main
```

---

## 🎯 重要注意事项

### ✅ DO

- ✅ 在合并前拉取最新代码
- ✅ 在测试环境先测试合并
- ✅ 仔细查看冲突
- ✅ 使用 `--no-ff` 保留分支历史
- ✅ 写清晰的合并信息
- ✅ 备份main分支(可选)

### ❌ DON'T

- ❌ 不要强制合并而不解决冲突
- ❌ 不要合并时误删其他人的代码
- ❌ 不要使用 `git push -f` 覆盖历史
- ❌ 不要在没有备份的情况下合并大量分支

---

## 🛡️ 安全备份(可选但推荐)

```powershell
# 备份当前main分支
git checkout -b main_backup_2025_11_01

# 切换回main
git checkout main

# 现在可以安全地进行合并
# 如果出错可以回到备份
```

---

## 📈 推荐的合并策略

### 情景1: 所有分支独立(没有冲突)

```powershell
git checkout main
git pull origin main

git merge origin/Lyh --no-ff -m "Merge: Lyh features"
git merge origin/LBY --no-ff -m "Merge: LBY features"
git merge origin/Yangdh --no-ff -m "Merge: Yangdh features"
git merge origin/LGC --no-ff -m "Merge: LGC features"
git merge origin/LUWEI --no-ff -m "Merge: LUWEI features"
git merge origin/LinJunyu --no-ff -m "Merge: LinJunyu features"

git push origin main
```

### 情景2: 分支之间有依赖

```powershell
# 先合并基础分支
git checkout main
git merge origin/LBY --no-ff -m "Merge: Base features (LBY)"

# 再合并依赖分支
git merge origin/Lyh --no-ff -m "Merge: Features on top of LBY (Lyh)"
git merge origin/Yangdh --no-ff -m "Merge: Additional features (Yangdh)"

git push origin main
```

### 情景3: 有冲突需要手动处理

```powershell
git checkout main
git pull origin main

# 尝试合并,可能失败
git merge origin/Lyh --no-ff -m "Merge: Lyh"

# 如果有冲突
# 1. 编辑文件解决冲突
# 2. git add .
# 3. git merge --continue
# 4. 完成后继续其他分支
```

---

## 📞 获取帮助

### 查看合并状态

```powershell
# 查看当前merge状态
git status

# 查看冲突文件
git diff --name-only --diff-filter=U

# 查看具体冲突
git diff --name-only
```

### 撤销合并

```powershell
# 撤销最后一次合并
git reset --hard HEAD~1

# 或使用revert(保留历史)
git revert -m 1 <merge-commit-hash>
```

---

## ✨ 完整示例

```powershell
# 1. 准备
cd D:\Cityu\SEMA\CS5351\Project\devkit
git fetch origin  # 更新远程分支信息

# 2. 备份
git checkout -b main_backup

# 3. 开始合并
git checkout main
git pull origin main

# 4. 合并Lyh
git merge origin/Lyh --no-ff -m "Merge: Merge Lyh branch (formatter tool)"

# 5. 处理可能的冲突
# ...

# 6. 继续其他分支
git merge origin/LBY --no-ff -m "Merge: Merge LBY branch"
git merge origin/Yangdh --no-ff -m "Merge: Merge Yangdh branch"
git merge origin/LGC --no-ff -m "Merge: Merge LGC branch"
git merge origin/LUWEI --no-ff -m "Merge: Merge LUWEI branch"
git merge origin/LinJunyu --no-ff -m "Merge: Merge LinJunyu branch"

# 7. 推送
git push origin main

# 8. 验证
git log --oneline --graph --all | head -30
```

---

**最后更新**: 2025-11-01  
**相关文档**: `docs/team/TEAM_GUIDELINES.md` - Git工作流部分
