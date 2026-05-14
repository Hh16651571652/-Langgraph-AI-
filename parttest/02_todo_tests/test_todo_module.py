"""
Todo 模块测试 - CRUD & 状态管理
测试待办事项相关的核心功能
"""
import pytest
from datetime import datetime, timedelta
from crud.todo_crud import (
    create_todo,
    get_todos_by_user_id,
    get_todo_by_id_and_user,
    update_todo_status,
    update_todo_info,
    _calculate_time_status
)


class TestTodoCRUD:
    """Todo CRUD 操作测试"""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_todo(self, db_session, test_user, sample_todo_data):
        """测试创建待办事项"""
        todo = await create_todo(
            db_session,
            user_id=test_user.id,
            **sample_todo_data
        )
        
        assert todo is not None
        assert todo.title == sample_todo_data["title"]
        assert todo.user_id == test_user.id
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_todos_by_user(self, db_session, test_user, sample_todo_data):
        """测试获取用户的所有待办"""
        # 先创建几个待办
        created_count = 3
        for i in range(created_count):
            data = sample_todo_data.copy()
            data["title"] = f"测试待办{i+1}"
            await create_todo(db_session, user_id=test_user.id, **data)
        
        # 确保所有更改都已提交
        await db_session.commit()
        
        todos, total = await get_todos_by_user_id(db_session, test_user.id)
        
        # 至少应该有创建的数量（可能有其他测试创建的）
        assert total >= created_count
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_todo_by_id(self, db_session, test_user, sample_todo_data):
        """测试通过 ID 获取待办"""
        todo = await create_todo(db_session, user_id=test_user.id, **sample_todo_data)
        
        retrieved = await get_todo_by_id_and_user(db_session, todo.id, test_user.id)
        
        assert retrieved is not None
        assert retrieved.id == todo.id
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_todo(self, db_session, test_user, sample_todo_data):
        """测试更新待办事项"""
        todo = await create_todo(db_session, user_id=test_user.id, **sample_todo_data)
        
        # 先获取待办对象
        retrieved = await get_todo_by_id_and_user(db_session, todo.id, test_user.id)
        
        # 更新状态（需要传入 todo 对象）
        updated = await update_todo_status(
            db_session,
            todo=retrieved,
            status="completed"
        )
        
        assert updated is not None
        assert updated.status == "completed"
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_delete_todo(self, db_session, test_user, sample_todo_data):
        """测试删除待办事项"""
        from sqlalchemy import delete
        from model.todo_model import Todo
        
        todo = await create_todo(db_session, user_id=test_user.id, **sample_todo_data)
        
        # 直接删除（因为 todo_crud 中没有 delete_todo 函数）
        await db_session.execute(
            delete(Todo).where(Todo.id == todo.id)
        )
        await db_session.commit()
        
        # 验证已删除
        deleted = await get_todo_by_id_and_user(db_session, todo.id, test_user.id)
        assert deleted is None


class TestTodoStatus:
    """Todo 状态管理测试"""
    
    @pytest.mark.unit
    def test_calculate_time_status_completed(self):
        """测试已完成状态"""
        status = _calculate_time_status(None, "completed")
        assert status == "completed"
    
    @pytest.mark.unit
    def test_calculate_time_status_overdue(self):
        """测试逾期状态"""
        past_date = datetime.now() - timedelta(days=1)
        status = _calculate_time_status(past_date, "pending")
        assert status == "overdue"
    
    @pytest.mark.unit
    def test_calculate_time_status_upcoming(self):
        """测试即将到期状态(1小时内)"""
        near_future = datetime.now() + timedelta(minutes=30)
        status = _calculate_time_status(near_future, "pending")
        assert status == "upcoming"
    
    @pytest.mark.unit
    def test_calculate_time_status_ongoing(self):
        """测试正常进行状态"""
        far_future = datetime.now() + timedelta(days=7)
        status = _calculate_time_status(far_future, "pending")
        assert status == "ongoing"
    
    @pytest.mark.unit
    def test_calculate_time_status_with_string_date(self):
        """测试字符串日期兼容性(修复后的功能)"""
        future_date_str = (datetime.now() + timedelta(days=7)).isoformat()
        status = _calculate_time_status(future_date_str, "pending")
        assert status == "ongoing"
    
    @pytest.mark.unit
    def test_calculate_time_status_no_due_date(self):
        """测试无截止日期的情况"""
        status = _calculate_time_status(None, "pending")
        assert status == "ongoing"


class TestTodoAPI:
    """Todo API 接口测试(需要启动服务)"""
    
    @pytest.mark.integration
    @pytest.mark.skip(reason="需要运行中的服务器")
    async def test_api_create_todo(self, auth_headers):
        """测试 API 创建待办"""
        import httpx
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8080/api/todos",
                json={
                    "title": "API测试待办",
                    "description": "通过API创建",
                    "priority": "medium"
                },
                headers=auth_headers
            )
            
            assert response.status_code == 200
    
    @pytest.mark.integration
    @pytest.mark.skip(reason="需要运行中的服务器")
    async def test_api_get_todos(self, auth_headers):
        """测试 API 获取待办列表"""
        import httpx
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:8080/api/todos",
                headers=auth_headers
            )
            
            assert response.status_code == 200
            assert isinstance(response.json(), list)
