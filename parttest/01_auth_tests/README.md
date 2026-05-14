# 认证模块测试 (01_auth_tests)

## 📋 测试范围

本模块测试 AI 数字员工系统的认证与授权功能,包括:

- ✅ Session Token 认证机制
- ✅ JWT 工具函数
- ✅ 用户 CRUD 操作
- ✅ 密码加密与验证
- ✅ 会话管理

## 🧪 测试文件说明

| 文件 | 说明 | 测试类型 |
|------|------|---------|
| `test_session_auth.py` | Session 认证流程测试 | 单元测试 |
| `test_jwt_utils.py` | JWT 工具函数测试 | 单元测试 |
| `test_auth_crud.py` | 用户 CRUD 操作测试 | 集成测试 |

## 🚀 运行测试

```bash
# 运行所有认证测试
pytest 01_auth_tests/ -v

# 运行特定测试文件
pytest 01_auth_tests/test_session_auth.py -v

# 带覆盖率报告
pytest 01_auth_tests/ --cov=../utils/session_auth --cov-report=term-missing
```

## 📊 测试用例示例

### Session 认证测试
- 创建有效的 Session Token
- 验证 Token 有效性
- Token 过期处理
- 无效 Token 拒绝访问

### 用户 CRUD 测试
- 创建新用户
- 查询用户信息
- 更新用户资料
- 删除用户账户
- 密码哈希验证

## ⚠️ 注意事项

1. 测试使用内存数据库,不会污染生产数据
2. 所有测试用例独立运行,互不影响
3. 密码测试使用固定测试密码 "Test123456"

---

**维护者**: AI Digital Staff Team  
**最后更新**: 2026-05-14
