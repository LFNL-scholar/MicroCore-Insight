# Clash Linux Server 
## 科学上网

> 针对于香橙派zero3中orangepi用户的文档

clash-linux 安装于 /home/orangepi/.config/mihomo/

科学上网步骤
1. 启动clash-linux，将程序放入后台运行
```bash
nohup ./clash-linux &> clash.log &
ps aux | grep clash-linux   # 查找进程
sudo kill <PID>             # 结束进程
```
2. 设置代理
```bash
export http_proxy="http://127.0.0.1:7890"
export https_proxy="http://127.0.0.1:7890"
echo $http_proxy    # 查看代理
echo $https_proxy   # 查看代理
unset http_proxy    # 取消代理
unset https_proxy   # 取消代理
```
3. 测试
```bash
curl -I https://www.google.com
```
> 输出如下，表示成功
> HTTP/1.1 200 Connection established

参考教程
https://fanqiang.gitbook.io/fanqiang/linux