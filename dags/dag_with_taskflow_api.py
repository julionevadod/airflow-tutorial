from airflow.decorators import dag, task
from datetime import datetime, timedelta

# USING TASKFLOW REDUCES HUGELY LINES OF CODE
default_args = {
    "owner": "julionevadod",
    "retries": 5,
    "retry_delay": timedelta(minutes=5)
}

@dag(
        dag_id="dag_with_taskflow_api_v02",
        default_args=default_args,
        start_date=datetime(2024,4,20),
        schedule_interval="@daily"
)
def helo_world_etl():
    
    # Example 1: Returning SINGLE parameter
    # @task()
    # def get_name():
    #     return "Jerry"

    # Example 2: Returning MULTIPLE parameters
    @task(multiple_outputs=True)
    def get_name():
        return {
            "first_name": "Jerry",
            "last_name": "Fridman"
        }
    
    @task()
    def get_age():
        return 24
    
    @task()
    def greet(first_name, last_name,age):
        print(f"Hello world! My name is {first_name} {last_name} and I am {age} years old!")

    name_dict = get_name()
    age = get_age()
    greet(first_name=name_dict["first_name"], last_name=name_dict["last_name"], age=age)

greet_dag = helo_world_etl()