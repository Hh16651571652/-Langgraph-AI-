"""
认证模块测试 - Session Auth & CRUD
测试认证相关的核心功能
"""
import pytest
from datetime import datetime, timedelta
from crud.session_crud import create_session_token, get_session_by_token, invalidate_session_token
from crud.auth_crud import create_user, get_user_by_id, get_user_by_username, update_user_info


class TestSessionAuth:
    """Session 认证测试类"""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_valid_token(self, db_session, test_user):
        """测试创建有效的 Session Token"""
        session = await create_session_token(
            db_session,
            user_id=test_user.id,
            ip_address="127.0.0.1",
            expires_days=7
        )
        
        assert session is not None
        assert isinstance(session.token, str)
        assert len(session.token) > 0
        assert session.user_id == test_user.id
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_verify_valid_token(self, db_session, test_user):
        """测试验证有效的 Token"""
        session = await create_session_token(
            db_session,
            user_id=test_user.id,
            ip_address="127.0.0.1"
        )
        
        retrieved = await get_session_by_token(db_session, session.token)
        
        assert retrieved is not None
        assert retrieved.user_id == test_user.id
        assert retrieved.is_active is True
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_verify_invalid_token(self, db_session):
        """测试验证无效的 Token"""
        invalid_token = "invalid.token.here"
        
        retrieved = await get_session_by_token(db_session, invalid_token)
        
        assert retrieved is None
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_invalidate_token(self, db_session, test_user):
        """测试使 Token 失效"""
        session = await create_session_token(
            db_session,
            user_id=test_user.id,
            ip_address="127.0.0.1"
        )
        
        # 使 token 失效
        success = await invalidate_session_token(db_session, session.token)
        
        assert success is True
        
        # 验证已失效
        retrieved = await get_session_by_token(db_session, session.token)
        assert retrieved is None


class TestAuthCRUD:
    """用户 CRUD 操作测试"""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_user(self, db_session, test_user_data):
        """测试创建用户"""
        # 从 test_user_data 中移除不需要的字段，只保留 create_user 函数需要的
        user_data = test_user_data.copy()
        user = await create_user(
            db_session,
            username=user_data["username"],
            password_hash=user_data["password_hash"],
            role=user_data.get("role", "user"),
            is_active=user_data.get("is_active", True)
        )
        
        assert user is not None
        assert user.username == user_data["username"]
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_user_by_id(self, db_session, test_user):
        """测试通过 ID 获取用户"""
        user = await get_user_by_id(db_session, test_user.id)
        
        assert user is not None
        assert user.id == test_user.id
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_user_by_username(self, db_session, test_user):
        """测试通过用户名获取用户"""
        user = await get_user_by_username(db_session, test_user.username)
        
        assert user is not None
        assert user.username == test_user.username
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_user(self, db_session, test_user):
        """测试更新用户信息"""
        updated_user = await update_user_info(
            db_session,
            user_id=test_user.id,
            email="updated@example.com",
            description="新的描述"
        )
        
        assert updated_user is not None
        assert updated_user.email == "updated@example.com"
