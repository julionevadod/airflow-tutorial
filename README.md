Airflow basic tutorial based on [coder2j video](https://youtu.be/K9AnJ9_ZAXE?si=gdp_y40ZhFTP-j5l).
# 1. Installation
## 1.1 Local Installation
 ``` bash
 pip install 'apache-airflow==2.9.0' \
 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.0/constraints-3.8.txt"
 ```

Bear in mind airflow you might be interested in other version/constraints version. Worth to check [official repository installation section](https://github.com/apache/airflow?tab=readme-ov-file#installing-from-pypi)

Set environment variable **AIRFLOW_HOME**. This will define the folder where airflow porject files will be created. If not set, airflow will create project files inside current directory.

### Useful commands
Initialise a SQLite DB.
``` bash
 airflow db init
 ```

Initialize airflow web server.
 ```bash
 airflow webserver -p PORT_TO_USE 
```

Create a user to login to airflow web server.
```bash
airflow users create --username USERNAME --firstname FIRST_NAME --lastname LAST_NAME --email EMAIL
```
After previous command, you will be prompted to create a password.

Start airflow scheduler.
```bash
airflow scheduler
```


## 1.2 Docker Installation
First, we need to fetch docker compose file [as show here](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).
```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.0/docker-compose.yaml'
```

Next, we should create project folders:
```bash
mkdir -p ./dags ./logs ./plugins ./config
```

If we are using Linux, we should also run:
```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
To start airflow web server, scheduler and db, use docker-compose command. This will download all necessary files and will create an admin user with airflow as username and password:
```bash
docker-compose up airflow-init
```

We can finally run airflow:
```bash
docker-compose up -d
```

# 2. Airflow concepts
## 2.1 Airflow components
Main component in airflow are workflows. Workflows are sequences of tasks defined by a DAG (Directed Acyclic Graph). A DAG allows us to organise tasks in a specific order reflecting task dependency. This has the huge benefit of enabling parallel execution of tasks (task dependencies are known so independent tasks can run in parallel) and fault tolerance (a failing task does not affect other task if they are independent).

The other two **main** components in airflow are:
- Tasks: A node in a DAG. Tasks are written in Python. Task allow us to achieve some specific goals by means of operators
- Operators: Define **WHAT** gets done. Some useful operators are BashOperator or PythonOperator. We can even define our custom operators.

Workflows are characterised by:
- Execution Date: Logical date & time in which a DAG ran.
- Task Instance: A specific run of a task at a very specific run.
- Dag Run: Instantiation of a DAG. It contains task instances that run for a execution date.

## 2.2 Task Lifecycle
Tasks in airflow can undergo 11 different states:
- no_status: Initial state. From this state, a task can move to:
    - scheduled: common workflow here is queued -> running -> success
    - queued
    - upstream_failed
    - skipped
- scheduled: scheduler plans the task to be run
- queued
- running: can go into:
    - success
    - failed: if max retires not exceeded, it will go up_for_retry, where it will be scheduled after some time
    - shutdown: if max retires not exceeded, it will go up_for_retry, where it will be scheduled after some time
    - up_for_reschedule -> schedule
- success
- upstream_failed
- up_for_schedule
- skipped: a task is manually skipped
- up_for_retry
- failed
- shutdown: a task is manually aborted

## 2.3 XCOMMS
Xcomms can be used to extract and feed runtime variables to tasks. For instance, we can use xcomms to feed return value of task 1 into input values of task 2. For a detailed usage of this, look **dags/create_dag_with_python_operator.py**

## 2.4 Backfill
One of the arguments that define a DAG is start_date. start_date can be a past date. In these cases, when backfill is enabled (it is by default), past runs until current date are automatically run. In other words, if today, we set a dag with start_date one year ago with a daily trigger, dag will run 365 times.

If backfill is set to false, no past runs will be executed. 

Backfill can also be done manually. We need to log into airflow scheduler and run:
```bash
airflow backfill -s START_DATE -e END_DATE DAG_NAME
```

## 2.5 Scheduling
Airflow DAGs can be scheduled to run periodically. This behaviour can be defined by schedule_interval. Bear in mind this schedule_interval breaks time into windows and airflow run DAGs at the END of each window.

Scheduling can be done using:
1. datetime.timedelta
2. Using CRON expressions

Airflow already provide some presets:
- None: only for manually triggered DAGs.
- @once: DAG is run once and only once (that unique run depends on start_date)
- @hourly: DAG is run every hour. Logical run of hour X will run at hour X+1:00
- @daily: DAG is run every day at midnight.
- @weekly: DAG is run every week, at sunday midnighgt.
- @monthly: DAG is run every month at midnight of first day.
- @yearly: DAG is run every year at midnight of Jan 1.

However, custom cron expressions can be built. This [webpage](https://crontab.guru/) can be useful for this purpose. 

# 3, Airflow PostgreSQL connection
In airflow web UI, we need to go admin > connections. There we can set up a connection with a PostgreSQL DB. We will need to set: 
- connId: Will be needed for PostgresOperator.
- schema/database: Name of the database to connect to.
- user
- password
- port
- host. This can be:
    - as defined in dockerfile
    - localhost
    - host.docker.internal

Appart from PostgreSQL, we can create connections to other servces like cloud servers. If required type is missingwe can install additional packages from several providers.

# 4. Installing python dependencies to airflow docker container
To install additional dependencies, two options are available:
1. Image extending:
    - Quick and easy solution.
    - It does not need airflow sources.
    - How? First, we need to create a dockerfile where additional dependencies from a requirements.txt file are installed. Then, we need to point this new image in our docker-compose.yml file.
2. Image customization:
    - Produces a size-optimized image
    - Built from custom airflow sources
    - Can be built on isolated systems (from internet)
    - How?
        - Clone airflow official repository
        - Create requirements.txt file with dependencies inside docker-content-file folder
        - Build docker image