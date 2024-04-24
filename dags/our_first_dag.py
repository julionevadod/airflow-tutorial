from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "julionevadod", #This appears on web UI
    "retries": 5,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id="our_first_dag_v5",
    default_args=default_args,
    description="This is our first dag that we write",
    start_date=datetime(2024,4,10,3), #Run workflow from 10th April of 2025 at 3. 
                                     #If this is set a year ago from today and you activate DAG, this is going to be run 365 times :). Logical time will show all of these days. 
                                     #Past runs are triggered at 00:00? -> Not easy to undserstand. Schedule intervals divide time. Runs are triggered at the end of the slot, not at the beginning
    schedule_interval="@daily" #Daily trigger. Appears on web UI
) as dag:
    task1 = BashOperator(
        task_id="first_task",
        bash_command="echo hello world, this is the first task!"
    )
    
    task2 = BashOperator(
        task_id="second_task",
        bash_command="echo hey, I am task2 and will be running after"
    )

    task3 = BashOperator(
        task_id="third_task",
        bash_command="echo hey, I am task3 and will be running after task 1"
    )

    # Task 2 and 3 depend on 1: OPTION 1
    # task1.set_downstream(task2) #This creates a dependency of task 2 on task 1 end. If omitted, task1 and 2 could run in parallel
    # task1.set_downstream(task3) #This creates a dependency of task 3 on task 1 end. If omitted, task1 and 3 could run in parallel

    # Task 2 and 3 depend on 1: OPTION 2
    # task1 >> task2 # These two lines are exactly the same as the two above
    # task1 >> task3

    # Task 2 and 3 depend on 1: OPTION 3
    task1 >> [task2,task3]