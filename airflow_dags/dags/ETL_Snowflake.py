from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from subprocess import run

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
extract_snowflake_script=Variable.get("extract_snowflake_script")
load_snowflake_script=Variable.get("load_snowflake_script")
python_command="python"

# DAG configuration
dag = DAG('elt_snowflake_dag', 
          default_args=default_dag_args, 
          schedule=None
)

# Function with python extract script to run
def run_extract_snowflake_script():
    run([python_command, 
         extract_snowflake_script])

# Function with python load script to run
def run_load_snowflake_script():
    run([python_command, 
         load_snowflake_script])

# Extraction task
extract_snowflake_task = PythonOperator(
    task_id='run_extract_snowflake_script',
    python_callable=run_extract_snowflake_script,
    dag=dag,
)

# Load task
load_snowflake_task = PythonOperator(
    task_id='run_load_script',
    python_callable=run_load_snowflake_script,
    dag=dag,
)

# Task order execution
extract_snowflake_task >> load_snowflake_task
