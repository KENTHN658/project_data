from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from pipelines.alphavantage_pipeline import income_pipeline


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 22),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_income_statement_pipeline():
    file_name = 'income_statement_IBM'
    income_pipeline(file_name)

with DAG(
    'etl_income_statement_pipeline',
    default_args=default_args,
    description='DAG for fetching and processing income statements from Alpha Vantage',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    run_pipeline = PythonOperator(
        task_id='income_extraction',
        python_callable=run_income_statement_pipeline,
    )

run_pipeline
