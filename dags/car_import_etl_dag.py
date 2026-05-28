from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

DEFAULT_ARGS = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="japan_car_import_etl",
    default_args=DEFAULT_ARGS,
    description="ETL pipeline for Japan car import advisory platform",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    run_pipeline = BashOperator(
        task_id="run_car_listing_pipeline",
        bash_command="cd /opt/airflow/project && python etl/run_pipeline.py",
    )

    train_model = BashOperator(
        task_id="train_price_prediction_model",
        bash_command="cd /opt/airflow/project && python ml/train_model.py",
    )

    run_pipeline >> train_model
