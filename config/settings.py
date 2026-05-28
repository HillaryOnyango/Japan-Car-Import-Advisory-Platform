from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/japan_car_import_db")
    exchange_rate_usd_kes: float = float(os.getenv("EXCHANGE_RATE_USD_KES", "130"))
    default_shipping_cost_usd: float = float(os.getenv("DEFAULT_SHIPPING_COST_USD", "1200"))
    default_insurance_rate: float = float(os.getenv("DEFAULT_INSURANCE_RATE", "0.015"))

settings = Settings()
