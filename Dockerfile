# app/Dockerfile

# FROM python:3.9-slim
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN uv init
RUN uv venv
RUN uv pip install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/healthz

ENTRYPOINT ["uv", "run", "streamlit", "run", "About.py", "--server.port=8501", "--server.address=0.0.0.0"]
