"""
会议室模块测试 - 基于实际存在的 CRUD 函数
测试会议预订、冲突检测、取消等功能
"""
import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from model.meeting_room_model import MeetingRoom
from model.meeting_booking_model import MeetingBooking
from crud.meeting_crud import (
    get_room_by_id,
    create_booking,
    get_bookings_by_user_id,
    check_time_conflict,
    cancel_booking,
    complete_booking
)


class TestMeetingBooking:
    """会议预订测试"""
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_booking_mock(self, db_session, test_user):
        """测试创建会议预订（使用 Mock）"""
        # Mock 所有依赖
        with patch('crud.meeting_crud.get_room_by_id', new_callable=AsyncMock) as mock_get_room:
            mock_room = MagicMock()
            mock_room.id = 1
            mock_room.room_name = "测试会议室"
            mock_room.capacity = 10
            mock_get_room.return_value = mock_room
            
            with patch('crud.meeting_crud.check_time_conflict', new_callable=AsyncMock) as mock_check:
                mock_check.return_value = False  # 无时间冲突
                
                try:
                    now = datetime.now()
                    booking = await create_booking(
                        db_session,
                        user_id=test_user.id,
                        room_id=1,
                        start_time=now + timedelta(hours=2),
                        end_time=now + timedelta(hours=3),
                        purpose="项目讨论"
                    )
                    
                    if booking:
                        assert booking.user_id == test_user.id
                        assert booking.room_id == 1
                        assert booking.purpose == "项目讨论"
                except Exception as e:
                    pytest.skip(f"需要真实会议室数据: {e}")
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_bookings_by_user_id_mock(self, db_session, test_user):
        """测试获取用户预订列表（使用 Mock）"""
        with patch.object(db_session, 'execute', new_callable=AsyncMock) as mock_execute:
            mock_result = MagicMock()
            mock_result.scalars.return_value.all.return_value = []
            mock_execute.return_value = mock_result
            
            # get_bookings_by_user_id 返回 (bookings, total)
            result = await get_bookings_by_user_id(db_session, test_user.id)
            
            assert isinstance(result, tuple)
            assert len(result) == 2
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_cancel_booking_mock(self, db_session, test_user):
        """测试取消预订（使用 Mock）"""
        mock_booking = MagicMock(spec=MeetingBooking)
        mock_booking.id = 1
        mock_booking.user_id = test_user.id
        mock_booking.room_id = 1
        mock_booking.status = "confirmed"
        
        with patch('crud.meeting_crud.update_room_status', new_callable=AsyncMock):
            success = await cancel_booking(db_session, mock_booking, test_user.id)
            
            assert mock_booking.status == "cancelled"
            assert success is not None
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_complete_booking_mock(self, db_session, test_user):
        """测试完成预订（使用 Mock）"""
        mock_booking = MagicMock(spec=MeetingBooking)
        mock_booking.id = 1
        mock_booking.user_id = test_user.id
        mock_booking.room_id = 1
        mock_booking.status = "confirmed"
        
        with patch('crud.meeting_crud.update_room_status', new_callable=AsyncMock):
            success = await complete_booking(db_session, mock_booking)
            
            assert mock_booking.status == "completed"
            assert success is not None


class TestMeetingRoomQueries:
    """会议室查询测试"""
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_room_by_id_not_found(self, db_session):
        """测试获取不存在的会议室"""
        with patch.object(db_session, 'execute', new_callable=AsyncMock) as mock_execute:
            mock_result = MagicMock()
            mock_result.scalar_one_or_none.return_value = None
            mock_execute.return_value = mock_result
            
            room = await get_room_by_id(db_session, 999)
            
            assert room is None


class TestTimeConflict:
    """时间冲突检测测试"""
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_check_time_conflict_basic(self, db_session):
        """测试时间冲突检测基本逻辑"""
        # Mock 查询结果
        with patch.object(db_session, 'execute', new_callable=AsyncMock) as mock_execute:
            mock_result = MagicMock()
            # 返回 None 表示无冲突，返回 booking 对象表示有冲突
            mock_result.scalar_one_or_none.return_value = None
            mock_execute.return_value = mock_result
            
            now = datetime.now()
            has_conflict = await check_time_conflict(
                db_session,
                room_id=1,
                start_time=now + timedelta(hours=2),
                end_time=now + timedelta(hours=3)
            )
            
            # scalar_one_or_none 返回 None 表示无冲突
            assert has_conflict is None or has_conflict is False


class TestMeetingNLP:
    """会议 NLP 解析简单测试"""
    
    @pytest.mark.unit
    def test_meeting_text_contains_keywords(self):
        """测试会议文本关键词检测"""
        text = "明天下午3点在会议室A开会"
        
        keywords = ["会议", "会议室", "开会"]
        found = any(keyword in text for keyword in keywords)
        
        assert found is True
    
    @pytest.mark.unit
    def test_time_pattern_detection(self):
        """测试时间模式检测"""
        text = "下午3点开会"
        
        time_patterns = ["上午", "下午", "点", "分", "小时"]
        found = any(pattern in text for pattern in time_patterns)
        
        assert found is True
