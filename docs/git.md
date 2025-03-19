# 一些相关的Git命令

## 普通
### 新建文件夹连接到远程仓库
```bash
git init
git remote add origin https://github.com/<Author>/<Project_name>.git
git branch -M main
```

### 基本 PR
```bash
git add .
git commit -m "</>"
git push
```

### 其他
查看当前的分支
```bash
git branch
```
创建新分支
```bash
git branch new_branch_name
```
切换到已有的分支
```bash
git switch branch_name
```
