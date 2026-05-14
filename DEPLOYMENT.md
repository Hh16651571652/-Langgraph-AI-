# 🚀 部署和运维指南

## 📦 Docker部署

### 1. 本地开发环境

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f backend

# 停止服务
docker-compose down

# 重建容器
docker-compose up -d --build
```

### 2. 生产环境部署

#### 准备环境变量
```bash
cp .env.example .env.production
# 编辑 .env.production 填入真实配置
```

#### 使用Docker Compose
```bash
# 使用生产配置
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## 🔧 GitHub Actions CI/CD

### 1. 配置Secrets

在GitHub仓库设置中添加以下Secrets：

```
DOCKER_USERNAME      - Docker Hub用户名
DOCKER_PASSWORD      - Docker Hub密码或Access Token
SERVER_HOST          - 服务器IP地址
SERVER_USER          - SSH用户名
SERVER_SSH_KEY       - SSH私钥
```

### 2. 工作流程

```mermaid
graph LR
    A[代码推送] --> B{分支判断}
    B -->|main/develop| C[运行测试]
    B -->|PR| D[运行测试]
    C --> E[构建Docker镜像]
    D --> F[仅测试]
    E --> G[推送到Docker Hub]
    G --> H[部署到服务器]
```

### 3. 手动触发部署

```bash
# 推送标签触发部署
git tag v1.0.0
git push origin v1.0.0
```

---

## 📊 监控和日志

### 1. 查看服务状态

```bash
# Docker容器状态
docker ps

# 资源使用情况
docker stats

# 服务健康检查
curl http://localhost:8080/health
```

### 2. 日志管理

```bash
# 实时日志
docker-compose logs -f backend

# 最近100行日志
docker-compose logs --tail=100 backend

# 导出日志
docker-compose logs backend > backend.log
```

### 3. 数据库备份

```bash
# 备份MySQL
docker-compose exec db mysqldump -u root -p ai_digital_staff > backup.sql

# 恢复数据库
docker-compose exec -T db mysql -u root -p ai_digital_staff < backup.sql
```

---

## 🔒 安全配置

### 1. HTTPS配置

```nginx
# Nginx SSL配置示例
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    location / {
        proxy_pass http://backend:8080;
    }
}
```

### 2. 防火墙配置

```bash
# Ubuntu UFW
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# CentOS Firewalld
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --reload
```

### 3. 定期更新

```bash
# 更新Docker镜像
docker-compose pull
docker-compose up -d

# 清理旧镜像
docker image prune -a
```

---

## 🎯 性能优化

### 1. 数据库索引

```bash
# 运行索引优化脚本
python optimize_db_indexes.py
```

### 2. 缓存配置

确保Redis正常运行：
```bash
docker-compose exec redis redis-cli ping
# 应返回: PONG
```

### 3. 压力测试

```bash
# 安装wrk
brew install wrk  # macOS
sudo apt install wrk  # Ubuntu

# 运行测试
wrk -t12 -c400 -d30s http://localhost:8080/api/todo
```

或使用Python脚本：
```bash
pip install aiohttp
python benchmark_performance.py
```

---

## 🐛 故障排查

### 1. 常见问题

#### 后端无法启动
```bash
# 检查日志
docker-compose logs backend

# 检查数据库连接
docker-compose exec db mysql -u user -p

# 检查Redis连接
docker-compose exec redis redis-cli ping
```

#### 前端无法访问
```bash
# 检查Nginx配置
docker-compose exec frontend nginx -t

# 重启Nginx
docker-compose restart frontend
```

### 2. 性能问题

```bash
# 检查慢查询
docker-compose exec db mysql -u root -p -e "SHOW PROCESSLIST;"

# 检查内存使用
docker stats

# 检查磁盘空间
df -h
docker system df
```

---

## 📈 扩展建议

### 1. 水平扩展

```yaml
# docker-compose.scale.yml
services:
  backend:
    deploy:
      replicas: 3
  
  redis:
    deploy:
      replicas: 2
```

```bash
# 扩展服务
docker-compose up -d --scale backend=3
```

### 2. 负载均衡

使用Nginx作为负载均衡器：
```nginx
upstream backend {
    server backend1:8080;
    server backend2:8080;
    server backend3:8080;
}
```

### 3. 数据库读写分离

- 主库：写操作
- 从库：读操作
- 使用ProxySQL或MaxScale

---

## 🔄 版本升级

### 升级流程

```bash
# 1. 备份数据
docker-compose exec db mysqldump -u root -p ai_digital_staff > backup_$(date +%Y%m%d).sql

# 2. 拉取新代码
git pull origin main

# 3. 停止服务
docker-compose down

# 4. 重新构建
docker-compose build --no-cache

# 5. 启动服务
docker-compose up -d

# 6. 运行数据库迁移
docker-compose exec backend python migrate.py

# 7. 验证服务
curl http://localhost:8080/health
```

---

## 📞 技术支持

### 联系方式
- GitHub Issues: [项目地址]/issues
- 文档: [项目Wiki]
- 邮箱: support@example.com

### 社区资源
- FastAPI官方文档: https://fastapi.tiangolo.com
- Vue.js官方文档: https://vuejs.org
- Docker官方文档: https://docs.docker.com

---

**最后更新**: 2026-05-14  
**版本**: v1.0
