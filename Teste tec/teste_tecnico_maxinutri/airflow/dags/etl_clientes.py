from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 5, 1),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='dbt_exec_existing_container',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['dbt', 'docker']
) as dag:

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=(
            "docker exec dbt "  # usa o nome do container definido em docker-compose.yml
            "dbt run --profiles-dir /usr/app"
        )
    )

    dbt_run
