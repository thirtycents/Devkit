# ⚡ 快速合并命令

## 一键合并所有分支到main(保留分支)

```powershell
# 1. 准备
git checkout main
git pull origin main

# 2. 合并所有分支
git merge origin/Lyh --no-ff -m "Merge: Lyh branch"
git merge origin/LBY --no-ff -m "Merge: LBY branch"
git merge origin/Yangdh --no-ff -m "Merge: Yangdh branch"
git merge origin/LGC --no-ff -m "Merge: LGC branch"
git merge origin/LUWEI --no-ff -m "Merge: LUWEI branch"
git merge origin/LinJunyu --no-ff -m "Merge: LinJunyu branch"

# 3. 推送
git push origin main

# 4. 验证
git log --oneline --graph --all | head -20
```

## 关键命令

| 命令 | 作用 |
|------|------|
| `git checkout main` | 切换到main分支 |
| `git pull origin main` | 拉取最新main |
| `git merge origin/分支名 --no-ff -m "message"` | 合并分支(保留历史) |
| `git push origin main` | 推送main |
| `git log --oneline --graph --all` | 查看合并图 |

## 如果有冲突

```powershell
# 1. 查看冲突
git status

# 2. 编辑冲突文件(找到 <<<<<<< 和 >>>>>>>)

# 3. 标记已解决
git add .

# 4. 完成合并
git merge --continue

# 或中止
git merge --abort
```

## 详细指南

见 `MERGE_GUIDE.md`
