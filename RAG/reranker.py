"""
RAG 重排序模块
使用Cross-Encoder对检索结果进行精排，提高相关性
"""
from typing import List, Dict
from sentence_transformers import CrossEncoder


class Reranker:
    """重排序器 - 使用Cross-Encoder对检索结果进行精排"""
    
    def __init__(self, model_name: str = "BAAI/bge-reranker-base"):
        """
        初始化重排序器
        
        Args:
            model_name: Cross-Encoder模型名称，如果为None则使用简化版本
        """
        self.model = None
        
        # 尝试加载模型，如果失败则使用简化版本
        if model_name:
            print(f"[Reranker] 尝试加载重排序模型: {model_name}")
            try:
                from sentence_transformers import CrossEncoder
                self.model = CrossEncoder(model_name)
                print(f"[Reranker] ✅ 重排序模型加载完成")
            except Exception as e:
                print(f"[Reranker] ⚠️ 模型加载失败，将使用简化版本（基于相似度分数排序）: {e}")
                self.model = None
        else:
            print("[Reranker] 使用简化版重排序器（基于相似度分数）")
    
    def rerank(self, 
               query: str, 
               documents: List[Dict], 
               top_k: int = 5) -> List[Dict]:
        """
        对检索结果进行重排序
        
        Args:
            query: 查询文本
            documents: 待重排序的文档列表
            top_k: 返回结果数量
            
        Returns:
            重排序后的文档列表
        """
        if not documents:
            return []
        
        if self.model is not None:
            # 使用Cross-Encoder模型进行重排序
            try:
                pairs = [(query, doc['content']) for doc in documents]
                scores = self.model.predict(pairs)
                
                # 添加分数到文档
                for i, doc in enumerate(documents):
                    doc['rerank_score'] = float(scores[i])
                
                # 按重排序分数降序排列
                reranked_docs = sorted(documents, key=lambda x: x.get('rerank_score', 0), reverse=True)
                print(f"[Reranker] 使用Cross-Encoder重排序完成")
                return reranked_docs[:top_k]
            except Exception as e:
                print(f"[Reranker] 重排序失败，使用备用方案: {e}")
                # 降级到基于原始分数的排序
        
        # 备用方案：根据已有的分数排序
        print("[Reranker] 使用基于相似度分数的排序")
        reranked_docs = sorted(
            documents, 
            key=lambda x: x.get('hybrid_score', x.get('relevance_score', 0)), 
            reverse=True
        )
        
        # 添加统一的score字段
        for doc in reranked_docs:
            doc['rerank_score'] = doc.get('hybrid_score', doc.get('relevance_score', 0))
        
        return reranked_docs[:top_k]
    
    def rerank_with_hybrid(self,
                          query: str,
                          hybrid_results: List[Dict],
                          top_k: int = 5) -> List[Dict]:
        """
        对混合检索结果进行重排序
        
        Args:
            query: 查询文本
            hybrid_results: 混合检索结果
            top_k: 返回结果数量
            
        Returns:
            重排序后的结果列表
        """
        return self.rerank(query, hybrid_results, top_k)
