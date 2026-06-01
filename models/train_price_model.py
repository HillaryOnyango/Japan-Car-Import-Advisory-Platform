import os
from pathlib import Path
from decimal import Decimal

import joblib
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

load_dotenv()

MODEL_PATH = Path("data/models/car_price_model.pkl")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "japan_car_import_db")
DB_USER = os.getenv("DB_USER", "car_admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "1900")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def load_training_data():
    query = """
        SELECT
            make,
            model,
            year,
            mileage,
            engine_size_cc,
            fuel_type,
            transmission,
            body_type,
            source_platform,
            price_kes
        FROM cars_cleaned
        WHERE price_kes IS NOT NULL
          AND price_kes > 0
          AND year IS NOT NULL;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            cols = [desc[0] for desc in cur.description]

    df = pd.DataFrame(rows, columns=cols)

    for col in df.columns:
        if df[col].map(lambda x: isinstance(x, Decimal)).any():
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def train():
    df = load_training_data()

    if len(df) < 5:
        raise ValueError(f"Not enough training data. Found {len(df)} rows. Scrape more listings first.")

    target = "price_kes"

    features = [
        "make",
        "model",
        "year",
        "mileage",
        "engine_size_cc",
        "fuel_type",
        "transmission",
        "body_type",
        "source_platform",
    ]

    X = df[features]
    y = df[target]

    numeric_features = ["year", "mileage", "engine_size_cc"]
    categorical_features = [
        "make",
        "model",
        "fuel_type",
        "transmission",
        "body_type",
        "source_platform",
    ]

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    model = RandomForestRegressor(
        n_estimators=300,
        random_state=42,
        min_samples_leaf=2,
        n_jobs=-1,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)

    metrics = {
        "rows": len(df),
        "mae_kes": float(mean_absolute_error(y_test, preds)),
        "rmse_kes": float(root_mean_squared_error(y_test, preds)),
        "r2": float(r2_score(y_test, preds)),
        "features": features,
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"pipeline": pipeline, "metrics": metrics}, MODEL_PATH)

    print("Model trained successfully")
    print(metrics)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    train()
