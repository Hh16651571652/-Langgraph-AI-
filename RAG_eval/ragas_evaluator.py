"""
RAGAS 评估引擎
使用 RAGAS 框架对 RAG 系统进行多维度评估
"""
import os
import sys
import json
import math
from typing import List, Dict, Any
from datetime import datetime
from datasets import Dataset
from dotenv import load_dotenv

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 加载环境变量
load_dotenv()

# 导入 RAGAS
try:
    from ragas import evaluate
    from ragas.metrics import (
        context_precision,
        context_recall,
        faithfulness,
        answer_relevancy,
        answer_similarity,
        answer_correctness
    )
    from ragas.llms import LangchainLLMWrapper
    from ragas.embeddings import LangchainEmbeddingsWrapper
except ImportError:
    print("❌ 请先安装 ragas: pip install ragas")
    sys.exit(1)

# 导入项目模块
from RAG.retriever import get_retriever
from agent.llm import get_qwen_llm


def load_ragas_prompt() -> str:
    """
    从文件加载 RAGAS 评估用的 Prompt 模板
    
    Returns:
        Prompt 模板字符串
    """
    prompt_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'prompt',
        'ragas_evaluator.txt'
    )
    
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️ 警告: 未找到 Prompt 文件 {prompt_file}，使用默认模板")
        return """请基于以下文档内容，简洁直接地回答问题。

要求：
1. 如果文档中有相关信息，请直接给出答案，不要解释
2. 如果文档中没有相关信息，请回答“无法回答”
3. 答案要简洁，控制在100字以内
4. 不要添加额外的说明或总结

文档内容：
{context_text}

问题：{question}

答案："""


class RAGEvaluator:
    """RAG 系统评估器"""
    
    def __init__(self):
        """初始化评估器"""
        print("="*60)
        print("🔍 初始化 RAGAS 评估器")
        print("="*60)
        
        # 获取 RAG 检索器
        self.retriever = get_retriever()
        
        # 获取 LLM
        self.llm = get_qwen_llm()
        
        # 包装 LLM 和 Embeddings 用于 RAGAS
        self.ragas_llm = LangchainLLMWrapper(self.llm)
        self.ragas_embeddings = LangchainEmbeddingsWrapper(self.retriever.vector_db.embeddings)
        
        # 定义评估指标
        self.metrics = [
            context_precision,      # 上下文精确率
            context_recall,         # 上下文召回率
            faithfulness,           # 忠诚度（无幻觉）
            answer_relevancy,       # 答案相关性
            answer_similarity,      # 答案相似度
            answer_correctness      # 答案准确性
        ]
        
        print(f"✅ 评估器初始化完成，将评估 {len(self.metrics)} 个指标")
        print(f"   - {', '.join([m.name for m in self.metrics])}")
    
    async def generate_answers(self, questions: List[str], top_k: int = 5) -> List[Dict]:
        """
        为问题生成答案和检索上下文
        
        Args:
            questions: 问题列表
            top_k: 每个问题检索的文档数量
            
        Returns:
            包含 question, answer, contexts 的列表
        """
        print(f"\n📝 开始为 {len(questions)} 个问题生成答案...")
        
        # 加载 Prompt 模板
        prompt_template = load_ragas_prompt()
        
        results = []
        for i, question in enumerate(questions, 1):
            print(f"  [{i}/{len(questions)}] 处理问题: {question[:50]}...")
            
            try:
                # 检索相关文档（使用异步方法）
                retrieved_docs = await self.retriever.retrieve(question, top_k=top_k)
                contexts = [doc['content'] for doc in retrieved_docs if doc.get('content', '').strip()]
                
                # 确保至少有一个有效的 context
                if not contexts:
                    contexts = ["未找到相关文档"]
                
                # 构建 RAG prompt（最多使用5个文档）
                context_text = "\n\n".join(contexts[:5])  # 最多使用5个文档
                
                # 使用模板生成 Prompt
                prompt = prompt_template.format(
                    context_text=context_text,
                    question=question
                )
                
                # 调用 LLM 生成答案
                response = self.llm.invoke(prompt)
                answer = response.content if hasattr(response, 'content') else str(response)
                
                # 清理答案，确保不为空
                answer = answer.strip()
                if not answer or len(answer) < 5:
                    answer = "根据提供的文档，无法找到相关信患来回答这个问题。"
                
                results.append({
                    "question": question,
                    "answer": answer,
                    "contexts": contexts[:5]  # 最多保留5个上下文
                })
                
            except Exception as e:
                print(f"  ⚠️ 处理问题时出错: {e}")
                import traceback
                traceback.print_exc()
                results.append({
                    "question": question,
                    "answer": "处理失败，无法生成答案。",
                    "contexts": ["未找到相关文档"]
                })
        
        print(f"✅ 答案生成完成")
        return results
    
    async def evaluate_with_ground_truth(
        self, 
        questions: List[str],
        ground_truths: List[str],
        top_k: int = 5
    ) -> Dict[str, Any]:
        """
        使用标准答案进行评估
        
        Args:
            questions: 问题列表
            ground_truths: 标准答案列表
            top_k: 检索文档数量
            
        Returns:
            评估结果
        """
        print("\n" + "="*60)
        print("🚀 开始 RAGAS 评估（含标准答案）")
        print("="*60)
        
        # 生成答案
        generated_results = await self.generate_answers(questions, top_k)
        
        # 准备 RAGAS 数据集
        data_samples = {
            'question': [r['question'] for r in generated_results],
            'answer': [r['answer'] for r in generated_results],
            'contexts': [r['contexts'] for r in generated_results],
            'ground_truth': ground_truths
        }
        
        dataset = Dataset.from_dict(data_samples)
        
        # 执行评估
        print("\n📊 正在计算评估指标...")
        result = evaluate(
            dataset=dataset,
            metrics=self.metrics,
            llm=self.ragas_llm,
            embeddings=self.ragas_embeddings
        )
        
        # 转换为字典
        scores = result.to_pandas().to_dict(orient='records')
        
        # 计算平均分（处理 NaN 值）
        avg_scores = {}
        for metric in self.metrics:
            metric_name = metric.name
            values = [s[metric_name] for s in scores if metric_name in s and not (isinstance(s[metric_name], float) and math.isnan(s[metric_name]))]
            avg_scores[metric_name] = sum(values) / len(values) if values else 0
        
        return {
            "detailed_scores": scores,
            "average_scores": avg_scores,
            "timestamp": datetime.now().isoformat(),
            "num_questions": len(questions),
            "top_k": top_k
        }
    
    async def evaluate_without_ground_truth(
        self,
        questions: List[str],
        top_k: int = 3
    ) -> Dict[str, Any]:
        """
        不使用标准答案进行评估（仅评估检索质量）
        
        Args:
            questions: 问题列表
            top_k: 检索文档数量
            
        Returns:
            评估结果
        """
        print("\n" + "="*60)
        print("🚀 开始 RAGAS 评估（不含标准答案）")
        print("="*60)
        
        # 生成答案
        generated_results = await self.generate_answers(questions, top_k)
        
        # 准备 RAGAS 数据集（不包含 ground_truth）
        data_samples = {
            'question': [r['question'] for r in generated_results],
            'answer': [r['answer'] for r in generated_results],
            'contexts': [r['contexts'] for r in generated_results]
        }
        
        dataset = Dataset.from_dict(data_samples)
        
        # 使用不需要 ground_truth 的指标
        limited_metrics = [
            context_precision,
            faithfulness,
            answer_relevancy
        ]
        
        # 执行评估
        print("\n📊 正在计算评估指标...")
        result = evaluate(
            dataset=dataset,
            metrics=limited_metrics,
            llm=self.ragas_llm,
            embeddings=self.ragas_embeddings
        )
        
        # 转换为字典
        scores = result.to_pandas().to_dict(orient='records')
        
        # 计算平均分（处理 NaN 值）
        avg_scores = {}
        for metric in limited_metrics:
            metric_name = metric.name
            values = [s[metric_name] for s in scores if metric_name in s and not (isinstance(s[metric_name], float) and math.isnan(s[metric_name]))]
            avg_scores[metric_name] = sum(values) / len(values) if values else 0
        
        return {
            "detailed_scores": scores,
            "average_scores": avg_scores,
            "timestamp": datetime.now().isoformat(),
            "num_questions": len(questions),
            "top_k": top_k
        }
    
    def save_results(self, results: Dict, output_file: str = None):
        """
        保存评估结果到文件
        
        Args:
            results: 评估结果
            output_file: 输出文件路径
        """
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"rag_eval/results/evaluation_{timestamp}.json"
        
        # 确保目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # 保存结果
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 评估结果已保存到: {output_file}")
    
    def print_report(self, results: Dict):
        """
        打印评估报告
        
        Args:
            results: 评估结果
        """
        print("\n" + "="*60)
        print("📊 RAG 系统评估报告")
        print("="*60)
        
        avg_scores = results.get('average_scores', {})
        
        print(f"\n评估时间: {results.get('timestamp', 'N/A')}")
        print(f"问题数量: {results.get('num_questions', 0)}")
        print(f"检索参数: top_k={results.get('top_k', 3)}")
        
        print("\n--- 平均得分 ---")
        for metric_name, score in avg_scores.items():
            # 根据指标名称选择图标
            icon_map = {
                'context_precision': '🎯',
                'context_recall': '🔍',
                'faithfulness': '✅',
                'answer_relevancy': '📌',
                'answer_similarity': '🔄',
                'answer_correctness': '✔️'
            }
            icon = icon_map.get(metric_name, '📊')
            
            # 评分等级
            if score >= 0.8:
                level = "优秀 ⭐⭐⭐⭐⭐"
            elif score >= 0.6:
                level = "良好 ⭐⭐⭐⭐"
            elif score >= 0.4:
                level = "一般 ⭐⭐⭐"
            else:
                level = "需改进 ⭐⭐"
            
            print(f"{icon} {metric_name:25s}: {score:.4f}  ({level})")
        
        print("\n--- 详细得分 ---")
        detailed = results.get('detailed_scores', [])
        for i, sample in enumerate(detailed[:5], 1):  # 只显示前5个
            print(f"\n问题 {i}: {sample.get('question', 'N/A')[:60]}...")
            for metric_name in avg_scores.keys():
                if metric_name in sample:
                    print(f"  - {metric_name}: {sample[metric_name]:.4f}")
        
        if len(detailed) > 5:
            print(f"\n... 还有 {len(detailed) - 5} 个问题的详细结果，请查看保存的文件")
        
        print("\n" + "="*60)
        print("💡 改进建议:")
        print("="*60)
        
        # 根据得分给出建议
        if avg_scores.get('context_precision', 0) < 0.6:
            print("⚠️  上下文精确率较低，建议：")
            print("   - 优化 chunk_size 和 chunk_overlap")
            print("   - 考虑使用混合检索（向量+关键词）")
        
        if avg_scores.get('context_recall', 0) < 0.6:
            print("⚠️  上下文召回率较低，建议：")
            print("   - 增加 top_k 值")
            print("   - 优化 embedding 模型")
            print("   - 考虑使用 query 扩展技术")
        
        if avg_scores.get('faithfulness', 0) < 0.7:
            print("⚠️  忠诚度较低（存在幻觉），建议：")
            print("   - 优化 prompt，强调基于文档回答")
            print("   - 降低 temperature 参数")
            print("   - 增加检索文档的相关性阈值")
        
        if avg_scores.get('answer_relevancy', 0) < 0.7:
            print("⚠️  答案相关性较低，建议：")
            print("   - 优化 prompt 结构")
            print("   - 提供更相关的上下文")
        
        print("\n" + "="*60)


async def run_evaluation():
    """运行完整评估流程"""
    from .evaluation_dataset import EVALUATION_DATASET
    
    # 提取问题和标准答案
    questions = [item['question'] for item in EVALUATION_DATASET]
    ground_truths = [item['ground_truth'] for item in EVALUATION_DATASET]
    
    # 创建评估器
    evaluator = RAGEvaluator()
    
    # 执行评估（含标准答案）
    results = await evaluator.evaluate_with_ground_truth(
        questions=questions,
        ground_truths=ground_truths,
        top_k=3
    )
    
    # 打印报告
    evaluator.print_report(results)
    
    # 保存结果
    evaluator.save_results(results)
    
    return results


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_evaluation())
