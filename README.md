# Japan Car Import Advisory Platform

A data engineering and machine learning platform that helps Kenyan car buyers compare the estimated cost of importing cars from Japan with buying cars locally.

## Features

- Scrape Japanese vehicle listings from SBT Japan, BE FORWARD, JapaneseCarTrade, AAA Japan, and Car From Japan
- Store raw and cleaned car listing data in PostgreSQL
- Clean and standardize vehicle data for analysis
- Estimate Kenya import costs including purchase price, shipping, taxes, port charges, clearing fees, registration, and other charges
- Compare estimated import cost with local Kenyan market prices
- Train a machine learning model to predict Japanese car listing prices
- Provide an interactive dashboard/web application
- Optional ETL orchestration with Airflow
- Containerized with Docker

## Tech Stack

- Python 3.11
- UV for dependency and virtual environment management
- PostgreSQL
- SQLAlchemy
- Pandas
- Requests
- BeautifulSoup
- Playwright
- Scikit-learn
- Streamlit
- Docker
- Optional: Apache Airflow

## Project Structure

```text
japan-car-import-advisory-platform/
├── app/
├── calculator/
├── config/
├── dags/
├── data/
│   ├── raw/
│   ├── cleaned/
│   └── processed/
├── docs/
├── etl/
├── ml/
├── notebooks/
├── presentation/
├── scrapers/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── .python-version
├── .env.example
└── README.md
```

## Quick Start with UV

This project now uses `pyproject.toml` and UV instead of `requirements.txt` and `pip`.

Install UV if you do not have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
```

Clone the project and install dependencies:

```bash
git clone <your-repo-url>
cd japan-car-import-advisory-platform
uv sync --dev
cp .env.example .env
```

Install Playwright browser support when using the Playwright-based scrapers:

```bash
uv run playwright install chromium
```

Run the Streamlit app:

```bash
uv run streamlit run app/streamlit_app.py
```

Run the ETL pipeline manually:

```bash
uv run python -m etl.run_pipeline
```

Train the ML model:

```bash
uv run python -m ml.train_model
```

Run tests:

```bash
uv run pytest
```

Create or refresh the lock file after dependencies resolve successfully:

```bash
uv lock
```

## Optional Airflow Setup

Airflow is kept as an optional dependency because it is heavy and not needed for the basic dashboard or ETL scripts.

```bash
uv sync --dev --extra orchestration
```

Then configure Airflow separately before running DAGs.

## Docker Usage

Start PostgreSQL and the Streamlit app:

```bash
docker compose up --build
```

Open the app at:

```text
http://localhost:8501
```

Stop containers:

```bash
docker compose down
```

## Environment Variables

Copy `.env.example` to `.env` and adjust values as needed:

```bash
cp .env.example .env
```

Important variables:

```text
DATABASE_URL
EXCHANGE_RATE_USD_KES
DEFAULT_SHIPPING_COST_USD
DEFAULT_INSURANCE_RATE
```

<img width="1847" height="928" alt="image" src="https://github.com/user-attachments/assets/e94de6e1-74dd-402d-a36f-421f741f0829" />


<img width="1844" height="907" alt="image" src="https://github.com/user-attachments/assets/c826ae36-aeee-4be0-bfad-2eecd499add0" />


<img width="1844" height="907" alt="image" src="https://github.com/user-attachments/assets/d83fa31e-3e70-4812-88ca-65f854e97f74" />

<img width="1844" height="907" alt="image" src="https://github.com/user-attachments/assets/4fa829b2-fc8a-4edd-9326-19453ac4404a" />



When running locally outside Docker, use a localhost database URL. When running inside Docker Compose, use the `postgres` service hostname.

## Notes on Scraping

- SBT Japan and BE FORWARD can initially be handled using `requests` and `BeautifulSoup`.
- CarFromJapan and AAA Japan may require Playwright, stealth techniques, or proxy services because of CAPTCHA/403 protection.
- Always respect website terms of service and robots.txt.

## Main Deliverables

- Database
- Cleaned dataset
- Scraping scripts
- Import cost calculator
- Machine learning model
- Dashboard/web application
- Documentation
- Final presentation
