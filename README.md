# Automated Data Management for DHMI Flight Information
## Introduction
- This project encompasses two interconnected phases focusing on the automated retrieval and storage of monthly flight data from the DHMI (State Airports Authority) website. In Part 1, the project simplifies the process of collecting, transforming, and consolidating this data into an Excel file. Building upon this foundation, Part 2 implements a systematic approach to storing the data in a PostgreSQL database using Docker and SQLAlchemy, with automation managed through Airflow. This ensures that the data is not only organized but also readily available for ongoing analysis.

## Table of Contents
1. [Part 1](#part-1-scraping-monthly-flight-data-from-dhmi)
    1. File Descriptions
        - [main_scraper.py](#data-scraper-for-dhmi-statistics-page) 
        - [main_month_checker.py](#monthly-data-checker)
        - [main_schedule.py](#monthly-data-scheduler)
        - [main_mc_schedule.py](#monthly-data-checker-schedule)
    2. [Requirements](#requirements)
    3. [File Structure](#file-structure)
    4. [License](#license)
    5. [Improvements](#improvements)
2. [Part 2](#part-2-automated-postgresql-storage-for-dhmi-data-using-airflow)

# **Part 1: Scraping Monthly Flight Data from DHMI**
- **Description:** Part 1 project facilitates the retrieval and processing of monthly data from the DHMI (State Airports Authority) website. It consists of multiple scripts to scrape data, transform it, and save it into a consolidated Excel file. The project runs on a predefined schedule to ensure that data is regularly updated and accessible for analysis.

## **File Descriptions**
### **Data Scraper for DHMI Statistics Page**
-  **Description:** The main.py script aims to scrape data from the DHMI (State Airports Authority) website, download Excel files, and process the extracted data. It focuses on extracting relevant information such as airport names and corresponding traffic data (domestic, international, and total). The processed data is then structured into a standardized format to facilitate further analysis and reporting.

- The [main_scraper.py](https://github.com/melisacar/monthly-scrape/blob/main/main_scraper.py) script performs the following tasks:
    - Disables SSL warnings to allow connections to HTTPS sites without certificate verification.
    - Fetches the content of the DHMI statistics page.
    - Parses the HTML to extract links to Excel files.
    - Downloads and processes each Excel file, transforming the data into a structured format.
    - Saves the combined data into a single Excel file named `DHMI_all.xlsx`.

#### **Installation**
1. Clone the Repo
```bash
git clone https://github.com/melisacar/monthly-scrape.git
cd monthly-scrape
```
2. Set up the Environment
    - Ensure you have Python installed on your machine. Then install the necessary packages using requirements.txt:
```bash
pip3 install -r requirements.txt
```
3. Run the Script
```bash
python3 main_scraper.py
```
---

### **Monthly Data Checker**
- **Description:** Manually start the process of checking for new monthly data from the DHMI (State Airports Authority) website, downloading the latest Excel files, and updating a local Excel file with the new data.

- The [main_month_checker.py](https://github.com/melisacar/monthly-scrape/blob/main/main_month_checker.py) script performs the following tasks:
    - Disable SSL Warnings: Suppresses SSL verification warnings for secure connections.
    - Fetch Page Content: Retrieves the HTML content of the specified DHMI statistics page.
    - Parse Excel Links: Identifies and extracts the link to the most recent Excel file available on the page.
    - Extract Month Number: Converts month names (e.g., "TEMMUZ SONU") to their corresponding numerical values for comparison.
    - Get Latest Month from Excel: Reads the existing DHMI_all.xlsx file to determine the latest month of data.
    - Find Newest Month in HTML: Analyzes the page content to find the most recent month available in the HTML.
    - Download Excel File: Downloads the latest Excel file if new data is detected.
    - Transform Excel File: Processes the downloaded Excel file, extracts relevant data, and formats it for consistent usage.
    - Update Local File: Merges the newly acquired data with the existing data in DHMI_all.xlsx and saves the updated file.

#### **Installation**
1. Clone the Repo
```bash
git clone https://github.com/melisacar/monthly-scrape.git
cd monthly-scrape
```
2. Set up the Environment
    - Ensure you have Python installed on your machine. Then install the necessary packages using requirements.txt:
```bash
pip3 install -r requirements.txt
```
3. Run the Script
```bash
python3 main_month_checker.py
```
---

### **Monthly Data Scheduler**
- **Description:** Automates the retrieval of monthly data from the DHMI (State Airports Authority) website. The script fetches Excel files containing statistics, processes the data, and saves it into a unified Excel file. It runs on a predefined schedule to ensure that data is regularly updated.

- The [main_schedule.py](https://github.com/melisacar/monthly-scrape/blob/main/main_schedule.py) script performs the following tasks:
    - Disable SSL Warnings: Suppresses SSL certificate verification warnings for secure connections.
    - Fetch Page Content: Retrieves the HTML content of the specified DHMI statistics page.
    - Parse Excel Links: Identifies and extracts links to Excel files available on the page.
    - Download Excel Files: Downloads each identified Excel file.
    - Extract Year and Month: Processes date information from the Excel files to format it correctly.
    - Transform Excel Data: Reads and transforms the data from the Excel files into a structured format.
    - Concatenate Data: Merges data from all downloaded Excel files into a single DataFrame.
    - Save to Excel: Writes the final DataFrame into an Excel file named DHMI_all.xlsx.
    - Scheduled Job: Uses the schedule library to run the data retrieval process at specific times on weekdays.
    - End Date Handling: Runs the scheduled job until a specified end date.

#### **Installation**
1. Clone the Repo
```bash
git clone https://github.com/melisacar/monthly-scrape.git
cd monthly-scrape
```
2. Set up the Environment
- Ensure you have Python installed on your machine. Then install the necessary packages using requirements.txt:
```bash
pip3 install -r requirements.txt
```
3. Run the Script
```bash
python3 main_schedule.py
```
---
### **Monthly Data Checker (Schedule)**
- **Description:** Automates the monitoring of the DHMI (State Airports Authority) website for the availability of new monthly data. The script checks the site for new Excel files containing monthly statistics, downloads the latest data if available, and updates a consolidated Excel file. It operates on a schedule to ensure timely updates.

- The [main_mc_schedule.py](https://github.com/melisacar/monthly-scrape/blob/main/main_mc_schedule.py) script performs the following tasks:

    - Disable SSL Warnings: Suppresses SSL certificate verification warnings for secure connections.
    - Fetch Page Content: Retrieves the HTML content of the specified DHMI statistics page.
    - Parse Excel Links: Identifies and extracts the most recent Excel file link available on the page.
    - Extract Month Numbers: Processes the month information from both the HTML content and Excel files.
    - Download Excel Files: Downloads the identified Excel file, ignoring SSL verification.
    - Extract Year and Month: Converts date information to a formatted "YYYY-MM" string.
    - Transform Excel Data: Reads data from all sheets of the downloaded Excel file, transforms it into a structured format, and adds metadata like category and access date.
    - Update Data: Merges the new data with existing data in the file DHMI_all.xlsx.
    - Scheduled Job: Uses the schedule library to run the data check process at specific times on weekdays.
    - End Date Handling: The scheduled job runs until a specified end date, stopping automatically when the date is reached.
#### **Installation**
1. Clone the Repo
```bash
git clone https://github.com/melisacar/monthly-scrape.git
cd monthly-scrape
```
2. Set up the Environment
    - Ensure you have Python installed on your machine. Then install the necessary packages using requirements.txt:
```bash
pip3 install -r requirements.txt
```
3. Run the Script
```bash
python3 main_mc_schedule.py
```
---

### **Requirements**
- Python 3.x
- Required Python packages are listed in [`requirements.txt`](https://github.com/melisacar/monthly-scrape/blob/main/requirements.txt), including:
    - pandas 
    - openpyxl 
    - pytest
    - bs4 
    - requests
    - schedule

#### Error Handling
When trying to install a Python package globally using pip on macOS, the system may not allow the installation. To handle this, you can try the following method:

##### Using a Virtual Environment
You can resolve this issue by creating a virtual environment. A virtual environment provides an isolated Python installation and allows you to work without affecting global packages.

1. Navigate to the Project Directory: Go to the directory where your project is located:
```bash
cd /path/to/your/repo
```
2. Create a Virtual Environment:
```bash
python3 -m venv venv
```
3. Activate the Virtual Environment (for Mac/Linux):
```bash
source venv/bin/activate
```
4. Upgrade pip:
```bash
pip3 install --upgrade pip
```
5. Install Libraries from requirements.txt:
```bash
pip3 install -r requirements.txt
```
### **File Structure**
```bash
monthly_scrape/
|
├── build-files/               # Directory for storing old or deprecated Python scripts.
│   ├── clean_format.py
|   └── ...                    
├── venv/                      # Virtual environment directory for managing dependencies.
│   ├── bin/                   # Executables and scripts for the virtual environment.
│   ├── lib/                   # Python libraries installed in the virtual environment.
│   └── ...                    # Other virtual environment files.
├── .DS_Store                  # macOS system file (can be ignored).
├── .gitignore                 # Specifies files and directories to be ignored by Git.
├── DHMI_all.xlsx              # Output file containing the merged and transformed data.
├── LICENSE.md                 # Contains the license information for the project.
├── README.md                  # Documentation of the project.
├── main_mc_schedule.py        # Script to automate scraping available new month data on a schedule.
├── main_month_checker.py      # Script for checking available new month data.
├── main_schedule.py           # Script to automate data scraping on a schedule.
├── main_scraper.py            # Script for scraping and downloading DHMI Excel files.
├── main_scraper_test.py       # Script for testing main_scraper.py
├── requirements.txt           # List of Python libraries required for the project.
├── ~$DHMI_all.xlsx            # Temporary Excel file (generated by Excel during editing).
```
---

### **License**
This project is licensed under the MIT License - see the [LICENSE](https://github.com/melisacar/monthly-scrape/blob/main/LICENSE.md) file for details.

### **Improvements**
- [x] : New column named "Retrieved at" (***Erişim Tarihi***) will be added. 


---
# **Part 2: Automated PostgreSQL Storage for DHMI Data Using Airflow** 

This project is a continuation of the DHMI Scraping Project, focused on storing monthly flight data in a `PostgreSQL` database using `Docker` and `SQLAlchemy`. Part 2 extends the automation from Part 1 by modifying the existing data processing scripts to write the cleaned data into the database. The entire process is automated using `Apache Airflow`, allowing for scheduled data scraping, transformation, and database insertion. The steps below will guide you through the setup, including creating Docker containers for PostgreSQL, **managing migrations** with SQLAlchemy, and inserting sample data into the database.

1. Create `docker_compose.yaml` File

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

2. Start Services Using Docker Compose

Start the database service defined in the docker-compose.yaml file.

```bash
docker compose down
```

```bash
docker-compose up -d
```
 - This command reads the `docker-compose.yaml` file, pulls the necessary image, creates the PostgreSQL container, and mounts the volume for data persistence.
 - `-d` starts the services in the background

 ```bash
docker ps
 ```
 - List running Docker containers.

 3. Connect to PostgreSQL from Python Using SQLAlchemy
- Connecting to a PostgreSQL database using a simple structure, creating a table, and performing basic CRUD (Create, Read, Update, Delete) operations.
- Install
```shell
pip3 install sqlalchemy psycopg2-binary
```
- Interact with the PostgreSQL database programmatically using Python.
```py
from sqlalchemy import create_engine
# 'postgresql://<user_name>:<passw>@<host>:<port>/<db_name>'
engine = create_engine('postgresql://postgres:secret@localhost:5432/dhmi-scrape')
```
4. Define the ORM Models and Run Migrations Using migration.py

Using SQLAlchemy’s ORM allows us to define our database tables as Python classes. This makes interacting with the database more intuitive, using Python objects instead of raw SQL queries.

```py

from sqlalchemy import create_engine, Column, Integer, Float, String, CHAR, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date

Base = declarative_base()

# Define the Flights table.
class Flight(Base):
    __tablename__ = 'flights' 

    id = Column(Integer, primary_key=True, autoincrement=True)  
    airport_name = Column(String)
    flight_type = Column(String)
    quantity = Column(Float)
    category = Column(String)
    flight_time = Column(CHAR(7))
    retrieved_at = Column(Date)      

engine = create_engine('postgresql://postgres:secret@localhost:5432/dhmi-scrape')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Try with sample data.
sample_flights = [
    Flight(airport_name='Istanbul Airport', flight_type='Domestic', quantity=150.5, category='Economy', flight_time='12:30', retrieved_at=date(2024, 6, 1)),
    Flight(airport_name='Sabiha Gokcen', flight_type='International', quantity=200.0, category='Business', flight_time='14:45', retrieved_at=date(2024, 6, 1)),
    Flight(airport_name='Ankara Esenboga', flight_type='Domestic', quantity=100.0, category='Economy', flight_time='09:00', retrieved_at=date(2024, 6, 2)),
]

session.add_all(sample_flights)
session.commit() 

session.close()
```
5. Run the `migration.py` File
Apply the ORM-defined schema to the PostgreSQL database, creating the necessary tables.
```bash
python3 migration.py
```
- This command runs the migration.py script, which creates the flights table in the database.