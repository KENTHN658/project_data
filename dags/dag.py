import os
import sys
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from pipelines.inflation_pipeline import inflation_pipeline


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 22),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

def run_inflation_rates_pipeline():
    current_year = datetime.now().year
    file_name = f'inflation_rates_{current_year}'
    url = "https://www.worlddata.info/america/brazil/inflation-rates.php"
    inflation_pipeline(file_name, url)

with DAG(
    'inflation_rates_pipeline_dag',
    default_args=default_args,
    description='DAG for fetching and processing inflation rates for Brazil',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:
    run_pipeline = PythonOperator(
        task_id='run_inflation_pipeline',
        python_callable=run_inflation_rates_pipeline,
    )

run_pipeline