
# 🚗 Nova Drive Motors - ELT Data Pipeline

This project is a fictional ELT pipeline designed for the **Sales Department** of **Nova Drive Motors**, developed as part of a data engineering bootcamp.

It implements an automated, scalable ELT solution using modern open-source tools and cloud-native services.

---

## 🚀 Tech Stack

- **Apache Airflow** (with Docker) – Orchestration
- **DBT Core** – SQL-based transformation
- **Google BigQuery** – Cloud data warehouse
- **Python** – Custom scripting
- **Looker Studio** – Visualization layer
- **Google Cloud Platform (GCP)** – Hosting and compute

---

## 📁 Project Structure

```
nova_drive_elt_project/
├── dags/                # Airflow DAGs (scheduling + orchestration)
├── nova_drive_dbt/      # DBT project (models, seeds, profiles)
├── requirements.txt     # Python dependencies
└── docker-compose.yaml  # Docker setup for Airflow
```

---

## 📅 How It Works

- A daily scheduled DAG orchestrates the pipeline.
- Steps include:
  - Ingestion of sales data from PostgreSQL (remote database provided by the bootcamp instructor)
  - Loading to BigQuery tables
  - Transformation of data using DBT models

---

## 📊 Dashboard

Visual insights from BigQuery models are exposed through **Looker Studio**:  
👉 [View Dashboard](https://shorturl.at/ZoccI)

---

## 🔐 Security

- `.env` and sensitive files (like GCP key) are ignored via `.gitignore`
- DBT profile and credentials are stored **outside version control**

---

## 👤 Author

- **Revson Vieira**
- Created as part of a Data Engineering Bootcamp project

---

## 📄 License

This project is not open for public contribution once it is part of a bootcamp.

---

## 🙌 Acknowledgements

- Prof. Fernando Amaral
- dbt Labs
- Google Cloud Platform
- Apache Airflow
