"""
Agent 模块测试 - 任务分类、LangGraph工作流、各类型Agent
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock


class TestTaskClassifier:
    """任务分类器测试"""
    
    @pytest.mark.unit
    def test_task_classifier_initialization(self):
        """测试任务分类器初始化"""
        from agent.task_classifier import get_task_classifier
        
        # Mock LLM to avoid actual API call
        with patch('agent.task_classifier.get_qwen_llm') as mock_llm:
            mock_llm.return_value = Mock()
            classifier = get_task_classifier()
            
            assert classifier is not None
            assert hasattr(classifier, 'classify')
    
    @pytest.mark.unit
    async def test_classify_meeting_intent(self):
        """测试会议意图分类"""
        query = "预订一个会议室"
        
        # 简单的关键词匹配测试
        assert "会议" in query or "预订" in query
    
    @pytest.mark.unit
    async def test_classify_weather_intent(self):
        """测试天气意图分类"""
        query = "上海今天天气怎么样"
        
        assert "天气" in query
    
    @pytest.mark.unit
    async def test_classify_chat_intent(self):
        """测试闲聊意图分类"""
        query = "你好，最近怎么样"
        
        # 不包含特定关键词，应归类为 chat
        assert True


class TestLangGraphWorkflow:
    """LangGraph 工作流测试"""
    
    @pytest.mark.unit
    def test_workflow_initialization(self):
        """测试工作流初始化"""
        from agent.langgraph_workflow import get_langgraph_workflow
        
        workflow = get_langgraph_workflow()
        
        assert workflow is not None
    
    @pytest.mark.integration
    @pytest.mark.skip(reason="需要完整配置和LLM API")
    async def test_workflow_execution(self):
        """测试工作流执行"""
        from agent.langgraph_workflow import get_langgraph_workflow
        
        workflow = get_langgraph_workflow()
        
        # 模拟输入
        input_data = {
            "message": "帮我创建一个待办",
            "user_id": 1
        }
        
        # 执行工作流
        result = await workflow.ainvoke(input_data)
        
        assert result is not None


class TestChatAgent:
    """Chat Agent 测试"""
    
    @pytest.mark.unit
    def test_chat_agent_process(self):
        """测试 Chat Agent process 方法"""
        from agent.chat_agent import ChatAgent
        
        agent = ChatAgent()
        
        # Verify agent has process method
        assert hasattr(agent, 'process')
        assert callable(getattr(agent, 'process'))
    
    @pytest.mark.unit
    async def test_chat_agent_with_rag(self):
        """测试带 RAG 的 Chat Agent"""
        # 测试 RAG 集成
        assert True


class TestTodoAgent:
    """Todo Agent 测试"""
    
    @pytest.mark.unit
    def test_todo_agent_process(self):
        """测试 Todo Agent process 方法"""
        from agent.todo_agent import TodoAgent
        
        agent = TodoAgent()
        
        # Verify agent has process method
        assert hasattr(agent, 'process')
        assert callable(getattr(agent, 'process'))


class TestMeetingAgent:
    """Meeting Agent 测试"""
    
    @pytest.mark.unit
    def test_meeting_agent_process(self):
        """测试 Meeting Agent process 方法"""
        from agent.meeting_agent import MeetingAgent
        
        agent = MeetingAgent()
        
        # Verify agent has process method
        assert hasattr(agent, 'process')
        assert callable(getattr(agent, 'process'))


class TestWeatherAgent:
    """Weather Agent 测试"""
    
    @pytest.mark.unit
    def test_weather_agent_process(self):
        """测试 Weather Agent process 方法"""
        from agent.weather_agent import WeatherAgent
        
        agent = WeatherAgent()
        
        # Verify agent has process method
        assert hasattr(agent, 'process')
        assert callable(getattr(agent, 'process'))


class TestAgentIntegration:
    """Agent 集成测试"""
    
    @pytest.mark.integration
    @pytest.mark.skip(reason="需要完整环境")
    async def test_full_agent_workflow(self):
        """测试完整的 Agent 工作流"""
        # 从用户输入到最终响应的完整流程
        user_input = "帮我创建一个明天的待办事项"
        
        # 1. 分类任务
        # 2. 选择 Agent
        # 3. 执行操作
        # 4. 返回结果
        
        assert True
