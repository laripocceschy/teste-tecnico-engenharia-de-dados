from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

import requests
import pandas as pd
import math
from time import sleep
from sqlalchemy import create_engine

# Configurações da DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='etl_maxinutri_to_postgres',
    default_args=default_args,
    description='ETL da API Maxinutri para PostgreSQL',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['maxinutri', 'etl'],
) as dag:

    BASE_URL = "https://teste-engenheiro.onrender.com/data"
    TOKEN = "63daac8dac3d57e6c6f9f71d3a9fa4ed"
    DB_CONN = "postgresql+psycopg2://admin:admin@postgres-maxinutri:5432/maxinutri"
    engine = create_engine(DB_CONN)

    def get_data():
        all_data = []
        print("🔍 Fazendo primeira requisição para obter metadados da API...")
        response = requests.get(BASE_URL, params={"token": TOKEN, "page": 1})
        if response.status_code != 200:
            raise Exception(f"Erro ao acessar a API: {response.text}")
        js = response.json()
        total_linhas = js.get("total_linhas", 0)
        linhas_por_pagina = js.get("linhas_por_pagina", 1)
        total_paginas = math.ceil(total_linhas / linhas_por_pagina)
        print(f"📄 Total de páginas a processar: {total_paginas}")

        for page in range(1, total_paginas + 1):
            try:
                print(f"📥 Requisitando página {page}...")
                resp = requests.get(BASE_URL, params={"token": TOKEN, "page": page}, timeout=10)
                if resp.status_code != 200:
                    print(f"⚠️ Página {page}: erro {resp.status_code}, tentando novamente após 5s...")
                    sleep(5)
                    continue
                data = resp.json().get("dados", [])
                all_data.extend(data)
                sleep(1)
            except requests.exceptions.RequestException as e:
                print(f"❌ Erro na requisição da página {page}: {e}")
                continue

        df = pd.DataFrame(all_data)
        print(f"✅ Dados coletados: {df.shape[0]} registros.")
        return df

    def gerar_dimensoes_e_fatos(df: pd.DataFrame) -> dict:
        datas = [
            "order_purchase_timestamp", "order_approved_at",
            "order_delivered_carrier_date", "order_delivered_customer_date",
            "order_estimated_delivery_date", "review_creation_date",
            "review_answer_timestamp"
        ]
        for col in datas:
            df[col] = pd.to_datetime(df[col], errors='coerce')

        dim_cliente = (
            df[["customer_id", "customer_city", "customer_state", "customer_zip_code_prefix"]]
            .drop_duplicates()
            .rename(columns={
                "customer_city": "cidade",
                "customer_state": "estado",
                "customer_zip_code_prefix": "cep_prefixo"
            })
        )

        dim_produto = (
            df[["product_id", "product_category_name", "product_photos_qty",
                 "product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]]
            .drop_duplicates()
            .rename(columns={
                "product_category_name": "categoria",
                "product_photos_qty": "fotos_qtd",
                "product_weight_g": "peso_g",
                "product_length_cm": "comprimento_cm",
                "product_height_cm": "altura_cm",
                "product_width_cm": "largura_cm"
            })
        )

        dim_pedido = (
            df[["order_id", "order_status", "order_purchase_timestamp",
                 "order_approved_at", "order_delivered_carrier_date",
                 "order_delivered_customer_date", "order_estimated_delivery_date"]]
            .drop_duplicates()
            .rename(columns={
                "order_status": "status_pedido",
                "order_purchase_timestamp": "data_compra",
                "order_approved_at": "data_aprovacao",
                "order_delivered_carrier_date": "data_envio_transportadora",
                "order_delivered_customer_date": "data_entrega_cliente",
                "order_estimated_delivery_date": "data_entrega_estimada"
            })
        )

        fato_vendas = (
            df[["order_id", "customer_id", "product_id", "price", "freight_value", "order_delivered_customer_date"]]
            .rename(columns={
                "freight_value": "frete",
                "order_delivered_customer_date": "data_entrega"
            })
        )

        fato_avaliacoes = (
            df[["order_id", "review_score", "review_comment_title", "review_comment_message",
                 "review_creation_date", "review_answer_timestamp"]]
            .dropna(subset=["review_score"])
            .rename(columns={
                "review_score": "nota_avaliacao",
                "review_comment_title": "titulo_avaliacao",
                "review_comment_message": "texto_avaliacao",
                "review_creation_date": "data_avaliacao",
                "review_answer_timestamp": "data_resposta"
            })
        )

        return {
            "dim_cliente": dim_cliente,
            "dim_produto": dim_produto,
            "dim_pedido": dim_pedido,
            "fato_vendas": fato_vendas,
            "fato_avaliacoes": fato_avaliacoes
        }

    def etl_to_postgres():
        print("🚀 Iniciando ETL...")
        df = get_data()
        tabelas = gerar_dimensoes_e_fatos(df)
        for nome, tabela in tabelas.items():
            print(f"📝 Gravando {nome} no PostgreSQL...")
            tabela.to_sql(nome, con=engine, if_exists='replace', index=False)
        print("🏁 ETL concluído com sucesso.")

    run_etl = PythonOperator(
        task_id='executar_etl_maxinutri',
        python_callable=etl_to_postgres
    )

    run_etl
