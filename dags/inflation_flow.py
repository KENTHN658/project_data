import os
import sys
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from pipelines.inflationrate import extract_data_from_website, transform_website_data, write_website_data



dag = DAG(
    dag_id='inflation_dag',
    default_args={
        "start_date": datetime(2024, 8, 1),
    },
    schedule_interval=timedelta(days=365),
    catchup=False
)

extract_data_from_website = PythonOperator(
    task_id="extract_data_from_website",
    python_callable=extract_data_from_website,
    provide_context=True,
    op_kwargs={"url": "https://www.worlddata.info/america/brazil/inflation-rates.php"},
    dag=dag
)

transform_website_data = PythonOperator(
    task_id='transform_website_data',
    provide_context=True,
    python_callable=transform_website_data,
    dag=dag
)

write_website_data = PythonOperator(
    task_id='write_website_data',
    provide_context=True,
    python_callable=write_website_data,
    dag=dag
)

extract_data_from_website >> transform_website_data >> write_website_data 