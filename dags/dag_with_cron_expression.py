from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "julionevadod",
    "retries": 5,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    default_args=default_args,
    dag_id="dag_with_cron_expression_v04",
    start_date=datetime(2024,4,8),
    schedule_interval="0 3 * * Tue-Fri" #This is from Tuesday to Friday at 3 AM (3:00) #Q: Why this, running on 22 APR at 23:36 executes every run except FRI 19? A: It seems like it runs when next should run
    #schedule_interval="0 3 * * Tue,Fri" # This is every Tuesday and Friday at 3 AM (3:00)
    #schedule_interval="0 3 * * Tue" # This is every Tuesday at 3 AM (3:00)
    #schedule_interval="0 0 * * *" # This is exactly the same as "@daily". Check this URL to get cron extensions: https://crontab.guru
) as dag:
    
    task1 = BashOperator(
        task_id="task1",
        bash_command="echo dag with cron expression!"
    )

    task1