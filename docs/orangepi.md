# 服务器 | 香橙派zero3 相关

## 服务器普通设置
WIFI 连接
```bash
nmcli dev wifi
sudo nmcli dev wifi connect <wifi_name> password <wifi_password>
```
查看IP
```bash
ip addr show wlan0
```
GPIO测试
```bash
gpio readall
gpio mode <wPi> <out | in | up| down>
gpio write <wPi> <0 | 1>
gpio read <wPi>
```

## 服务器启动需要开启的服务
- clash
- flask | 网页