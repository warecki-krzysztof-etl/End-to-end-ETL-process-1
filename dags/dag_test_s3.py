from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from pipeline import ETL_Process
from datetime import datetime
from airflow import DAG

def task_to_extract_data(ti):
    print("Starting...")
    etl = ETL_Process()
    raw_path = etl.extract_and_save()

    ti.xcom_push(key = 'raw_json_path', value = raw_path)

def task_transformation(ti):
    print("Transformation starting...")
    raw_path = ti.xcom_pull(task_ids = 'extract_data', key = 'raw_json_path')

    etl = ETL_Process()

    clean_path = etl.transform_and_save_parquet(raw_path)

    ti.xcom_push(key = 'clean_parquet_path', value = clean_path)

def task_load_data(ti):
    print("Start loading to database...")

    clean_path = ti.xcom_pull(key = 'clean_parquet_path', task_ids = 'transform_data')

    etl = ETL_Process()

    etl.load_to_postgres(clean_path)

default_args = {
    'owner' : 'Warecki Krzysztof',
    'start_date' : datetime(2026,7,31),
}

with DAG(
    'Project_Alpha_Test_Dag',
    default_args = default_args,
    schedule_interval = '@daily',
    catchup = False,

)as dag:
    extract_task = PythonOperator(
        task_id = 'exctract_data',
        python_callable = task_load_data,
    )
    backup_to_s3 = LocalFilesystemToS3Operator(
        task_id = 'backup_to_s3',
        filename = "{{ ti.xcom_pull(task_ids = 'extract_data', key = 'raw_json_path')}}",
        dest_key = 'warecki-project-alpha',
        aws_conn_id = 'project-alpha-aws-conn',
        replace = True
    )
    transform_task = PythonOperator(
        task_id = 'transform_data',
        python_callable = task_transformation,
    )
    load_postgres_task = PythonOperator(
        task_id = 'load_to_database',
        python_callable = task_load_data
    )

    extract_task >> [backup_to_s3, transform_task] 
    transform_task >> load_postgres_task