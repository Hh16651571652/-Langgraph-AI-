# 🐳 Docker 部署配置

本目录包含AI数字员工项目的Docker配置文件。

## 📁 文件说明

- `Dockerfile.backend` - 后端FastAPI服务镜像
- `Dockerfile.frontend` - 前端Vue3+Nginx服务镜像
- `docker-compose.yml` - 多服务编排配置（后端+前端+MySQL+Redis）
- `.dockerignore` - Docker构建忽略规则

## 🚀 快速开始

### 1. 从项目根目录启动

```bash
# 返回项目根目录
cd ..

# 一键启动所有服务
docker-compose -f docker/docker-compose.yml up -d

# 查看日志
docker-compose -f docker/docker-compose.yml logs -f backend

# 停止服务
docker-compose -f docker/docker-compose.yml down
```

### 2. 单独构建镜像

```bash
# 构建后端镜像
docker build -f docker/Dockerfile.backend -t ai-digital-staff-backend .

# 构建前端镜像
docker build -f docker/Dockerfile.frontend -t ai-digital-staff-frontend ./forward/-AI-Digital-Worker-development-project
```

## 📊 服务端口

| 服务 | 容器端口 | 主机端口 | 说明 |
|------|---------|---------|------|
| Backend | 8080 | 8080 | FastAPI API服务 |
| Frontend | 80 | 80 | Vue3 + Nginx |
| MySQL | 3306 | 3306 | 数据库 |
| Redis | 6379 | 6379 | 缓存 |

## 🔧 环境变量

在启动前，确保设置以下环境变量：

```bash
# 方式1: 创建 .env 文件
echo "DASHSCOPE_API_KEY=your-api-key" > .env

# 方式2: 直接导出
export DASHSCOPE_API_KEY=your-api-key
```

## 💾 数据持久化

Docker Compose配置了以下数据卷：

- `mysql-data` - MySQL数据库文件
- `redis-data` - Redis缓存数据

数据会持久化保存，即使容器重启也不会丢失。

## 🛠️ 常用命令

```bash
# 查看所有运行中的容器
docker ps

# 查看资源使用情况
docker stats

# 进入容器内部
docker-compose -f docker/docker-compose.yml exec backend bash

# 重启单个服务
docker-compose -f docker/docker-compose.yml restart backend

# 清理未使用的镜像和容器
docker system prune -a
```

## 🐛 故障排查

### 后端无法启动
```bash
# 查看后端日志
docker-compose -f docker/docker-compose.yml logs backend

# 检查数据库连接
docker-compose -f docker/docker-compose.yml exec db mysql -u user -p
```

### 前端无法访问
```bash
# 检查Nginx配置
docker-compose -f docker/docker-compose.yml exec frontend nginx -t

# 重启前端服务
docker-compose -f docker/docker-compose.yml restart frontend
```

## 📝 开发模式

如果需要热重载开发，建议使用本地运行而非Docker：

```bash
# 后端
python ai-project-main.py

# 前端
cd forward/-AI-Digital-Worker-development-project
npm run dev
```

---

**最后更新**: 2026-05-14  
**版本**: v1.0
