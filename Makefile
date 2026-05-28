.PHONY: setup install browsers app etl train test lint docker-up docker-down

setup:
	uv sync --dev

install:
	uv sync

browsers:
	uv run playwright install chromium

app:
	uv run streamlit run app/streamlit_app.py

etl:
	uv run python -m etl.run_pipeline

train:
	uv run python -m ml.train_model

test:
	uv run pytest

lint:
	uv run ruff check .

docker-up:
	docker compose up --build

docker-down:
	docker compose down
