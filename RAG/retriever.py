"""
RAG 检索器模块
提供文档检索功能，支持混合检索、重排序和查询扩展
"""
from typing import List, Dict, Optional
from .vector_db import VectorDatabase
from .hybrid_retriever import HybridRetriever
from .reranker import Reranker
from .query_expansion import get_query_expander
from agent.llm import get_qwen_llm


class RAGRetriever:
    """RAG检索器 - 支持混合检索、重排序和查询优化"""
    
    def __init__(self, vector_db: VectorDatabase, use_hybrid: bool = True, use_rerank: bool = True):
        """
        初始化检索器
        
        Args:
            vector_db: 向量数据库实例
            use_hybrid: 是否使用混合检索
            use_rerank: 是否使用重排序
        """
        self.vector_db = vector_db
        self.use_hybrid = use_hybrid
        self.use_rerank = use_rerank
        
        # 初始化混合检索器
        if use_hybrid:
            self.hybrid_retriever = HybridRetriever(vector_db)
        else:
            self.hybrid_retriever = None
        
        # 初始化重排序器
        if use_rerank:
            self.reranker = Reranker()
        else:
            self.reranker = None
        
        # 初始化LLM（用于查询扩展）
        self.llm = get_qwen_llm(temperature=0.3)
        
        # 初始化查询扩展器
        self.query_expander = get_query_expander()
    
    async def retrieve(self, 
                 query: str, 
                 top_k: int = 5,
                 filter_category: str = None,
                 min_relevance_score: float = 0.3,
                 use_query_expansion: bool = True) -> List[Dict]:
        """
        检索相关文档（支持混合检索、重排序和查询扩展）
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            filter_category: 可选的分类过滤
            min_relevance_score: 最小相关性分数阈值
            use_query_expansion: 是否使用查询扩展
            
        Returns:
            检索结果列表（按相关性排序）
        """
        # 查询扩展
        if use_query_expansion:
            expanded_queries = await self.query_expander.expand_query(query, num_variants=2)
            print(f"[RAGRetriever] 使用查询扩展，共 {len(expanded_queries)} 个查询")
        else:
            expanded_queries = [query]
        
        # 对每个扩展查询进行检索并合并结果
        all_results = []
        for exp_query in expanded_queries:
            # 执行混合检索
            if self.use_hybrid and self.hybrid_retriever:
                results = self.hybrid_retriever.hybrid_search(
                    query=exp_query,
                    top_k=top_k * 2,
                    filter_category=filter_category,
                    vector_weight=0.7,  # 语义权重调整为0.7
                    bm25_weight=0.3     # 关键词权重提升为0.3
                )
            else:
                # 纯向量检索
                results = self.vector_db.search(
                    query=exp_query,
                    n_results=top_k * 2,
                    filter_category=filter_category
                )
            all_results.extend(results)
        
        print(f"[RAGRetriever] 合并后共 {len(all_results)} 个结果")
        
        # 去重（基于文档ID）
        seen_ids = set()
        unique_results = []
        for result in all_results:
            doc_id = result.get('id', '')
            if doc_id not in seen_ids:
                seen_ids.add(doc_id)
                unique_results.append(result)
        
        print(f"[RAGRetriever] 去重后 {len(unique_results)} 个结果")
        
        # 重排序
        if self.use_rerank and self.reranker and len(unique_results) > 0:
            unique_results = self.reranker.rerank(query, unique_results, top_k=top_k * 2)
            print(f"[RAGRetriever] 完成重排序")
        
        # 过滤低相关性结果
        filtered_results = [
            r for r in unique_results 
            if r.get('hybrid_score', r.get('rerank_score', r.get('relevance_score', 0))) >= min_relevance_score
        ]
        
        # 按相关性排序并截取top_k
        if self.use_rerank and self.reranker:
            sorted_results = sorted(
                filtered_results, 
                key=lambda x: x.get('rerank_score', 0), 
                reverse=True
            )[:top_k]
        elif self.use_hybrid and self.hybrid_retriever:
            sorted_results = sorted(
                filtered_results, 
                key=lambda x: x.get('hybrid_score', 0), 
                reverse=True
            )[:top_k]
        else:
            sorted_results = sorted(
                filtered_results, 
                key=lambda x: x.get('relevance_score', 0), 
                reverse=True
            )[:top_k]
        
        return sorted_results
    
    async def retrieve_with_context(self, 
                              query: str, 
                              top_k: int = 3,
                              include_metadata: bool = True) -> str:
        """
        检索并格式化上下文
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            include_metadata: 是否包含元数据
            
        Returns:
            格式化的上下文字符串
        """
        results = await self.retrieve(query, top_k=top_k)
        
        if not results:
            return "未找到相关文档。"
        
        # 构建上下文
        context_parts = []
        for i, result in enumerate(results, 1):
            metadata = result.get('metadata', {})
            category = metadata.get('category', '未知分类')
            filename = metadata.get('filename', '未知文件')
            content = result.get('content', '')
            
            # 获取相关性分数
            score = result.get('rerank_score', result.get('hybrid_score', result.get('relevance_score', 0)))
            
            if include_metadata:
                context_parts.append(
                    f"[文档 {i}] (相关性: {score:.2f}) ({category}/{filename})\n{content}"
                )
            else:
                context_parts.append(content)
        
        return "\n\n".join(context_parts)
    
    async def is_relevant(self, query: str, threshold: float = 0.4) -> bool:
        """
        判断是否有相关文档
        
        Args:
            query: 查询文本
            threshold: 相关性阈值
            
        Returns:
            是否有相关文档
        """
        results = await self.retrieve(query, top_k=1, min_relevance_score=threshold)
        return len(results) > 0
    
    def get_categories(self) -> List[str]:
        """获取所有可用的分类"""
        # ChromaDB不直接支持获取唯一值，这里返回预定义的分类
        return [
            "入职文件",
            "就业政策",
            "招聘文件",
            "操作文档",
            "福利和优待"
        ]


# 全局检索器实例（懒加载）
_retriever_instance = None


def get_retriever() -> RAGRetriever:
    """
    获取全局检索器实例（单例模式）
    
    Returns:
        RAGRetriever实例
    """
    global _retriever_instance
    
    if _retriever_instance is None:
        from .vector_db import initialize_rag_database
        # 使用默认参数，自动检测DATA目录
        vector_db = initialize_rag_database()
        _retriever_instance = RAGRetriever(vector_db)
    
    return _retriever_instance


if __name__ == "__main__":
    # 测试代码
    retriever = get_retriever()
    
    print("="*60)
    print("🔍 测试RAG检索器")
    print("="*60)
    
    test_queries = [
        "如何申请年假？",
        "公司的远程工作政策是什么？",
        "新员工需要完成哪些入职手续？",
        "今天的天气怎么样？"  # 这个应该不相关
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"查询: {query}")
        print(f"{'='*60}")
        
        # 检查是否相关
        is_relevant = retriever.is_relevant(query)
        print(f"是否相关: {'✅ 是' if is_relevant else '❌ 否'}")
        
        if is_relevant:
            # 检索文档
            results = retriever.retrieve(query, top_k=3)
            print(f"\n找到 {len(results)} 个相关文档:\n")
            
            for i, result in enumerate(results, 1):
                metadata = result.get('metadata', {})
                print(f"{i}. [{metadata.get('category', 'N/A')}] {metadata.get('filename', 'N/A')}")
                print(f"   相关性: {result.get('relevance_score', 0):.2f}")
                print(f"   内容: {result.get('content', '')[:150]}...")
                print()
            
            # 获取格式化上下文
            context = retriever.retrieve_with_context(query, top_k=2)
            print(f"格式化上下文预览:\n{context[:300]}...")
