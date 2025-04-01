## 1. Nginx 简介
Nginx 是一个高性能的 HTTP 和反向代理服务器，同时支持负载均衡、静态文件服务和缓存功能，广泛用于网站架构优化。

---

## 2. Nginx 安装与启动
### 2.1 安装 Nginx（以 Linux 为例）
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install nginx -y

# CentOS
sudo yum install epel-release -y
sudo yum install nginx -y
```

### 2.2 启动、停止和重启 Nginx
```bash
sudo systemctl start nginx   # 启动 Nginx
sudo systemctl stop nginx    # 停止 Nginx
sudo systemctl restart nginx # 重启 Nginx
sudo systemctl reload nginx  # 平滑重载配置文件
```

### 2.3 查看 Nginx 运行状态
```bash
sudo systemctl status nginx
```

---

## 3. Nginx 目录结构
| 目录 | 说明 |
|-------|------|
| `/etc/nginx/nginx.conf` | 主配置文件 |
| `/etc/nginx/sites-available/` | 可用的站点配置文件 |
| `/etc/nginx/sites-enabled/` | 已启用的站点配置文件（通常是符号链接） |
| `/var/log/nginx/access.log` | 访问日志 |
| `/var/log/nginx/error.log` | 错误日志 |

---

## 4. Nginx 配置文件结构
Nginx 的配置文件由多个指令组成，常见指令包括：
```nginx
worker_processes auto;  # 工作进程数

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;
    sendfile on;
    keepalive_timeout 65;

    server {
        listen 80;  # 监听 80 端口
        server_name example.com;
        
        location / {
            root /var/www/html;
            index index.html index.htm;
        }
    }
}
```

---

## 5. 常见功能配置
### 5.1 反向代理
```nginx
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### 5.2 负载均衡
```nginx
upstream backend_servers {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend_servers;
    }
}
```

### 5.3 静态文件服务
```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.html index.htm;
}
```

### 5.4 HTTPS 配置
```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/example.com.crt;
    ssl_certificate_key /etc/nginx/ssl/example.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

### 5.5 URL 重写
```nginx
server {
    listen 80;
    server_name example.com;

    location /oldpage {
        rewrite ^/oldpage$ /newpage permanent;
    }
}
```

### 5.6 限流
```nginx
http {
    limit_req_zone $binary_remote_addr zone=one:10m rate=1r/s;

    server {
        listen 80;
        location /api/ {
            limit_req zone=one burst=5;
        }
    }
}
```

---

## 6. 常用 Nginx 命令
| 命令 | 说明 |
|------|------|
| `nginx -t` | 测试 Nginx 配置是否正确 |
| `nginx -s reload` | 重新加载配置文件 |
| `nginx -s stop` | 停止 Nginx 进程 |
| `nginx -s quit` | 优雅地停止 Nginx |
| `systemctl restart nginx` | 重新启动 Nginx |

---

## 7. 日志查看
```bash
# 查看访问日志
sudo tail -f /var/log/nginx/access.log

# 查看错误日志
sudo tail -f /var/log/nginx/error.log
```

---

## 8. 其他高级配置
### 8.1 Gzip 压缩
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
gzip_min_length 1000;
gzip_comp_level 5;
```

### 8.2 CORS 处理（跨域）
```nginx
location /api/ {
    add_header 'Access-Control-Allow-Origin' '*';
    add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
}
```

### 8.3 设置缓存控制
```nginx
location /static/ {
    expires 30d;
    add_header Cache-Control "public, max-age=2592000";
}
```

---

## 9. 结语
Nginx 是一个功能强大的服务器，灵活性高，适用于反向代理、负载均衡、静态资源托管等场景。熟练掌握 Nginx 的基本配置和命令，可以有效优化网站架构，提高服务器性能。