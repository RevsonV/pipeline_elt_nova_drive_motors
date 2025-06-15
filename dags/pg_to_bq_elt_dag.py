from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
import pandas as pd
from pandas_gbq import to_gbq
import logging

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

def get_bq_max_id(project, dataset, table, **kwargs):
    bq_hook = BigQueryHook(gcp_conn_id='google_cloud_default', use_legacy_sql=False)
    sql_query = f"SELECT MAX(id_{table}) AS max_id FROM {project}.{dataset}.{table}"
    try:
        result = bq_hook.get_pandas_df(sql_query)
        max_id = result['max_id'][0]
        logging.info(f"[{table}] Last id is: {max_id}")
        return max_id if max_id is not None else 0
    except Exception as e:
        logging.info(f"[{table}] Exception raised: {e}")
        return 0

def load_pg_to_bq(project, dataset, table, ti, **kwargs):
    max_id = ti.xcom_pull(task_ids=f'{table}.get_max_id')
    with PostgresHook(postgres_conn_id='postgres_default').get_conn() as pg_conn:
        with pg_conn.cursor() as pg_cursor:
            pg_cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
            columns = [row[0] for row in pg_cursor.fetchall()]
            columns_list_str = ', '.join(columns)
            primary_key = f'id_{table}'
            pg_cursor.execute(f"SELECT {columns_list_str} FROM {table} WHERE {primary_key} > {max_id}")
            rows = pg_cursor.fetchall()
            try:
                df = pd.DataFrame(rows, columns=columns)
                to_gbq(
                    dataframe=df,
                    destination_table=f'{dataset}.{table}',
                    project_id=project,
                    if_exists='append'
                )
                logging.info(f"[{table}] {len(df)} rows inserted into BigQuery.")
            except Exception as e:
                logging.info(f"[{table}] Error loading to BigQuery: {e}")

with DAG(
    dag_id='postgres_to_bigquery_all_tables_grouped',
    default_args=default_args,
    description='Incremental loading of tables from Postgres to BigQuery by TaskGroups',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['elt', 'bq', 'taskgroup']
) as dag:

    bq_project = 'dark-forge-453419-d7'
    raw_dataset = 'raw'
    tables_list = ['veiculos', 'estados', 'cidades', 'concessionarias', 'vendedores', 'clientes', 'vendas']

    last_load_tasks = []

    for table in tables_list:
        with TaskGroup(group_id=table) as tg:
            get_max_id = PythonOperator(
                task_id='get_max_id',
                python_callable=get_bq_max_id,
                op_args=[bq_project, raw_dataset, table]
            )

            load_data = PythonOperator(
                task_id='load_incremental',
                python_callable=load_pg_to_bq,
                op_args=[bq_project, raw_dataset, table]
            )

            get_max_id >> load_data
            last_load_tasks.append(load_data)
    
    run_dbt = BashOperator(
        task_id='run_dbt',
        bash_command='cd /opt/airflow/dbt/nova_drive_dbt && /home/airflow/.local/bin/dbt run --target prod',
        env={
            'DBT_PROFILES_DIR': '/opt/airflow/dbt/nova_drive_dbt',
            'GOOGLE_APPLICATION_CREDENTIALS': '/opt/airflow/config/credentials.json'
        }
    )

    last_load_tasks >> run_dbt
