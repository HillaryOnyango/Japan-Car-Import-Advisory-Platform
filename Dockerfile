FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml README.md ./
RUN uv sync --no-dev

COPY . .

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "app/streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]
