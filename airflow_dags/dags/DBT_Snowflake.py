from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# DAG arguments
default_dag_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 11, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Variables
dbt_snowflake_path = Variable.get("dbt_snowflake_path")
dbt_snapshot_command = "dbt snapshot"
dbt_seed_command = "dbt seed"
dbt_run_command = "dbt run"

# DAG configuration
dag = DAG('dbt_snowflake_dag', 
          default_args=default_dag_args, 
          schedule_interval=None
)

# DBT snapshot task
dbt_snowflake_snapshot = BashOperator(
    task_id='dbt_snapshot',
    bash_command=f'cd {dbt_snowflake_path} && {dbt_snapshot_command}',
    dag=dag,
)

# DBT seed task
dbt_snowflake_seed = BashOperator(
    task_id='dbt_seed',
    bash_command=f'cd {dbt_snowflake_path} && {dbt_seed_command}',
    dag=dag,
)

# DBT run task
dbt_snowflake_run = BashOperator(
    task_id='dbt_run',
    bash_command=f'cd {dbt_snowflake_path} && {dbt_run_command}',
    dag=dag,
)

# Task order execution
dbt_snowflake_seed >> dbt_snowflake_snapshot >> dbt_snowflake_run
