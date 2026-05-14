# 项目测试套件说明

## 📋 目录结构

```
parttest/
├── README.md                          # 本文件 - 测试总览
├── conftest.py                        # pytest 全局配置和 fixtures
├── run_all_tests.py                   # 主测试运行脚本
├── generate_report.py                 # 测试报告生成器
├── requirements-test.txt              # 测试依赖包
│
├── 01_auth_tests/                     # 认证模块测试
│   ├── README.md                      # 模块测试说明
│   ├── test_session_auth.py           # Session 认证测试
│   ├── test_jwt_utils.py              # JWT 工具测试
│   └── test_auth_crud.py              # 认证 CRUD 测试
│
├── 02_todo_tests/                     # 待办事项模块测试
│   ├── README.md
│   ├── test_todo_crud.py              # Todo CRUD 操作测试
│   ├── test_todo_api.py               # Todo API 接口测试
│   └── test_todo_status.py            # Todo 状态管理测试
│
├── 03_meeting_tests/                  # 会议室模块测试
│   ├── README.md
│   ├── test_meeting_crud.py           # 会议室 CRUD 测试
│   ├── test_meeting_booking.py        # 预订逻辑测试
│   ├── test_meeting_nlp.py            # NLP 解析测试
│   └── test_meeting_api.py            # Meeting API 测试
│
├── 04_weather_tests/                  # 天气模块测试
│   ├── README.md
│   ├── test_weather_api.py            # 天气 API 测试
│   ├── test_weather_cache.py          # 天气缓存测试
│   └── test_mcp_tools.py              # MCP 天气工具测试
│
├── 05_agent_tests/                    # Agent 智能体测试
│   ├── README.md
│   ├── test_task_classifier.py        # 任务分类器测试
│   ├── test_langgraph_workflow.py     # LangGraph 工作流测试
│   ├── test_chat_agent.py             # 聊天 Agent 测试
│   ├── test_todo_agent.py             # Todo Agent 测试
│   ├── test_meeting_agent.py          # Meeting Agent 测试
│   └── test_weather_agent.py          # Weather Agent 测试
│
├── 06_rag_tests/                      # RAG 检索增强生成测试
│   ├── README.md
│   ├── test_vector_db.py              # 向量数据库测试
│   ├── test_hybrid_retriever.py       # 混合检索器测试
│   ├── test_reranker.py               # 重排序器测试
│   ├── test_query_expansion.py        # 查询扩展测试
│   └── test_rag_retriever.py          # RAG 检索器集成测试
│
├── 07_security_tests/                 # 安全与中间件测试
│   ├── README.md
│   ├── test_security_utils.py         # 安全工具测试（敏感词、SQL注入）
│   ├── test_rate_limit.py             # API 限流测试
│   └── test_middleware.py             # 中间件测试
│
├── 08_frontend_tests/                 # 前端测试（可选，需安装 @vue/test-utils）
│   ├── README.md
│   ├── test_api_client.js             # API 客户端测试
│   └── test_components.spec.js        # Vue 组件测试
│
└── 09_integration_tests/              # 集成测试
    ├── README.md
    ├── test_full_workflow.py          # 完整业务流程测试
    ├── test_cross_module.py           # 跨模块交互测试
    └── test_performance.py            # 性能基准测试
```

## 🚀 快速开始

### 1. 安装测试依赖

```bash
cd parttest
pip install -r requirements-test.txt
```

### 2. 运行所有测试

```bash
# 运行全部测试并生成报告
python run_all_tests.py

# 或者使用 pytest 直接运行
pytest -v --cov=../ --cov-report=html:reports/coverage_html
```

### 3. 运行特定模块测试

```bash
# 只运行 Auth 模块测试
pytest 01_auth_tests/ -v

# 只运行 Agent 模块测试
pytest 05_agent_tests/ -v

# 运行带覆盖率报告的测试
pytest 02_todo_tests/ --cov=../crud/todo_crud --cov-report=term-missing
```

### 4. 查看测试报告

测试完成后，报告将生成在 `reports/` 目录下：
- `test_report_*.html` - HTML 格式详细报告
- `coverage_html/` - 代码覆盖率报告
- `test_results_*.xml` - JUnit XML 格式结果

## 📊 测试覆盖目标

| 模块 | 单元测试 | 集成测试 | 覆盖率目标 |
|------|---------|---------|-----------|
| Auth | ✅ | ✅ | 85%+ |
| Todo | ✅ | ✅ | 90%+ |
| Meeting | ✅ | ✅ | 85%+ |
| Weather | ✅ | ✅ | 80%+ |
| Agent | ✅ | ✅ | 80%+ |
| RAG | ✅ | ✅ | 75%+ |
| Security | ✅ | ✅ | 90%+ |

## 🔧 测试配置说明

### pytest 配置 (pyproject.toml)

```toml
[tool.pytest.ini_options]
testpaths = ["."]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]
```

### 全局 Fixtures (conftest.py)

- `db_session` - 数据库会话 fixture
- `test_user` - 测试用户 fixture
- `auth_headers` - 认证请求头 fixture
- `mock_llm` - Mock LLM 响应 fixture

## 📝 测试规范

### 命名规范
- 测试文件：`test_<模块名>.py`
- 测试类：`Test<功能名>`
- 测试函数：`test_<具体场景>`

### 测试用例结构
```python
def test_<场景描述>(self, fixture1, fixture2):
    # Arrange - 准备测试数据
    ...
    
    # Act - 执行被测操作
    result = function_under_test()
    
    # Assert - 验证结果
    assert result == expected_value
```

### 标记使用
- `@pytest.mark.unit` - 单元测试
- `@pytest.mark.integration` - 集成测试
- `@pytest.mark.slow` - 耗时较长的测试

## 🐛 常见问题

### Q: 测试失败提示数据库连接错误？
A: 确保已启动测试数据库或在 conftest.py 中配置了正确的数据库 URL。

### Q: 如何跳过某些测试？
A: 使用 `@pytest.mark.skip(reason="原因")` 装饰器。

### Q: 如何调试单个测试？
A: 使用 `pytest test_file.py::test_function -v -s` 命令。

## 📞 联系与支持

如有测试相关问题，请查阅各模块下的 README.md 文件或联系开发团队。

---

**最后更新**: 2026-05-14  
**维护者**: AI Digital Staff Team
