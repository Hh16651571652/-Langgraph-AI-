"""
RAG 混合检索模块
结合向量检索和BM25关键词检索，提高检索精度
"""
import os
import jieba
from typing import List, Dict, Optional
from rank_bm25 import BM25Okapi
from .vector_db import VectorDatabase


class HybridRetriever:
    """混合检索器 - 结合向量检索和BM25关键词检索"""
    
    def __init__(self, vector_db: VectorDatabase):
        """
        初始化混合检索器
        
        Args:
            vector_db: 向量数据库实例
        """
        self.vector_db = vector_db
        self.bm25 = None
        self.documents = []
        self.tokenized_docs = []
        
        # 初始化BM25索引
        self._initialize_bm25()
    
    def _initialize_bm25(self):
        """初始化BM25索引"""
        print("[HybridRetriever] 初始化BM25索引...")
        
        # 从向量数据库获取所有文档
        collection = self.vector_db.collection
        all_docs = collection.get(include=['documents'])
        
        if all_docs and all_docs['documents']:
            self.documents = all_docs['documents']
            
            # 对中文文档进行分词
            self.tokenized_docs = []
            for doc in self.documents:
                # 使用jieba进行中文分词
                tokens = list(jieba.cut(doc))
                # 过滤掉停用词和单字符
                tokens = [token for token in tokens if len(token.strip()) > 1]
                self.tokenized_docs.append(tokens)
            
            # 创建BM25索引
            self.bm25 = BM25Okapi(self.tokenized_docs)
            print(f"[HybridRetriever] ✅ BM25索引初始化完成，共 {len(self.documents)} 个文档")
        else:
            print("[HybridRetriever] ⚠️ 未找到文档，BM25索引未初始化")
    
    def bm25_search(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        使用BM25进行关键词检索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            
        Returns:
            检索结果列表
        """
        if not self.bm25 or not self.documents:
            return []
        
        # 对查询进行分词
        query_tokens = list(jieba.cut(query))
        query_tokens = [token for token in query_tokens if len(token.strip()) > 1]
        
        if not query_tokens:
            return []
        
        # 执行BM25搜索
        scores = self.bm25.get_scores(query_tokens)
        
        # 获取top_k个最高分的文档索引
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        
        results = []
        for idx in top_indices:
            if scores[idx] > 0:  # 只返回有分数的结果
                results.append({
                    "content": self.documents[idx],
                    "bm25_score": float(scores[idx]),
                    "index": idx
                })
        
        return results
    
    def vector_search(self, query: str, top_k: int = 10, filter_category: str = None) -> List[Dict]:
        """
        使用向量检索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            filter_category: 可选的分类过滤
            
        Returns:
            检索结果列表
        """
        return self.vector_db.search(
            query=query,
            n_results=top_k,
            filter_category=filter_category
        )
    
    def hybrid_search(self, 
                     query: str, 
                     top_k: int = 5,
                     filter_category: str = None,
                     vector_weight: float = 0.7,
                     bm25_weight: float = 0.3) -> List[Dict]:
        """
        混合检索 - 结合向量检索和BM25检索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            filter_category: 可选的分类过滤
            vector_weight: 向量检索权重
            bm25_weight: BM25检索权重
            
        Returns:
            混合检索结果列表
        """
        # 获取两种检索的结果
        vector_results = self.vector_search(query, top_k=top_k * 2, filter_category=filter_category)
        bm25_results = self.bm25_search(query, top_k=top_k * 2)
        
        # 标准化分数
        vector_scores = {}
        for i, result in enumerate(vector_results):
            # 使用relevance_score作为向量分数
            vector_scores[result['content']] = result.get('relevance_score', 0)
        
        bm25_scores = {}
        for result in bm25_results:
            bm25_scores[result['content']] = result['bm25_score']
        
        # 合并结果并计算加权分数
        all_contents = set(list(vector_scores.keys()) + list(bm25_scores.keys()))
        
        # 归一化分数到0-1范围
        max_vector_score = max(vector_scores.values()) if vector_scores else 1.0
        max_bm25_score = max(bm25_scores.values()) if bm25_scores else 1.0
        
        combined_results = []
        for content in all_contents:
            v_score = vector_scores.get(content, 0) / max_vector_score if max_vector_score > 0 else 0
            b_score = bm25_scores.get(content, 0) / max_bm25_score if max_bm25_score > 0 else 0
            
            # 加权组合
            final_score = vector_weight * v_score + bm25_weight * b_score
            
            # 查找元数据
            metadata = {}
            for result in vector_results:
                if result['content'] == content:
                    metadata = result.get('metadata', {})
                    break
            
            combined_results.append({
                "content": content,
                "metadata": metadata,
                "hybrid_score": final_score,
                "vector_score": v_score,
                "bm25_score": b_score
            })
        
        # 按混合分数排序并返回top_k
        combined_results.sort(key=lambda x: x['hybrid_score'], reverse=True)
        
        return combined_results[:top_k]
