"""
安全防护工具
提供敏感词过滤、SQL注入检测等功能
"""
import re
from fastapi import HTTPException, status

# 基础敏感词库（可根据实际需求扩展）
SENSITIVE_WORDS = {
    "政治敏感": ["反动", "暴力", "恐怖"],
    "违规操作": ["删库", "提权", "绕过验证"]
}

# SQL 注入特征正则
SQL_INJECTION_PATTERNS = [
    r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER)\b.*\b(FROM|INTO|TABLE|WHERE)\b)",
    r"(--|#|/\*|\*/|;)",
    r"(\b(OR|AND)\b\s+\d+=\d+)"
]

def sanitize_input(text: str) -> str:
    """
    清理用户输入，防止 XSS 和基础注入
    """
    if not text:
        return ""
    # 移除 HTML 标签
    clean_text = re.sub(r'<[^>]+>', '', text)
    # 移除多余的空格和控制字符
    clean_text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', clean_text)
    return clean_text.strip()

def check_sensitive_words(text: str) -> bool:
    """
    检查是否包含敏感词
    Returns: True 如果包含敏感词
    """
    for category, words in SENSITIVE_WORDS.items():
        for word in words:
            if word in text:
                print(f"[Security] ⚠️ 检测到{category}敏感词: {word}")
                return True
    return False

def detect_sql_injection(text: str) -> bool:
    """
    检测 SQL 注入尝试
    Returns: True 如果检测到注入特征
    """
    for pattern in SQL_INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            print(f"[Security] 🚨 检测到潜在的 SQL 注入特征")
            return True
    return False

def security_guard(text: str):
    """
    统一安全网关：执行所有安全检查
    """
    if not text:
        return
    
    clean_text = sanitize_input(text)
    
    if check_sensitive_words(clean_text):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="输入内容包含不合规信息"
        )
    
    if detect_sql_injection(clean_text):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="检测到非法输入格式"
        )
