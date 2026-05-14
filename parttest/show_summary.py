"""测试报告汇总"""
import json
from pathlib import Path

print("\n" + "="*80)
print("  📊 AI数字员工 - 测试报告汇总")
print("="*80)

modules = {
    '认证模块 (Auth)': 'auth_test_results.json',
    '待办模块 (Todo)': 'todo_test_results.json',
    '会议模块 (Meeting)': 'meeting_test_results.json',
    '安全模块 (Security)': 'security_test_results.json',
    'Agent模块': 'agent_test_results.json',
    '集成测试 (Integration)': 'integration_test_results.json',
}

total_passed = 0
total_failed = 0
total_skipped = 0
total_tests = 0

for module_name, json_file in modules.items():
    json_path = Path('reports') / json_file
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        s = data['summary']
        total_tests += s.get('total', 0)
        total_passed += s.get('passed', 0)
        total_failed += s.get('failed', 0)
        total_skipped += s.get('skipped', 0)
        
        status = "✅" if s.get('failed', 0) == 0 else "⚠️"
        print(f"\n{status} {module_name}:")
        print(f"   总计: {s.get('total', 0)}, 通过: {s.get('passed', 0)}, 失败: {s.get('failed', 0)}, 跳过: {s.get('skipped', 0)}")

pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

print("\n" + "="*80)
print(f"  📈 总体统计:")
print(f"     总测试数: {total_tests}")
print(f"     ✅ 通过: {total_passed}")
print(f"     ❌ 失败: {total_failed}")
print(f"     ⏭️  跳过: {total_skipped}")
print(f"     通过率: {pass_rate:.1f}%")
print("="*80 + "\n")
