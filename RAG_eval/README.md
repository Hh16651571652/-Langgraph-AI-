# RAG 评估系统

基于 **RAGAS** (Retrieval Augmented Generation Assessment) 框架的 RAG 系统量化评估工具。

## 📋 功能特性

### 评估指标

| 指标 | 说明 | 范围 | 含义 |
|------|------|------|------|
| **Context Precision** | 上下文精确率 | 0-1 | 检索到的文档中有多少是真正相关的 |
| **Context Recall** | 上下文召回率 | 0-1 | 是否检索到了所有相关文档 |
| **Faithfulness** | 忠诚度 | 0-1 | 生成的答案是否忠实于检索到的上下文（无幻觉） |
| **Answer Relevancy** | 答案相关性 | 0-1 | 答案是否与问题相关 |
| **Answer Similarity** | 答案相似度 | 0-1 | 生成答案与标准答案的语义相似度 |
| **Answer Correctness** | 答案准确性 | 0-1 | 答案的事实正确性 |

### 评分等级

- ⭐⭐⭐⭐⭐ **优秀**: ≥ 0.8
- ⭐⭐⭐⭐ **良好**: ≥ 0.6
- ⭐⭐⭐ **一般**: ≥ 0.4
- ⭐⭐ **需改进**: < 0.4

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r RAG_eval/requirements_eval.txt
```

### 2. 运行评估

```bash
# 在项目根目录执行
python -m RAG_eval.ragas_evaluator
```

或者：

```bash
cd RAG_eval
python ragas_evaluator.py
```

### 3. 查看结果

评估完成后会：
- ✅ 在控制台打印详细报告
- ✅ 保存 JSON 格式结果到 `RAG_eval/results/` 目录
- ✅ 提供改进建议

## 📊 评估数据集

当前评估集包含 **20 个问题**，覆盖以下类别：

- 📝 入职文件（3个）
- 📜 就业政策（6个）
- 💰 福利和优待（5个）
- 📖 操作文档（5个）
- 👥 招聘文件（1个）

难度分布：
- 🔵 简单：6个
- 🟡 中等：9个
- 🔴 困难：5个

### 自定义评估集

编辑 `RAG_eval/evaluation_dataset.py`，添加或修改问题：

```python
EVALUATION_DATASET = [
    {
        "question": "你的问题",
        "ground_truth": "标准答案",
        "expected_categories": ["分类"],
        "difficulty": "easy"  # easy/medium/hard
    },
    # ... 更多问题
]
```

## 📁 文件结构

```
RAG_eval/
├── __init__.py                 # 包初始化
├── evaluation_dataset.py       # 评估测试集
├── ragas_evaluator.py          # RAGAS 评估引擎
├── requirements_eval.txt       # 依赖包
├── README.md                   # 说明文档
└── results/                    # 评估结果输出目录
    └── evaluation_YYYYMMDD_HHMMSS.json
```

## 🔧 高级用法

### 调整检索参数

```python
from RAG_eval.ragas_evaluator import RAGEvaluator

evaluator = RAGEvaluator()

# 使用不同的 top_k
results = evaluator.evaluate_with_ground_truth(
    questions=questions,
    ground_truths=ground_truths,
    top_k=5  # 默认是 3
)
```

### 不使用标准答案评估

如果还没有标注标准答案，可以只评估检索质量：

```python
results = evaluator.evaluate_without_ground_truth(
    questions=questions,
    top_k=3
)
```

这会评估以下指标：
- Context Precision
- Faithfulness
- Answer Relevancy

### 批量评估不同配置

```python
# 比较不同 top_k 的效果
for k in [1, 3, 5, 10]:
    results = evaluator.evaluate_with_ground_truth(
        questions=questions,
        ground_truths=ground_truths,
        top_k=k
    )
    print(f"top_k={k}: {results['average_scores']}")
```

## 📈 结果解读示例

```
📊 RAG 系统评估报告
============================================================

评估时间: 2026-05-12T15:30:00
问题数量: 20
检索参数: top_k=3

--- 平均得分 ---
🎯 context_precision        : 0.7234  (良好 ⭐⭐⭐⭐)
🔍 context_recall           : 0.6891  (良好 ⭐⭐⭐⭐)
✅ faithfulness             : 0.8456  (优秀 ⭐⭐⭐⭐⭐)
📌 answer_relevancy         : 0.7823  (良好 ⭐⭐⭐⭐)
🔄 answer_similarity        : 0.6547  (良好 ⭐⭐⭐⭐)
✔️ answer_correctness       : 0.7012  (良好 ⭐⭐⭐⭐)

💡 改进建议:
============================================================
⚠️  上下文召回率较低，建议：
   - 增加 top_k 值
   - 优化 embedding 模型
   - 考虑使用 query 扩展技术
```

## 🎯 优化建议

根据评估结果，可以采取以下优化措施：

### 如果 Context Precision 低
- 减小 `chunk_size`（当前500，尝试300）
- 提高 `min_relevance_score` 阈值
- 使用混合检索（向量+关键词）

### 如果 Context Recall 低
- 增加 `top_k` 值
- 升级到更好的 embedding 模型（text-embedding-v3）
- 使用 query 扩展技术

### 如果 Faithfulness 低
- 优化 prompt，强调"基于文档回答"
- 降低 LLM 的 temperature 参数
- 过滤低相关性文档

### 如果 Answer Relevancy 低
- 改进 prompt 结构
- 提供更相关的上下文
- 增加后处理步骤

## 📝 注意事项

1. **首次运行较慢**：RAGAS 需要调用 LLM 进行评估，20个问题大约需要 5-10 分钟
2. **API 费用**：评估过程会消耗 DashScope API 额度
3. **稳定性**：确保网络连接稳定，避免中断
4. ** reproducibility**：保存每次评估结果，便于对比优化效果

## 🔗 相关资源

- [RAGAS 官方文档](https://docs.ragas.io/)
- [RAGAS GitHub](https://github.com/explodinggradients/ragas)
- [评估指标详解](https://docs.ragas.io/en/latest/concepts/metrics/index.html)

## 📞 问题反馈

如有问题或建议，请创建 Issue 或联系开发团队。
