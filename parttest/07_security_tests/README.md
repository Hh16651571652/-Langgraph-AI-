# 安全与中间件模块测试 (07_security_tests)

## 📋 测试范围

本模块测试系统的安全防护功能,包括:

- ✅ 敏感词过滤
- ✅ SQL注入检测
- ✅ API限流机制
- ✅ 中间件执行顺序

## 🧪 测试文件

| 文件 | 说明 |
|------|------|
| `test_security_utils.py` | 安全工具函数测试 |
| `test_rate_limit.py` | API限流测试 |
| `test_middleware.py` | 中间件集成测试 |

## 🚀 运行测试

```bash
pytest 07_security_tests/ -v
```

---

**维护者**: AI Digital Staff Team  
**最后更新**: 2026-05-14
