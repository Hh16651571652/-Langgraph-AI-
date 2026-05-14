"""
pytest 全局配置和 fixtures
提供通用的测试工具和数据库会话管理
"""
import pytest
import asyncio
from datetime import datetime, timedelta
from typing import AsyncGenerator

# 导入项目模块
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config.db_config import Base

# 配置 pytest-asyncio
pytest_plugins = ['pytest_asyncio']


# ==================== 数据库 Fixtures ====================

@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """创建测试数据库引擎"""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True
    )
    
    # 创建所有表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # 清理
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """为每个测试创建独立的数据库会话"""
    async_session_maker = async_sessionmaker(
        test_engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    
    async with async_session_maker() as session:
        yield session
        await session.rollback()


# ==================== 用户 Fixtures ====================

@pytest.fixture
def test_user_data():
    """测试用户数据 - 使用 UUID 确保唯一性"""
    import uuid
    unique_id = uuid.uuid4().hex[:8]
    return {
        "username": f"test_user_{unique_id}",
        "password_hash": "hashed_password_123",
        "role": "user",
        "is_active": True
    }


@pytest.fixture
async def test_user(db_session, test_user_data):
    """创建测试用户"""
    from crud.auth_crud import create_user
    
    user = await create_user(db_session, **test_user_data)
    return user


# ==================== Auth Fixtures ====================

@pytest.fixture
async def auth_headers(db_session, test_user):
    """生成认证请求头"""
    from crud.session_crud import create_session_token
    
    # 创建 session token
    session = await create_session_token(
        db_session,
        user_id=test_user.id,
        ip_address="127.0.0.1"
    )
    
    return {
        "Authorization": f"Bearer {session.token}",
        "Content-Type": "application/json"
    }


# ==================== Mock Fixtures ====================

@pytest.fixture
def mock_llm_response():
    """Mock LLM 响应"""
    return {
        "task_type": "chat",
        "confidence": 0.95,
        "response": "这是一个测试回复"
    }


@pytest.fixture
def mock_weather_data():
    """Mock 天气数据"""
    return {
        "city": "上海",
        "temperature": 25,
        "condition": "晴",
        "humidity": 60,
        "wind_speed": 12
    }


@pytest.fixture
def mock_meeting_rooms():
    """Mock 会议室数据"""
    return [
        {
            "id": 1,
            "room_name": "会议室A",
            "capacity": 10,
            "location": "3楼"
        },
        {
            "id": 2,
            "room_name": "会议室B",
            "capacity": 20,
            "location": "5楼"
        }
    ]


# ==================== 工具 Fixtures ====================

@pytest.fixture
def sample_todo_data():
    """示例待办数据 - 不包含 status，因为 create_todo 会自动设置"""
    return {
        "title": "测试待办事项",
        "description": "这是一个测试用的待办事项",
        "due_date": datetime.now() + timedelta(days=7),
        "priority": "high",
        "category": "work",
        "tags": "测试,重要"
    }


@pytest.fixture
def sample_meeting_booking():
    """示例会议预订数据"""
    now = datetime.now()
    return {
        "start_time": now + timedelta(hours=2),
        "end_time": now + timedelta(hours=3),
        "purpose": "项目讨论会议",
        "room_id": 1
    }


# ==================== Pytest 配置 ====================

def pytest_configure(config):
    """注册自定义标记"""
    config.addinivalue_line("markers", "unit: 单元测试标记")
    config.addinivalue_line("markers", "integration: 集成测试标记")
    config.addinivalue_line("markers", "slow: 慢速测试标记")


def pytest_collection_modifyitems(config, items):
    """自动添加标记"""
    for item in items:
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "slow" in item.nodeid:
            item.add_marker(pytest.mark.slow)
        else:
            item.add_marker(pytest.mark.unit)
