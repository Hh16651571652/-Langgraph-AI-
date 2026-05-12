"""
查询扩展模块 - 对用户问题进行优化和扩展
"""
import asyncio
from typing import List
from agent.llm import get_qwen_llm


class QueryExpander:
    """查询扩展器 - 使用 LLM 生成问题的多个变体"""
    
    def __init__(self):
        """初始化查询扩展器"""
        self.llm = get_qwen_llm()
        
    async def expand_query(self, original_query: str, num_variants: int = 3) -> List[str]:
        """
        对原始查询进行扩展，生成多个相关变体
        
        Args:
            original_query: 原始用户问题
            num_variants: 生成的变体数量（默认3个）
            
        Returns:
            包含原始问题和扩展问题的列表
        """
        prompt = f"""你是一个专业的查询扩展助手。请为以下用户问题生成 {num_variants} 个语义相关但表述不同的变体问题。

要求：
1. 保持原问题的核心意图不变
2. 使用不同的词汇和句式表达相同的意思
3. 可以考虑从不同角度提问（如：具体细节、应用场景、相关概念等）
4. 每个变体问题应该简洁明了
5. 直接输出变体问题，每行一个，不要编号

原始问题：{original_query}

生成的变体问题："""
        
        try:
            response = await self.llm.ainvoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)
            
            # 解析生成的变体
            variants = [line.strip() for line in content.split('\n') if line.strip()]
            
            # 限制数量并过滤掉与原始问题完全相同的
            variants = [v for v in variants[:num_variants] if v != original_query]
            
            # 将原始问题也加入列表
            all_queries = [original_query] + variants
            
            print(f"[QueryExpander] 原始问题: {original_query}")
            print(f"[QueryExpander] 生成 {len(variants)} 个变体")
            for i, v in enumerate(variants, 1):
                print(f"  变体{i}: {v}")
            
            return all_queries
            
        except Exception as e:
            print(f"[QueryExpander] 查询扩展失败: {e}，返回原始问题")
            return [original_query]
    
    async def expand_and_deduplicate(self, queries: List[str]) -> List[str]:
        """
        对多个查询进行扩展并去重
        
        Args:
            queries: 原始查询列表
            
        Returns:
            扩展并去重后的查询列表
        """
        all_expanded = []
        
        for query in queries:
            expanded = await self.expand_query(query)
            all_expanded.extend(expanded)
        
        # 去重（保持顺序）
        seen = set()
        unique_queries = []
        for q in all_expanded:
            if q not in seen:
                seen.add(q)
                unique_queries.append(q)
        
        print(f"[QueryExpander] 扩展前: {len(queries)} 个查询，扩展后: {len(unique_queries)} 个唯一查询")
        return unique_queries


# 全局实例
_query_expander = None

def get_query_expander() -> QueryExpander:
    """获取查询扩展器单例"""
    global _query_expander
    if _query_expander is None:
        _query_expander = QueryExpander()
    return _query_expander
