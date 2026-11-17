# Project Alpha: Data Engineering Pipeline

> **"Hello, I am a hard-working student with a strong desire to become a solid Data Engineer. Studying how data works, understanding various data processes, and constructing complex data pipelines are my main objectives as an AGH Medical Computer Science student."**

## About the Project

**Project Alpha** is a complete data pipeline project built for local practice. It uses modern data tools to download data from an API, save a backup in the cloud, transform the data using Python (Pandas), check for errors, and build final analytical tables using **dbt** and **PostgreSQL**.

## Tools & Technologies

* **Orchestration**: Apache Airflow 2.9.1 (running on Docker).

* **Data Processing**: Python, Pandas, PyArrow.

* **Cloud Storage**: AWS S3 (saving raw JSON data as a backup).

* **Database**: PostgreSQL 13 (storing clean data and dbt models).

* **Transformation**: dbt-postgres with a separate virtual environment inside Airflow to keep things fast and clean.

* **Testing**: `pytest` for data quality checks.

## How the `Project_Alpha_Test_Dag_S3` Pipeline Works 

The pipeline runs step-by-step:

1. **`extract_data`**: Downloads raw JSON data from an online API and saves it locally.

2. **`backup_to_s3`**: Uploads the raw JSON file to an AWS S3 bucket (`s3://warecki-project-alpha/bronze_layer/raw_data.json`).

3. **`transform_data`**: Cleans the data using Pandas (changes column names, calculates prices in PLN, removes unwanted categories) and saves it as a Parquet file.

4. **`data_quality_gate`**: Runs tests with `pytest` to make sure the data is correct.

5. **`load_to_database`**: Saves the clean data into the PostgreSQL database as the `produkty` table.

6. **`dbt_launcher`**: Creates a virtual environment, runs `dbt seed` (to load small CSV reference tables like `category_dict` and `workers`), and runs `dbt run` to build final reports and SQL models.

7. **`dbt_tester`**: Runs automatic dbt tests to check the data quality in the database.

## Project Structure

```
Project Alpha/
├── dags/
│   ├── project_alpha_dag.py        # Main Airflow DAG workflow
│   ├── pipeline.py                 # Python ETL logic (Extract, Transform, Load)
│   ├── test_data_quality.py        # Pytest quality checks
│   └── project_alpha_dbt/          # dbt project folder
│       ├── models/                 # SQL models (reports and transformations)
│       ├── seeds/                  # CSV files (category_dict.csv, workers.csv)
│       ├── macros/                 # Custom SQL code (e.g., discount calculation)
│       ├── dbt_project.yml         # dbt settings
│       └── profiles.yml            # Database connection settings
├── docker-compose.yaml             # Airflow setup for Docker
├── README.md                       # Project documentation
└── logger.log                      # Log files
```

## How to Run This Project

### 1. Requirements

* Docker and Docker Compose.

* Python 3.10+

* An AWS account with an S3 bucket.

### 2. Start Airflow

Open your terminal in the project folder and run:

```
docker compose down
docker compose up -d
```

### 3. Access the Airflow UI

1. Open your browser and go to: `http://localhost:8085`
2. Log in using the default development credentials:
   - **Username:** `airflow`
   - **Password:** `dataenv2026`

### 4. Configure AWS Connection

Before running the DAG, you need to provide Airflow with your AWS credentials to enable the S3 backup task:
1. In the Airflow UI, go to **Admin** -> **Connections**.
2. Click the **+** (Add a new record) button.
3. Fill in the form:
   - **Connection Id:** `project-alpha-aws-conn`
   - **Connection Type:** `Amazon Web Services`
   - **AWS Access Key ID:** *(your-access-key)*
   - **AWS Secret Access Key:** *(your-secret-key)*
4. Click **Save**.

### 5. Trigger the Pipeline

1. Go back to the **DAGs** page.
2. Search for `Project_Alpha_Test_Dag_S3`.
3. Unpause the DAG by clicking the toggle button on the left.
4. Click the **Play** button (Trigger DAG) on the right side to start the pipeline.
5. Click on the DAG name and go to the **Graph** or **Grid** view to watch the tasks succeed in real-time!

### 6. Stop the Environment

When you are done, you can stop the containers and clean up the resources by running:

```bash
docker compose down -v
```
## 👤 Author

**Krzysztof Warecki**

* AGH University of Krakow — Medical Computer Science Student

* Looking for a Data Engineering Internship in Krakow (or remote).
