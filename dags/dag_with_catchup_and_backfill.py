from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "julionevadod",
    "retries": 5,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id="dag_with_catchup_backfill_v02",
    default_args=default_args,
    start_date=datetime(2024,4,20),
    schedule_interval="@daily",
    catchup=False # True is default value. It helps run the dag from start_date, Avoids running the DAG several times. Q: Why once???
                    # If setting False, it is not going to run from start date. Backfill can be done manually by logging into AIRFLOW scheduler and running: airflow dag backfill -s START_DATE -e END_DATE DAG_NAME 
) as dag:
    task1 = BashOperator(
        task_id="task1",
        bash_command="echo This is a simple bash command!"
    )
