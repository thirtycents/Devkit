# ⚡ 最简化合并指令(复制即用)

## 5行命令搞定

```powershell
git checkout main && git pull origin main && git merge origin/Lyh --no-ff -m "Merge Lyh" && git merge origin/LBY --no-ff -m "Merge LBY" && git merge origin/Yangdh --no-ff -m "Merge Yangdh" && git merge origin/LGC --no-ff -m "Merge LGC" && git merge origin/LUWEI --no-ff -m "Merge LUWEI" && git merge origin/LinJunyu --no-ff -m "Merge LinJunyu" && git push origin main
```

## 分行版本(逐个执行)

```powershell
# 1. 准备
git checkout main
git pull origin main

# 2. 合并
git merge origin/Lyh --no-ff -m "Merge Lyh"
git merge origin/LBY --no-ff -m "Merge LBY"
git merge origin/Yangdh --no-ff -m "Merge Yangdh"
git merge origin/LGC --no-ff -m "Merge LGC"
git merge origin/LUWEI --no-ff -m "Merge LUWEI"
git merge origin/LinJunyu --no-ff -m "Merge LinJunyu"

# 3. 推送
git push origin main
```

## 验证

```powershell
git log --oneline --graph --all | head -30
```

---

## 如果有冲突

```powershell
# 查看冲突
git status

# 编辑冲突文件后
git add .
git merge --continue
```

---

**就这么简单!** 分支会合并到main,但原分支保留不删除。
