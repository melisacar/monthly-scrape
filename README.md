# DHMI Monthly Data Pipeline

- A data pipeline to **automate** the **scraping and transformation** of monthly airport traffic data from the DHMI (State Airports Authority) website. This project uses **Apache Airflow** to **schedule** the pipeline, fetches data with `requests` and `BeautifulSoup`, and stores transformed data in a PostgreSQL database.
---
## Table of Contents

- Overview
- Project Structure
- Setup
- Data Pipeline Flow
- Database Integration
- License

## Overview
This project automates the following tasks:

- **Scraping:** Collects the latest Excel files of airport traffic data from DHMI's website.
- **Data Transformation:** Transforms the Excel file into a structured format with columns for airport name, domestic/international flights, category, and date.
- **Database Storage:** Stores processed data into a PostgreSQL database for analysis and reporting.


## Project Structure
The main components of this project are organized into directories and files as follows:
```bash
├── dags
│   └── data_pipeline_dag.py    # Defines the DAG for Apache Airflow to schedule and run the data pipeline
├── src
│   ├── main_scraper.py         # Contains main scraping and data transformation logic
│   ├── models.py               # Defines the database schema and connects to PostgreSQL
│   ├── migrations/             # Contains migration files for schema management (optional)
│   └── alembic.ini             # Configuration for Alembic migrations
|   └── config.py       
├── .gitignore
├── Dockerfile                  # Docker configuration for running the app
├── README.md                   # Project documentation
├── docker-compose.yaml         # Docker Compose setup for Airflow, PostgreSQL, and the app
└── requirements.txt            # Python dependencies
```

## Setup
This project uses Docker to simplify the setup process, ensuring all dependencies and services are easily configured and reproducible. Make sure Docker and Docker Compose are installed on your machine.

1. Clone the Repository
```bash
git clone https://github.com/melisacar/monthly-scrape.git
cd monthly-scrape 
```

2. Build the Docker Containers
The docker-compose.yaml file configures the containers for:

- Apache Airflow (DAG scheduler)
- PostgreSQL (database)
- A custom container to run the scraping script

To build and start the containers:
```shell
docker compose up airflow-init
```
If you have stop running containers and then:
```shell
docker-compose up -d --build
```
4. Access Airflow UI
Once Airflow is running, access the Airflow web interface at `http://localhost:8080` or `http://127.0.0.1:8080/`. Use the default login (airflow / airflow) to view and manage DAGs.


## Data Pipeline Flow
### **DAG:** `data_pipeline_dag.py`:
- The `data_pipeline_dag.py` defines the Airflow DAG that schedules and runs the main data processing steps.
- **Schedule Interval:** Runs daily at 10:00 AM.
- **Task:** Runs run_main_check, which initiates the scraping and processing of the monthly data.

### Script: `main_scraper.py`
`main_scraper.py` contains the main functions for scraping, processing, and saving data to the PostgreSQL database:

- `fetch_page_content(url)`: Retrieves the HTML content from DHMI's website.
- `parse_excel_links(html_content)`: Finds and returns the most recent Excel file link.
- `download_excel_file(href)`: Downloads the Excel file and returns its content.
- `transform_excel_file(excel_content)`: Processes the Excel data and reformats it into the desired structure.
- `save_to_database(df, session)`: Saves the processed data to the database.

## Database Integration
### Database Schema: 
The database schema, defined in `models.py`, specifies the structure of the flight_check table, which includes columns for airport name, flight type, number of flights, category, and date.

### Connecting to PostgreSQL
The database connection string in `config.py` connects to the `dhmi-scrape` database. The Docker setup in docker-compose.yaml exposes this database to the Airflow DAGs and the scraping script.

### Storing Processed Data
The `save_to_database` function commits new rows to the database. Each entry includes the airport name, type of flight (domestic/international), the number of flights, category, date and data retrieval date.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/melisacar/monthly-scrape/blob/main/LICENSE) file for details.