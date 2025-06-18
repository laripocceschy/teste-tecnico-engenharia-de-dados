from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import psycopg2

# Função que será chamada pelo PythonOperator
def ingest_csv_to_postgres():
    # Lê o CSV
    df = pd.read_csv('/opt/airflow/dags/files/dados.csv')

    # Conecta ao Postgres
    conn = psycopg2.connect(
        dbname="warehouse",
        user="admin",
        password="admin",
        host="postgres",
        port="5432"
    )
    cursor = conn.cursor()

    # Cria a tabela (caso não exista)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            nome TEXT,
            email TEXT,
            idade INT
        );
    """)
    conn.commit()

    # Insere os dados
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO clientes (nome, email, idade) VALUES (%s, %s, %s)
        """, (row['nome'], row['email'], int(row['idade'])))

    conn.commit()
    cursor.close()
    conn.close()

# Define a DAG
with DAG(
    dag_id='INGESTION-etl_csv_to_postgres',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    default_args={'owner': 'airflow'}
) as dag:

    etl_task = PythonOperator(
        task_id='ingest_csv',
        python_callable=ingest_csv_to_postgres
    )

    etl_task
