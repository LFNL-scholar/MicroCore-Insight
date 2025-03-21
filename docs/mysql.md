# mysql 分支

> 目前mysql以docker的方式运行在1Panel中

## 信息
- 安装位置：/opt/1Panel/apps/mysql/mysql
- 密码：LFNL1041
  
查看命令
```bash
docker ps
```
进入mysql
```bash
mysql -uroot -p # 本机
docker exec -it 容器名 mysql -uroot -p  # docker容器
mysql -uroot -p -h 192.168.1.100    # 远程连接
docker exec -it 1Panel-mysql-ZAa0 mysql -uroot -p
```
退出mysql
```bash
exit;
```

## mysql命令
数据库操作
```bash
SHOW DATABASES; # 查看所有数据库
CREATE DATABASE test_db;    # 创建数据库
USE test_db;    # 使用数据库
DROP DATABASE test_db;  # 删除数据库
```
数据表操作
```bash
SHOW TABLES;
```



