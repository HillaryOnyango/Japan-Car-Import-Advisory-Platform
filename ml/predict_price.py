import joblib
import pandas as pd

MODEL_PATH = "ml/car_price_model.joblib"


def predict_price(input_data: dict) -> float:
    model = joblib.load(MODEL_PATH)
    df = pd.DataFrame([input_data])
    return float(model.predict(df)[0])
