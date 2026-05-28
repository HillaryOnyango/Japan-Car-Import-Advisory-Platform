import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATA_PATH = "data/cleaned/car_listings_cleaned.csv"
MODEL_PATH = "ml/car_price_model.joblib"


def train_model():
    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=["price_usd"])

    features = [
        "make", "model", "year", "mileage_km", "engine_size_cc",
        "fuel_type", "transmission", "body_type", "source_platform"
    ]
    target = "price_usd"

    X = df[features]
    y = df[target]

    categorical_features = ["make", "model", "fuel_type", "transmission", "body_type", "source_platform"]
    numeric_features = ["year", "mileage_km", "engine_size_cc"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("regressor", RandomForestRegressor(n_estimators=200, random_state=42)),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print("MAE:", mean_absolute_error(y_test, predictions))
    print("RMSE:", mean_squared_error(y_test, predictions, squared=False))
    print("R2:", r2_score(y_test, predictions))

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


def main():
    train_model()


if __name__ == "__main__":
    main()
