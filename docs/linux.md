# 一些工作中常用到的Linux环境下的命令

## 普通
### 1. 对于Python程序，想要在后台保持运行
```bash
nohup python app.py > output.log 2>&1 &
```
使用 tail 命令实时查看文件的最后几行
```bash
tail -f output.log
```
查看所有运行中的进程并查找特定的进程：
```bash
ps aux | grep <process_name>
ps aux | grep app.py
```
关闭这个服务，杀死进程
```bash
kill <PID>
```

### 2. MiniConda的使用
查看conda版本
```bash
conda --version
```
创建一个新的conda环境
```bash
conda create -n myenv python=3.12 -y
```
删除一个环境
```bash
conda remove -n xiaozhi-esp32-server --all -y
```
启用一个环境
```bash
conda activate mynev
```
退出conda环境
```bash
conda deactivate
```
列出所有已创建的环境
```bash
conda env list
```
添加清华源通道
```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
```
批量下载软件包
```bash
pip install -r requirements.txt
```
