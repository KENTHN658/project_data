import os
import sys
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from pipelines.uploadmanual import write_kaggle_data



dag = DAG(
    dag_id='ecom_dag',
    default_args={
         'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2024, 6, 22),
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1),
    },
    catchup=False,
)

write_kaggle_data = PythonOperator(
    task_id='write_kaggle_data',
    provide_context=True,
    python_callable=write_kaggle_data,
    dag=dag
)

write_kaggle_data 