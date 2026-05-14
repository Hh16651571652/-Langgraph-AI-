"""生成综合测试报告界面"""
import json
from datetime import datetime
from pathlib import Path


def generate_dashboard():
    """生成综合测试报告仪表盘"""
    
    # 读取所有模块的测试结果
    modules = {
        '认证模块 (Auth)': 'auth_test_results.json',
        '待办模块 (Todo)': 'todo_test_results.json',
        '会议模块 (Meeting)': 'meeting_test_results.json',
        '安全模块 (Security)': 'security_test_results.json',
        'Agent模块': 'agent_test_results.json',
        '集成测试 (Integration)': 'integration_test_results.json',
    }
    
    module_data = []
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
            passed = s.get('passed', 0)
            failed = s.get('failed', 0)
            skipped = s.get('skipped', 0)
            total = s.get('total', 0)
            
            total_tests += total
            total_passed += passed
            total_failed += failed
            total_skipped += skipped
            
            pass_rate = (passed / total * 100) if total > 0 else 0
            
            module_data.append({
                'name': module_name,
                'total': total,
                'passed': passed,
                'failed': failed,
                'skipped': skipped,
                'pass_rate': pass_rate,
                'status': 'success' if failed == 0 else 'warning' if passed > 0 else 'danger'
            })
    
    overall_pass_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    # 确定总体状态
    if total_failed == 0:
        overall_status = "✅ 全部通过"
        status_color = "#52c41a"
    elif total_passed > 0:
        overall_status = "⚠️ 部分失败"
        status_color = "#faad14"
    else:
        overall_status = "❌ 全部失败"
        status_color = "#ff4d4f"
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI数字员工 - 综合测试报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .dashboard {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.8em;
            color: #667eea;
            margin-bottom: 10px;
        }}
        .header .subtitle {{
            color: #666;
            font-size: 1.2em;
            margin-bottom: 20px;
        }}
        .overall-status {{
            display: inline-block;
            padding: 15px 40px;
            background: {status_color};
            color: white;
            border-radius: 30px;
            font-size: 1.5em;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.25);
        }}
        .stat-card h3 {{
            color: #666;
            font-size: 1em;
            margin-bottom: 15px;
            text-transform: uppercase;
        }}
        .stat-card .value {{
            font-size: 3.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .stat-card.total .value {{ color: #667eea; }}
        .stat-card.passed .value {{ color: #52c41a; }}
        .stat-card.failed .value {{ color: #ff4d4f; }}
        .stat-card.skipped .value {{ color: #faad14; }}
        .progress-section {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            margin-bottom: 30px;
        }}
        .progress-section h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        .progress-bar-container {{
            background: #e0e0e0;
            border-radius: 15px;
            height: 40px;
            overflow: hidden;
            position: relative;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
        }}
        .progress-bar-fill {{
            background: linear-gradient(90deg, #52c41a 0%, #73d13d 50%, #95de64 100%);
            height: 100%;
            width: {overall_pass_rate}%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 1.2em;
            transition: width 1.5s ease;
            box-shadow: 0 2px 10px rgba(82, 196, 26, 0.3);
        }}
        .modules-section {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            margin-bottom: 30px;
        }}
        .modules-section h2 {{
            color: #333;
            margin-bottom: 30px;
            font-size: 1.8em;
        }}
        .module-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }}
        .module-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid;
            box-shadow: 0 3px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        .module-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 6px 25px rgba(0,0,0,0.15);
        }}
        .module-card.success {{ border-left-color: #52c41a; }}
        .module-card.warning {{ border-left-color: #faad14; }}
        .module-card.danger {{ border-left-color: #ff4d4f; }}
        .module-card h3 {{
            color: #333;
            font-size: 1.3em;
            margin-bottom: 15px;
        }}
        .module-stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            margin-bottom: 15px;
        }}
        .module-stat {{
            text-align: center;
            padding: 10px;
            background: white;
            border-radius: 8px;
        }}
        .module-stat .label {{
            font-size: 0.8em;
            color: #666;
            margin-bottom: 5px;
        }}
        .module-stat .number {{
            font-size: 1.5em;
            font-weight: bold;
            color: #333;
        }}
        .module-progress {{
            background: #e0e0e0;
            border-radius: 10px;
            height: 25px;
            overflow: hidden;
            position: relative;
        }}
        .module-progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #52c41a, #73d13d);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
            transition: width 1s ease;
        }}
        .footer {{
            text-align: center;
            padding: 30px;
            color: white;
            font-size: 1.1em;
        }}
        .report-links {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            margin-top: 30px;
        }}
        .report-links h2 {{
            color: #333;
            margin-bottom: 20px;
        }}
        .link-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }}
        .report-link {{
            display: block;
            padding: 15px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        .report-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>🧪 AI数字员工 - 综合测试报告</h1>
            <p class="subtitle">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <div class="overall-status">{overall_status}</div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card total">
                <h3>总测试数</h3>
                <div class="value">{total_tests}</div>
            </div>
            <div class="stat-card passed">
                <h3>通过</h3>
                <div class="value">{total_passed}</div>
            </div>
            <div class="stat-card failed">
                <h3>失败</h3>
                <div class="value">{total_failed}</div>
            </div>
            <div class="stat-card skipped">
                <h3>跳过</h3>
                <div class="value">{total_skipped}</div>
            </div>
        </div>
        
        <div class="progress-section">
            <h2>📊 总体通过率</h2>
            <div class="progress-bar-container">
                <div class="progress-bar-fill">{overall_pass_rate:.1f}%</div>
            </div>
        </div>
        
        <div class="modules-section">
            <h2>📋 各模块详情</h2>
            <div class="module-cards">
"""
    
    for module in module_data:
        status_class = module['status']
        html += f"""
                <div class="module-card {status_class}">
                    <h3>{module['name']}</h3>
                    <div class="module-stats">
                        <div class="module-stat">
                            <div class="label">总计</div>
                            <div class="number">{module['total']}</div>
                        </div>
                        <div class="module-stat">
                            <div class="label">通过</div>
                            <div class="number" style="color: #52c41a;">{module['passed']}</div>
                        </div>
                        <div class="module-stat">
                            <div class="label">失败</div>
                            <div class="number" style="color: #ff4d4f;">{module['failed']}</div>
                        </div>
                        <div class="module-stat">
                            <div class="label">跳过</div>
                            <div class="number" style="color: #faad14;">{module['skipped']}</div>
                        </div>
                    </div>
                    <div class="module-progress">
                        <div class="module-progress-fill" style="width: {module['pass_rate']:.1f}%;">
                            {module['pass_rate']:.1f}%
                        </div>
                    </div>
                </div>
"""
    
    html += """
            </div>
        </div>
        
        <div class="report-links">
            <h2>📄 查看详细报告</h2>
            <div class="link-grid">
"""
    
    for module in module_data:
        # 使用实际的文件名（与 generate_module_reports.py 生成的文件名一致）
        filename = f"{module['name']}_report.html"
        html += f'                <a href="{filename}" class="report-link">{module["name"]} 详细报告</a>\n'
    
    html += """
            </div>
        </div>
        
        <div class="footer">
            <p>AI数字员工项目 - 自动化测试报告系统</p>
            <p style="margin-top: 10px; opacity: 0.8;">Powered by pytest + HTML Report Generator</p>
        </div>
    </div>
</body>
</html>
"""
    
    # 保存报告
    output_path = Path('reports') / 'comprehensive_report.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ 综合测试报告已生成: {output_path}")
    print(f"   总测试数: {total_tests}")
    print(f"   通过率: {overall_pass_rate:.1f}%")
    print(f"   状态: {overall_status}\n")


if __name__ == "__main__":
    generate_dashboard()
