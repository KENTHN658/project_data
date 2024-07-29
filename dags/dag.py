import os
import sys
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from pipelines.alphavantage_pipeline import alphavantage_pipeline


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 22),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

def run_alphavantage_pipeline():
    file_name = 'income_statement_IBM'
    subreddit = 'financialdata'
    alphavantage_pipeline(file_name)

with DAG(
    'alphavantage_income_statement_dag',
    default_args=default_args,
    description='DAG for fetching and processing income statements from Alpha Vantage',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    run_pipeline = PythonOperator(
        task_id='run_alphavantage_pipeline',
        python_callable=run_alphavantage_pipeline,
    )

run_pipeline

