"""
@author: Joseph A.
Description: This script defines the ETL process for the TMDB API and Netflix data.
"""
import sys
import os
from datetime import datetime, timedelta

# Add dags folder to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from netflix.extractors import extract_netflix_data
from netflix.loaders import load_to_postgres, load_to_mongo
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

# DAG Arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 29),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG Definition
dag = DAG(
    'etl_tmdb_netflix',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
)

# Tasks
extract_task = PythonOperator(
    task_id='extract_netflix_data',
    python_callable=extract_netflix_data,
    execution_timeout=timedelta(minutes=10),
    dag=dag
)

load_postgres_task = PythonOperator(
    task_id='load_to_postgres',
    python_callable=load_to_postgres,
    execution_timeout=timedelta(minutes=5),
    dag=dag
)

load_mongo_task = PythonOperator(
    task_id='load_to_mongo',
    python_callable=load_to_mongo,
    execution_timeout=timedelta(minutes=5),
    dag=dag
)

# Task Dependencies
extract_task >> [load_postgres_task, load_mongo_task]
