from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from pipeline import ETL_Process
from datetime import datetime
from airflow import DAG
import logging

def critise_alarm(context):
    faulty_test = context.get('task_instance').task_id
    reason = context.get('exception')
    message = f"[CRITISE ALARM!] Task {faulty_test} was faulty! Reason: {reason}"
    logging.error(message)
    try:
        with open('/tmp/alarm.txt','a') as file:
            file.write(message)
    except Exception as e:
        logging.error(f"No alarm file found! : {e}")

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
    'on_failure_callback' : critise_alarm,
}

with DAG(
    'Project_Alpha_Test_Dag_S3',
    default_args = default_args,
    schedule_interval = '@daily',
    catchup = False,

)as dag:
    extract_task = PythonOperator(
        task_id = 'extract_data',
        python_callable = task_to_extract_data,
    )
    backup_to_s3 = LocalFilesystemToS3Operator(
        task_id = 'backup_to_s3',
        filename = "{{ ti.xcom_pull(task_ids = 'extract_data', key = 'raw_json_path')}}",
        dest_bucket = 'warecki-project-alpha',
        dest_key = 'bronze_layer/raw_data.json',
        aws_conn_id = 'project_alpha_aws_conn',
        replace = True
    )
    transform_task = PythonOperator(
        task_id = 'transform_data',
        python_callable = task_transformation,
    )
    data_quality_gate = BashOperator(
        task_id = 'data_quality_gate',
        bash_command = 'python -m pytest /opt/airflow/dags/test_data_quality.py'
    )
    dbt_launcher = BashOperator(
        task_id = 'dbt_launcher',
        bash_command = 'python -m venv /tmp/dbt_venv && source /tmp/dbt_venv/bin/activate && pip install dbt-postgres && cd /opt/airflow/dags/project_alpha_dbt && dbt run --profiles-dir .'
    )
    dbt_tester = BashOperator(
        task_id = 'dbt_tester',
        bash_command = 'source /tmp/dbt_venv/bin/activate && cd /opt/airflow/dags/project_alpha_dbt && dbt test --profiles-dir .'
    )
    load_postgres_task = PythonOperator(
        task_id = 'load_to_database',
        python_callable = task_load_data
    )

    extract_task >> [backup_to_s3, transform_task]
    transform_task >> data_quality_gate >> load_postgres_task >> dbt_launcher >> dbt_tester

