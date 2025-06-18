
# 🚀 Desafio Técnico - Engenharia de Dados | Maxinutri

Este projeto tem como objetivo demonstrar habilidades em ingestão de dados, modelagem dimensional, ETL e orquestração de pipelines com Apache Airflow, conforme solicitado no desafio técnico da Maxinutri.

---

## 📌 Visão Geral

- **Fonte de Dados:** API paginada fornecida pela Maxinutri.
- **Armazenamento:** PostgreSQL.
- **Orquestração:** Apache Airflow.
- **Formato de Modelagem:** Estrela.
- **Script:** Desenvolvido em Python utilizando `pandas`, `sqlalchemy` e `requests`.

---

## ⚙️ Arquitetura da Solução

```mermaid
graph TD
    API[API Maxinutri]
    API -->|Paginação + Requests| Ingestao[Ingestão de Dados (Python)]
    Ingestao -->|Transformação| Transformacao[Transformações + Modelagem Dimensional]
    Transformacao -->|Carga| PostgreSQL[(Data Warehouse)]
    PostgreSQL --> Airflow[Airflow DAG]
````

---

## 🧠 Justificativas Técnicas

* **Python**: Linguagem flexível e poderosa para manipulação de dados e integração com APIs.
* **PostgreSQL**: Banco relacional robusto, ideal para modelagem dimensional.
* **Airflow**: Usado para orquestrar, monitorar e agendar o pipeline de forma reutilizável e escalável.
* **Modelagem Estrela**: Simplifica consultas e otimiza performance em análises OLAP.

---

## 🗂️ Estrutura do Projeto

```bash
├── dags/
│   └── etl_maxinutri_to_postgres.py
├── docker/
│   ├── docker-compose.yaml
├── README.md
```

---

## 🧱 Modelagem Dimensional

### 🔹 Fatos

**fato\_vendas**

* `order_id` (FK)
* `customer_id` (FK)
* `product_id` (FK)
* `price`
* `frete`
* `data_entrega`

**fato\_avaliacoes**

* `order_id` (FK)
* `nota_avaliacao`
* `titulo_avaliacao`
* `texto_avaliacao`
* `data_avaliacao`
* `data_resposta`

### 🔸 Dimensões

**dim\_cliente**

* `customer_id` (PK)
* `cidade`
* `estado`
* `cep_prefixo`

**dim\_produto**

* `product_id` (PK)
* `categoria`
* `fotos_qtd`
* `peso_g`
* `comprimento_cm`
* `altura_cm`
* `largura_cm`

**dim\_pedido**

* `order_id` (PK)
* `status_pedido`
* `data_compra`
* `data_aprovacao`
* `data_envio_transportadora`
* `data_entrega_cliente`
* `data_entrega_estimada`

---

## 🏗️ Setup do Projeto

### Pré-requisitos

* Docker + Docker Compose

### Subindo a stack

```bash
docker-compose up 
```

---

## ✅ Pontos de Validação

* ✅ Dados coletados da API paginada.
* ✅ Modelagem dimensional aplicada (modelo estrela).
* ✅ ETL implementado e automatizado via Airflow.
* ✅ Dados carregados no PostgreSQL com integridade referencial.
* ✅ Código limpo, modular e reutilizável.
* ✅ Logs descritivos e tratamento básico de falhas (timeout, tentativas).

---

## 💡 Melhorias Futuras

* Implementar notificações (e-mail/Slack) via Airflow em falhas.
* Persistência em CSV/Parquet como backup local.
* Indexação e particionamento no PostgreSQL para escalabilidade.
* Painel de monitoramento (ex: Grafana + Prometheus).
* Criação incremental em vez de `replace` nas tabelas.


**Obrigado pela oportunidade!**


