# **DHMI Monthly Data Scraper**
---
## Table of Contents
1. [DHMI Monthly Data Scraper](#project-overview)
    1. [File Structure](#file-structure)
    2. [Setup, Installation and Usage](#setup-and-installation)
    3. [License](#license)
    4. [Improvements](#improvements)
---
## **Introduction**
This project automates the process of scraping monthly data from the DHMI (State Airports Authority) website. It downloads Excel files containing monthly statistics, processes the data, and stores it in a PostgreSQL database. The script checks for new monthly data and updates the database accordingly.

## **Project Overview**
- Features:
    1. Uses `requests` and `BeautifulSoup` to scrape and parse the DHMI statistics [page](https://www.dhmi.gov.tr/Sayfalar/Istatistikler.aspx).
    2. Downloads Excel files, reads and processes the data using `pandas`.
    3. Uses `SQLAlchemy` for database interactions, saving processed data into a `PostgreSQL` database.
    4. Handles SSL warnings for secure HTTPS connections.
    5. Automates the data-checking process and updates the database when **new data is available**.
    6. Uses `Docker` for a consistent development environment, making it easy to run the PostgreSQL database and other dependencies.
---
## File Structure
```shell
monthly-scrape/
├── build_files/
│   ├── clean_format.py
|   └── ... 
├── migrations/ # Contains Alembic files for managing database migrations.
|   └── .env # Stores environment variables for the project.
|   └── ... 
├── .gitignore
├── LICENSE
├── README.md
├── alembic.ini # Configuration file for Alembic.
├── docker-compose.yaml # Configuration for Docker Compose.
├── main-scraper-db.py # Main script for scraping and processing data.
├── models.py # Defines the SQLAlchemy models for database tables.
├── requirements.txt # Lists Python package dependencies.
 ```
---
## Setup and Installation
1. **Clone the Repo**
```bash
git clone https://github.com/melisacar/monthly-scrape.git
cd monthly-scrape
```
**Prerequisites**
- Docker & Docker Compose
- Python 3.6+
- PostgreSQL database

2. Start Services Using Docker Compose:
- Start the database service defined in the `docker-compose.yaml` file.
```bash
docker-compose up -d
```
This project is Dockerized for easy deployment. 

 - This command reads the `docker-compose.yaml` file, pulls the necessary image, creates the PostgreSQL container, and mounts the volume for data persistence.
 - `-d` starts the services in the background

3. Prepare the database:
- Ensure that PostgreSQL is running in the Docker container. The database will be created automatically using the settings defined in the `docker-compose.yaml` file.
- You do not need to manually create a database named `dhmi-scrape` as it is handled by the Docker setup.

4. Install required Python packages:
```shell
pip3 install -r requirements.txt
```
5. Environment Variables:
The `.env`(inside the `migrations/`) file is used to configure environment variables required by the project:
```bash
DATABASE_URL: PostgreSQL connection string.
```
Ensure that your `.env` file is correctly set up before running the scraper or Docker commands.
---
## Usage
- To start the scraping process, run the main script:

```shell
python3 main-scraper-db.py
```
The script will check for new data, download the latest Excel file if new data is available, processes it, and save it to the database.

## SQLAlchemy Model
Defined in `models.py`:
```py
class Flight_Check(Base):
    __tablename__ = 'flight_check'
    # Columns: id, havalimani, hat_turu, num, kategori, tarih, erisim_tarihi
```
## **License**
This project is licensed under the MIT License - see the [LICENSE](https://github.com/melisacar/monthly-scrape/blob/main/LICENSE) file for details.

## Improvement

The data-checking process will be automated using `Apache Airflow`, which will run the scraping script every weekday at a specified time. This enhancement ensures that the database is consistently updated with the latest data **without manual intervention**, making the project more efficient and reliable.

# Extra Notes
- Create `docker_compose.yaml` File

Created to define the PostgreSQL database service with settings like environment variables, volumes, and ports in a single file for easy deployment.

```yaml
version: "3.9"
services:
    database:
        container_name: "postgres"
        image: "postgres"
        ports:
            - "5432:5432"
        environment:
            - "POSTGRES_PASSWORD=secret"
            - "POSTGRES_DB=dhmi-scrape"
        volumes:
            - pg-data:/var/lib/postgresql/data

volumes:
    pg-data:
```

- Error Handling

SQL IDE error message `password authentication failed for user "postgres"` while reconnecting to your database (Can have multiple reasons for that, see below for what I faced and how I fixed):

- Identify the Process Using Port number:
    - This command will **show** you the process ID (PID) that is using the port. (in my case: 141)
```bash
sudo lsof -i :5432
```
- You can then stop the process using: 
```bash
sudo kill -9 141
```
- Restart Docker services
```bash
docker compose up -d
```
- List and see running Docker containers.
 ```bash
docker ps
 ```
- Common Commands:
 - The `docker-compose stop` command will stop your containers, but it **won't remove** them. 
 - The `docker-compose down` command will stop your containers, but it also **removes** the stopped containers as well as any networks that were created. 
 - You can take down 1 step further and add the `-v` flag to **remove all volumes too**.
