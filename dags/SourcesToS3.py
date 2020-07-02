# Standard Library
import os
import sys
import json
import datetime as dt

# Third Party
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook

# Custom
sys.path.append("/usr/local/airflow/dags/efs")
from redb.scripts.transfer_to_s3 import main

CONN = BaseHook.get_connection('redb-test')
BUCKET = CONN.conn_id
AWS_ACCESS_KEY_ID = json.loads(CONN.extra)['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = json.loads(CONN.extra)['aws_secret_access_key']

default_args = {
    'owner': 'redb',
    'start_date': dt.datetime.now(),
    'concurrency': 1,
    'retries': 0,
    'catchup': False
}

with DAG('SourcesToS3',
         default_args=default_args,
         schedule_interval='@once',
         ) as dag:
    transfer = PythonOperator(task_id='Transfer',
                               python_callable=main,
                               op_kwargs={'bucket': BUCKET,
                                        'aws_access_key_id': AWS_ACCESS_KEY_ID,
                                        'aws_secret_access_key': AWS_SECRET_ACCESS_KEY})
transfer
