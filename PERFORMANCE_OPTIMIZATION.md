# 性能优化指南

## 🚀 后端性能优化

### 1. 数据库优化

#### 添加索引
```sql
-- 用户表索引
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

-- 待办事项索引
CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_status ON todos(status);
CREATE INDEX idx_todos_due_date ON todos(due_date);

-- 会议预订索引
CREATE INDEX idx_bookings_user_id ON meeting_bookings(user_id);
CREATE INDEX idx_bookings_room_id ON meeting_bookings(room_id);
CREATE INDEX idx_bookings_time ON meeting_bookings(start_time, end_time);

-- Session Token索引
CREATE INDEX idx_session_token ON session_tokens(token);
CREATE INDEX idx_session_expires ON session_tokens(expires_at);
```

#### 查询优化
- ✅ 使用异步查询（已实现）
- ✅ 分页查询避免大量数据加载
- ⚠️ 避免N+1查询问题
- ⚠️ 使用连接池配置

### 2. 缓存策略

#### Redis缓存层级
```python
# 建议的缓存策略
CACHE_TTL = {
    'weather_current': 1800,      # 30分钟
    'weather_forecast': 3600,     # 1小时
    'user_profile': 600,          # 10分钟
    'todo_list': 300,             # 5分钟
    'meeting_rooms': 600,         # 10分钟
}
```

#### 缓存失效策略
- 写操作后主动失效相关缓存
- 使用缓存版本号避免脏数据
- 设置合理的TTL

### 3. API优化

#### 响应压缩
```python
# 在middleware中添加Gzip压缩
from starlette.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

#### 限流优化
```python
# 不同API使用不同的限流策略
RATE_LIMITS = {
    '/api/weather': '100/minute',     # 天气查询高频
    '/api/auth/login': '5/minute',    # 登录低频
    '/api/todo/*': '200/minute',      # 待办中频
    '/api/meeting/*': '100/minute',   # 会议中频
}
```

### 4. 异步任务

#### Celery集成（可选）
```python
# 用于耗时操作
- RAG文档索引
- 邮件发送
- 数据统计
- 日志归档
```

---

## 🎨 前端性能优化

### 1. 代码分割

#### 路由懒加载（已实现）
```javascript
const routes = [
  {
    path: '/todo',
    component: () => import('../views/Todo.vue')
  },
  // ... 其他路由
]
```

### 2. 资源优化

#### 图片优化
- 使用WebP格式
- 实施懒加载
- CDN加速

#### 字体优化
```css
/* 预加载关键字体 */
<link rel="preload" href="/fonts/main.woff2" as="font" type="font/woff2" crossorigin>
```

### 3. 状态管理优化

#### 避免不必要的重渲染
```javascript
// 使用computed而非watch
// 使用v-memo缓存组件
// 合理使用key属性
```

### 4. 网络优化

#### HTTP/2支持
- Nginx已配置HTTP/2
- 启用服务器推送

#### 资源预取
```javascript
// 预取可能需要的路由
router.beforeEach((to, from, next) => {
  if (to.name === 'Todo') {
    import(/* webpackPrefetch: true */ '../views/Todo.vue')
  }
  next()
})
```

---

## 📊 监控和指标

### 1. 性能指标

#### 后端
- 请求响应时间（P95 < 200ms）
- QPS（目标：1000 req/s）
- 数据库连接池使用率
- 缓存命中率（目标：>80%）

#### 前端
- FCP (First Contentful Paint) < 1.5s
- LCP (Largest Contentful Paint) < 2.5s
- FID (First Input Delay) < 100ms
- CLS (Cumulative Layout Shift) < 0.1

### 2. 监控工具

#### 推荐方案
- **Prometheus + Grafana** - 系统监控
- **Sentry** - 错误追踪
- **New Relic** - APM性能监控
- **Google Lighthouse** - 前端性能审计

---

## 🔧 具体优化建议

### 立即执行（高优先级）
1. ✅ 添加数据库索引
2. ✅ 配置Redis缓存策略
3. ✅ 启用Gzip压缩
4. ✅ 优化SQL查询（避免SELECT *）

### 短期计划（中优先级）
5. 实施CDN加速静态资源
6. 添加API响应缓存头
7. 优化图片加载（懒加载+WebP）
8. 数据库连接池调优

### 长期规划（低优先级）
9. 微服务架构拆分
10. 读写分离
11. 消息队列引入
12. 边缘计算/CDN动态内容

---

## 📈 性能测试

### 压力测试脚本
```bash
# 使用wrk进行压力测试
wrk -t12 -c400 -d30s http://localhost:8080/api/todo

# 使用Apache Bench
ab -n 10000 -c 100 http://localhost:8080/api/weather?city=上海
```

### 基准测试
```python
# parttest/performance_test.py
import asyncio
import time
from aiohttp import ClientSession

async def benchmark_api(url, iterations=100):
    async with ClientSession() as session:
        start = time.time()
        for _ in range(iterations):
            async with session.get(url) as resp:
                await resp.text()
        elapsed = time.time() - start
        print(f"{iterations} requests in {elapsed:.2f}s")
        print(f"Average: {elapsed/iterations*1000:.2f}ms per request")
```

---

**最后更新**: 2026-05-14  
**版本**: v1.0
