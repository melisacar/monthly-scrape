import sys
from pathlib import Path

# Adding the `src` folder to Python path so our imports work smoothly – all for you!
src_path = Path(__file__).resolve().parent.parent / 'src'
sys.path.append(str(src_path))

# Importing the main function for scraping – yep, that code you wrote, Melom!
from main_scraper import run_main_check

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'data_pipeline_dag',
    default_args=default_args,
    description='A DAG to run data processing script',
    schedule_interval='0 10 * * *',  # Runs every day at 10:00 AM
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # let’s hope it’s in a good mood today
    run_data_processing = PythonOperator(
        task_id='run_main_check',
        python_callable=run_main_check,
    )