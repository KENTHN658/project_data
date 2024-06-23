# project_data
1. echo -e "AIRFLOW_UID=$(id -u)" > .env
2. pip install requirements.txt
3. docker compose up airflow-init
4. docker compose up
