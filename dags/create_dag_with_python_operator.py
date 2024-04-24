from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "julionevadod",
    "retries": 5,
    "retry_delay": timedelta(minutes=5)
}

# Example 1: Passing values to python func
# def greet(name, age):
#     print(f"Hello World! My name is {name} and I am {age} yeasrs old.")

# Example 2: Ingesting name from xcomms
# def greet(age, ti): #ti -> task instance
#     name = ti.xcom_pull(task_ids="get_name") # We create variable name from the returned value from task with id "get_name"
#     print(f"Hello World! My name is {name} and I am {age} yeasrs old.")

# Example 3: Pulling MULTIPLE variables
# def greet(age, ti): #ti -> task instance
#     first_name = ti.xcom_pull(task_ids="get_name", key="first_name")
#     last_name = ti.xcom_pull(task_ids="get_name",key="last_name")
#     print(f"Hello World! My name is {first_name} {last_name} and I am {age} yeasrs old.")

# Example 3: Pulling MULTIPLE variables
def greet(ti): #ti -> task instance
    first_name = ti.xcom_pull(task_ids="get_name", key="first_name") # MAX SIZE OF XCOMS is 48 KB. Do NOT use for large data, otherwise it will crash!
    last_name = ti.xcom_pull(task_ids="get_name",key="last_name")
    age = ti.xcom_pull(task_ids="get_age",key="age")
    print(f"Hello World! My name is {first_name} {last_name} and I am {age} yeasrs old.")

# Example 2: Returning ONLY one variable
# def get_name():
#     return "Jerry"

# Example 3: Pushing MULTIPLE variables
def get_name(ti):
    ti.xcom_push(key="first_name",value="Jerry")
    ti.xcom_push(key="last_name",value="Fridman")

def get_age(ti):
    ti.xcom_push(key="age", value = 24)


with DAG(
    default_args=default_args,
    dag_id="our_dag_with_python_operator_v06",
    description="Our first dag using python operator",
    start_date=datetime(2024,4,20,3),
    schedule_interval="@daily"
) as dag:
    
    # Example 1: Passing values to python func
    # task1 = PythonOperator(
    #     task_id="greet",
    #     python_callable=greet,
    #     op_kwargs = {"name":"Julio","age":24} # With op_kwargs we can pass all kind of parameters defined in our python_callable function
    # )

    # Example 2: Ingesting name from xcomms
    # task1 = PythonOperator(
    #     task_id="greet",
    #     python_callable=greet,
    #     op_kwargs = {"age":24} # With op_kwargs we can pass all kind of parameters defined in our python_callable function
    # )

    # Example 3: Ingesting name and age from xcomms
    task1 = PythonOperator(
        task_id="greet",
        python_callable=greet,
    )


    task2 = PythonOperator(
        task_id="get_name",
        python_callable=get_name # In this case, in xcomms we can see the returned value was Jerry
    )

    task3 = PythonOperator(
        task_id="get_age",
        python_callable=get_age
    )

    [task2, task3] >> task1