"""
API 限流中间件
基于 Redis 实现滑动窗口或固定窗口限流
"""
import time
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

try:
    import redis
    # 使用 db=2 专门用于限流计数
    rate_limit_redis = redis.Redis(host='localhost', port=6379, db=2, decode_responses=True)
    rate_limit_redis.ping()
except Exception:
    rate_limit_redis = None

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    全局 API 限流中间件
    支持针对不同路由设置不同的限流阈值
    """
    
    # 默认限流配置: {路径前缀: (最大请求数, 时间窗口秒数)}
    RATE_LIMIT_CONFIG = {
        "/api/agent/chat": (30, 60),      # LLM对话接口：限制较严，防止资源滥用
        "/api/weather": (60, 60),         # 天气查询：中等频率
        "/api/todo": (100, 60),           # 待办事项：常规频率
        "/default": (100, 60)             # 其他接口：默认频率
    }

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if not rate_limit_redis:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        path = request.url.path
        
        # 排除静态资源和文档接口
        if path.startswith("/docs") or path.startswith("/openapi.json") or path.startswith("/uploads"):
            return await call_next(request)

        # 🔥 匹配限流规则
        limit_config = self.RATE_LIMIT_CONFIG.get("/default")
        for prefix, config in self.RATE_LIMIT_CONFIG.items():
            if path.startswith(prefix):
                limit_config = config
                break
        
        max_requests, window_seconds = limit_config
        key = f"rate_limit:{client_ip}:{path}"
        
        try:
            current_count = rate_limit_redis.get(key)
            
            if current_count is None:
                rate_limit_redis.setex(key, window_seconds, 1)
            elif int(current_count) >= max_requests:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"请求过于频繁，请在 {window_seconds} 秒后重试"
                )
            else:
                rate_limit_redis.incr(key)
                
        except HTTPException:
            raise
        except Exception as e:
            # Redis 故障时不阻断请求，仅记录日志
            print(f"[RateLimit] Redis error: {e}")

        response = await call_next(request)
        return response
