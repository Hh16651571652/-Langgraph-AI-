"""为每个模块生成独立的HTML测试报告"""
import json
from datetime import datetime
from pathlib import Path


def generate_module_report(module_name, json_file):
    """为单个模块生成HTML报告"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        summary = data['summary']
        tests = data.get('tests', [])
        
        # 统计测试结果
        passed = summary.get('passed', 0)
        failed = summary.get('failed', 0)
        skipped = summary.get('skipped', 0)
        total = summary.get('total', 0)
        
        # 确定状态
        if failed == 0:
            status_icon = "✅"
            status_text = "全部通过"
            status_color = "#52c41a"
        elif passed > 0:
            status_icon = "⚠️"
            status_text = "部分失败"
            status_color = "#faad14"
        else:
            status_icon = "❌"
            status_text = "全部失败"
            status_color = "#ff4d4f"
        
        # 计算通过率
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        # 生成HTML
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{module_name} - 测试报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .status-badge {{
            display: inline-block;
            margin-top: 15px;
            padding: 10px 30px;
            background: {status_color};
            border-radius: 25px;
            font-size: 1.2em;
            font-weight: bold;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        .stat-card h3 {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 15px;
            text-transform: uppercase;
        }}
        .stat-card .value {{
            font-size: 3em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-card.passed .value {{ color: #52c41a; }}
        .stat-card.failed .value {{ color: #ff4d4f; }}
        .stat-card.skipped .value {{ color: #faad14; }}
        .progress-bar {{
            padding: 0 40px 40px;
        }}
        .progress-container {{
            background: #e0e0e0;
            border-radius: 10px;
            height: 30px;
            overflow: hidden;
            position: relative;
        }}
        .progress-fill {{
            background: linear-gradient(90deg, #52c41a 0%, #73d13d 100%);
            height: 100%;
            width: {pass_rate}%;
            transition: width 1s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}
        .test-list {{
            padding: 0 40px 40px;
        }}
        .test-list h2 {{
            margin-bottom: 20px;
            color: #333;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        th {{
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
        }}
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        tr:hover {{
            background: #f5f7fa;
        }}
        .badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: bold;
        }}
        .badge-passed {{ background: #d4edda; color: #155724; }}
        .badge-failed {{ background: #f8d7da; color: #721c24; }}
        .badge-skipped {{ background: #fff3cd; color: #856404; }}
        .footer {{
            text-align: center;
            padding: 30px;
            background: #f8f9fa;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 {module_name}</h1>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <div class="status-badge">{status_icon} {status_text}</div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>总测试数</h3>
                <div class="value">{total}</div>
            </div>
            <div class="stat-card passed">
                <h3>通过</h3>
                <div class="value">{passed}</div>
            </div>
            <div class="stat-card failed">
                <h3>失败</h3>
                <div class="value">{failed}</div>
            </div>
            <div class="stat-card skipped">
                <h3>跳过</h3>
                <div class="value">{skipped}</div>
            </div>
        </div>
        
        <div class="progress-bar">
            <h3 style="margin-bottom: 10px; color: #333;">通过率: {pass_rate:.1f}%</h3>
            <div class="progress-container">
                <div class="progress-fill">{pass_rate:.1f}%</div>
            </div>
        </div>
        
        <div class="test-list">
            <h2>📋 测试详情</h2>
            <table>
                <thead>
                    <tr>
                        <th>测试名称</th>
                        <th>状态</th>
                        <th>耗时(秒)</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        # 添加测试列表
        for test in tests:
            nodeid = test.get('nodeid', '')
            test_name = nodeid.split('::')[-1] if '::' in nodeid else nodeid
            outcome = test.get('outcome', 'unknown')
            
            # 计算总耗时
            duration = 0
            for phase in ['setup', 'call', 'teardown']:
                if phase in test:
                    duration += test[phase].get('duration', 0)
            
            if outcome == 'passed':
                badge_class = 'badge-passed'
                badge_text = '✅ 通过'
            elif outcome == 'failed':
                badge_class = 'badge-failed'
                badge_text = '❌ 失败'
            else:
                badge_class = 'badge-skipped'
                badge_text = '⏭️ 跳过'
            
            html += f"""
                    <tr>
                        <td><strong>{test_name}</strong></td>
                        <td><span class="badge {badge_class}">{badge_text}</span></td>
                        <td>{duration:.3f}s</td>
                    </tr>
"""
        
        html += """
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>AI数字员工项目 - 自动化测试报告系统</p>
        </div>
    </div>
</body>
</html>
"""
        
        # 保存HTML文件
        output_path = Path('reports') / f"{module_name}_report.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ {module_name}: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ {module_name}: 生成失败 - {e}")
        return False


def main():
    """主函数"""
    print("\n" + "="*80)
    print("  📊 生成模块测试报告")
    print("="*80 + "\n")
    
    reports_dir = Path('reports')
    
    # 定义模块映射
    modules = {
        '认证模块 (Auth)': 'auth_test_results.json',
        '待办模块 (Todo)': 'todo_test_results.json',
        '会议模块 (Meeting)': 'meeting_test_results.json',
        '安全模块 (Security)': 'security_test_results.json',
        'Agent模块': 'agent_test_results.json',
        '集成测试 (Integration)': 'integration_test_results.json',
    }
    
    generated = 0
    for module_name, json_file in modules.items():
        json_path = reports_dir / json_file
        if json_path.exists():
            if generate_module_report(module_name, json_path):
                generated += 1
        else:
            print(f"⚠️  {module_name}: 未找到结果文件")
    
    print("\n" + "="*80)
    print(f"  ✅ 成功生成 {generated} 个报告")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
