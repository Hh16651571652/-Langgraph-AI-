FROM python:3.11-slim

WORKDIR /app

# 复制依赖文件
COPY requirements_llm.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements_llm.txt

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 8080

# 启动命令
CMD ["python", "ai-project-main.py"]
