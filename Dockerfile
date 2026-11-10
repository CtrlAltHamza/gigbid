# Production Dockerfile for Hugging Face Spaces & Cloud Containers
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PORT=7860

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir -e .

COPY agent/ ./agent/
COPY rag/ ./rag/
COPY mcp_servers/ ./mcp_servers/
COPY gigsim/ ./gigsim/
COPY apps/api/ ./apps/api/
COPY data/ ./data/

# Hugging Face Spaces runs as user ID 1000
RUN useradd -m -u 1000 user && chown -R user:user /app
USER user

EXPOSE 8000 7860

CMD ["sh", "-c", "uvicorn apps.api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

