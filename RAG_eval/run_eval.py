"""
RAG 评估快速运行脚本
"""
import sys
import os
import asyncio

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from RAG_eval.ragas_evaluator import run_evaluation

if __name__ == "__main__":
    print("🚀 启动 RAG 系统评估...\n")
    
    try:
        # 使用异步方式运行评估
        results = asyncio.run(run_evaluation())
        
        print("\n✅ 评估完成！")
        print(f"📊 平均得分:")
        for metric, score in results['average_scores'].items():
            print(f"   {metric}: {score:.4f}")
        
    except Exception as e:
        print(f"\n❌ 评估失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
