# 🎯 分支合并步骤可视化指南

## 当前状态

```
远程仓库:
├── main (0036040)
├── Lyh (61626ea)
├── LBY (6dde6c3)
├── Yangdh (283dcc7)
├── LGC (c5640ed)
├── LUWEI (3c2bd24)
└── LinJunyu (52fe740)

目标: 将所有分支合并到main,但保留分支不删除
```

## 合并流程(分步)

### 第1步: 准备工作

```powershell
# 进入项目目录
cd D:\Cityu\SEMA\CS5351\Project\devkit

# 更新远程分支信息
git fetch origin

# 切换到main分支
git checkout main

# 拉取最新main
git pull origin main
```

### 第2步: 创建备份(可选但推荐)

```powershell
# 创建备份分支
git checkout -b main_backup_before_merge

# 切换回main
git checkout main
```

### 第3步: 合并第一个分支

```powershell
# 合并Lyh分支
git merge origin/Lyh --no-ff -m "Merge: Merge Lyh branch"

# 可能的结果:
# ✅ 成功 -> 继续下一个
# ⚠️ 冲突 -> 解决冲突后 git merge --continue
# ❌ 错误 -> git merge --abort 后处理
```

**如果有冲突:**
```powershell
# 1. 查看冲突文件
git status

# 2. 编辑文件,解决冲突
# (在编辑器中找到 <<<<<<< 和 >>>>>>>,选择要保留的代码)

# 3. 标记已解决
git add .

# 4. 完成合并
git merge --continue

# 5. 输入合并信息并保存(通常是默认信息)
```

### 第4步: 依次合并其他分支

```powershell
# 合并LBY
git merge origin/LBY --no-ff -m "Merge: Merge LBY branch"

# 合并Yangdh
git merge origin/Yangdh --no-ff -m "Merge: Merge Yangdh branch"

# 合并LGC
git merge origin/LGC --no-ff -m "Merge: Merge LGC branch"

# 合并LUWEI
git merge origin/LUWEI --no-ff -m "Merge: Merge LUWEI branch"

# 合并LinJunyu
git merge origin/LinJunyu --no-ff -m "Merge: Merge LinJunyu branch"
```

### 第5步: 推送到远程

```powershell
# 推送合并后的main
git push origin main
```

### 第6步: 验证合并结果

```powershell
# 查看合并图(重要!)
git log --oneline --graph --all --decorate

# 应该看到多个merge commit,像这样:
# * abc1234 Merge: Merge LinJunyu branch
# |\
# | * def5678 LinJunyu的commit
# |/
# * ghi9012 Merge: Merge LUWEI branch
# |\
# | * jkl3456 LUWEI的commit
# |/
# * ... (其他merge)
```

---

## 完整代码块(复制粘贴)

如果你想一次性执行所有命令:

### PowerShell版本

```powershell
# 完整合并脚本 - 复制整个代码块到PowerShell执行

# 1. 准备
Write-Host "准备合并..." -ForegroundColor Green
git fetch origin
git checkout main
git pull origin main

# 2. 创建备份
Write-Host "创建备份..." -ForegroundColor Green
git checkout -b main_backup_2025_11_01
git checkout main

# 3. 定义要合并的分支
$branches = @(
    "origin/Lyh",
    "origin/LBY",
    "origin/Yangdh",
    "origin/LGC",
    "origin/LUWEI",
    "origin/LinJunyu"
)

# 4. 依次合并
foreach ($branch in $branches) {
    $branchName = $branch -replace "origin/", ""
    Write-Host "合并 $branchName..." -ForegroundColor Cyan
    
    git merge $branch --no-ff -m "Merge: Merge $branchName branch"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 合并 $branchName 时出错! 请手动解决冲突后运行: git merge --continue" -ForegroundColor Red
        break
    }
    Write-Host "✅ $branchName 合并成功" -ForegroundColor Green
}

# 5. 推送
Write-Host "推送到远程..." -ForegroundColor Green
git push origin main

# 6. 显示结果
Write-Host "查看合并图..." -ForegroundColor Green
git log --oneline --graph --all --decorate | head -30

Write-Host "✅ 完成!" -ForegroundColor Green
```

### Bash版本(macOS/Linux)

```bash
# 完整合并脚本 - 复制到bash执行

echo "准备合并..."
git fetch origin
git checkout main
git pull origin main

echo "创建备份..."
git checkout -b main_backup_2025_11_01
git checkout main

branches=(
    "origin/Lyh"
    "origin/LBY"
    "origin/Yangdh"
    "origin/LGC"
    "origin/LUWEI"
    "origin/LinJunyu"
)

for branch in "${branches[@]}"; do
    branchName=${branch#origin/}
    echo "合并 $branchName..."
    
    git merge $branch --no-ff -m "Merge: Merge $branchName branch"
    
    if [ $? -ne 0 ]; then
        echo "❌ 合并 $branchName 时出错! 请手动解决冲突"
        break
    fi
    echo "✅ $branchName 合并成功"
done

echo "推送到远程..."
git push origin main

echo "查看合并图..."
git log --oneline --graph --all --decorate | head -30

echo "✅ 完成!"
```

---

## 预期的最终结果

```
合并后的main分支结构:

main
├── ✅ Lyh的所有提交
├── ✅ LBY的所有提交
├── ✅ Yangdh的所有提交
├── ✅ LGC的所有提交
├── ✅ LUWEI的所有提交
└── ✅ LinJunyu的所有提交

远程分支:
├── main (已更新,包含所有代码)
├── Lyh (保留 ✅)
├── LBY (保留 ✅)
├── Yangdh (保留 ✅)
├── LGC (保留 ✅)
├── LUWEI (保留 ✅)
└── LinJunyu (保留 ✅)
```

---

## 遇到问题?

### 问题1: 合并时出现冲突

```powershell
# 1. 查看冲突
git status

# 2. 编辑冲突文件
# (使用编辑器打开,找到 <<<<<<< 和 >>>>>>>,手动选择)

# 3. 完成合并
git add .
git merge --continue
```

### 问题2: 合并后想撤销

```powershell
# 回到备份分支
git checkout main_backup_2025_11_01

# 或者使用reset回到之前
git reset --hard <commit-hash>
```

### 问题3: 分支没有出现在main中

```powershell
# 检查是否真的合并了
git log --all --graph --oneline | grep "分支名"

# 检查分支是否存在
git branch -a | grep 分支名
```

---

## 验证检查清单

合并完成后,检查:

- [ ] 所有分支都成功合并
- [ ] 没有冲突(或冲突已解决)
- [ ] main分支已推送到远程
- [ ] 所有分支仍然存在(未被删除)
- [ ] main包含所有分支的代码
- [ ] 合并图看起来正确

---

**关键点总结:**

✅ 使用 `--no-ff` 保留分支历史  
✅ 按顺序依次合并  
✅ 创建备份以防万一  
✅ 冲突时耐心解决  
✅ 最后推送到远程  
✅ 分支保留不删除

**需要帮助?** 见 `MERGE_GUIDE.md` 详细文档
