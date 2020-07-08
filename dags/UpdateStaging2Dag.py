import os
import sys
from datetime import datetime
# Third Party
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook

# Make python folder a module
sys.path.append("/usr/local/airflow/dags/efs")
from redb.scripts.staging_2_functions import poulate_dead_parcels_table, copy_data

# Connect to Amazon Aurora Postgres database using Airflow
CONN = BaseHook.get_connection("redb_postgres")
BUCKET = CONN.conn_id
HOST = CONN.host
LOGIN = CONN.login
PASSWORD = CONN.password
PORT = CONN.port

default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 4, 15, 3, 00, 00),
    "concurrency": 1,
    "retries": 3
}

dag = DAG(
    "UpdateStaging2",
    default_args=default_args,
    schedule_interval='@once'
)

populate_dead_parcels_table = PythonOperator(
    task_id="populate_dead_parcels_table",
    python_callable=poulate_dead_parcels_table,
    op_kwargs={
        "database": BUCKET,
        "host": HOST,
        "username": LOGIN,
        "password": PASSWORD,
        "port": PORT
    },
    dag=dag
)

copy_data = PythonOperator(
    task_id="copy_data",
    python_callable=copy_data,
    op_kwargs={
        "database": BUCKET,
        "host": HOST,
        "username": LOGIN,
        "password": PASSWORD,
        "port": PORT
    },
    dag=dag
)

populate_dead_parcels_table >> copy_data
