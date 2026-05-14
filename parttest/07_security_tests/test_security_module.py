"""
安全模块测试 - 敏感词过滤、SQL注入防护、API限流
"""
import pytest
from utils.security import (
    sanitize_input,
    check_sensitive_words,
    detect_sql_injection,
    security_guard
)
from fastapi import HTTPException


class TestSecurityUtils:
    """安全工具函数测试"""
    
    @pytest.mark.unit
    def test_sanitize_input_removes_html(self):
        """测试移除HTML标签"""
        dirty_input = "<script>alert('xss')</script>Hello"
        clean = sanitize_input(dirty_input)
        
        assert "<script>" not in clean
        assert "Hello" in clean
    
    @pytest.mark.unit
    def test_sanitize_input_strips_whitespace(self):
        """测试去除空白字符"""
        dirty_input = "  Hello World  \n\t"
        clean = sanitize_input(dirty_input)
        
        assert clean == "Hello World"
    
    @pytest.mark.unit
    def test_check_sensitive_words_detects_bad_words(self):
        """测试敏感词检测"""
        bad_text = "这是一个反动言论"
        
        result = check_sensitive_words(bad_text)
        
        assert result is True
    
    @pytest.mark.unit
    def test_check_sensitive_words_clean_text(self):
        """测试正常文本通过"""
        clean_text = "今天天气真好"
        
        result = check_sensitive_words(clean_text)
        
        assert result is False
    
    @pytest.mark.unit
    def test_detect_sql_injection_select_statement(self):
        """测试检测SQL SELECT注入"""
        malicious = "SELECT * FROM users WHERE id=1"
        
        result = detect_sql_injection(malicious)
        
        assert result is True
    
    @pytest.mark.unit
    def test_detect_sql_injection_drop_table(self):
        """测试检测DROP TABLE注入"""
        malicious = "'; DROP TABLE users; --"
        
        result = detect_sql_injection(malicious)
        
        assert result is True
    
    @pytest.mark.unit
    def test_detect_sql_injection_safe_input(self):
        """测试安全输入通过"""
        safe = "Hello World 123"
        
        result = detect_sql_injection(safe)
        
        assert result is False
    
    @pytest.mark.unit
    def test_security_guard_blocks_sensitive_words(self):
        """测试安全网关拦截敏感词"""
        with pytest.raises(HTTPException) as exc_info:
            security_guard("包含反动内容")
        
        assert exc_info.value.status_code == 400
    
    @pytest.mark.unit
    def test_security_guard_blocks_sql_injection(self):
        """测试安全网关拦截SQL注入"""
        with pytest.raises(HTTPException) as exc_info:
            security_guard("SELECT * FROM users")
        
        assert exc_info.value.status_code == 400
    
    @pytest.mark.unit
    def test_security_guard_allows_safe_input(self):
        """测试安全网关允许安全输入"""
        # 不应抛出异常
        security_guard("这是一条安全的消息")


class TestRateLimit:
    """API限流测试(需要Redis)"""
    
    @pytest.mark.integration
    @pytest.mark.skip(reason="需要Redis运行中")
    async def test_rate_limit_middleware(self):
        """测试限流中间件"""
        from middleware.rate_limit import RateLimitMiddleware
        from starlette.testclient import TestClient
        from fastapi import FastAPI
        
        app = FastAPI()
        app.add_middleware(RateLimitMiddleware)
        
        @app.get("/test")
        def test_endpoint():
            return {"message": "ok"}
        
        client = TestClient(app)
        
        # 快速发送多个请求
        responses = []
        for i in range(150):  # 超过限制的请求数
            response = client.get("/test")
            responses.append(response.status_code)
        
        # 应该有一些请求被拒绝(429)
        assert 429 in responses
