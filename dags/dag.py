import os
import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from pipelines.alphavantage_pipeline import alphavantage_pipeline


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 22),    
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

file_postfix = datetime.now().strftime("%Y%m%d")

dag = DAG(
    dag_id='etl_income_statement_pipeline',
    default_args=default_args,
    catchup=False,
    tags=['reddit', 'etl', 'pipeline']
)

extract = PythonOperator(
    task_id='income_extraction',
    python_callable=alphavantage_pipeline,
    op_kwargs={
        'file_name': f'income_{file_postfix}',
    },
    dag=dag
)

extract 