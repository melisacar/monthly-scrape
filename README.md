# **DHMI Monthly Data Automation Project**
##### Description
This project automates the retrieval and processing of monthly data from the DHMI (State Airports Authority) website. It consists of multiple scripts that work together to scrape data, transform it, and save it into a consolidated Excel file. The project runs on a predefined schedule to ensure that data is regularly updated and accessible for analysis.

## Table of Contents
1. File Descriptions
    - [main_scraper.py](#data-scraper-for-dhmi-statistics-page) 
    - [main_month_checker.py](#monthly-data-checker)
    - [main_schedule.py](#monthly-data-scheduler)
2. [Requirements](#requirements)
3. File Structure
4. [License](#license)

### File Descriptions
#### **Data Scraper for DHMI Statistics Page**
##### Description:
The main.py script aims to scrape data from the DHMI (State Airports Authority) website, download Excel files, and process the extracted data. It focuses on extracting relevant information such as airport names and corresponding traffic data (domestic, international, and total). The processed data is then structured into a standardized format to facilitate further analysis and reporting.

- The [main_scraper.py](https://github.com/melisacar/monthly-scrape/blob/main/main_scraper.py) script performs the following tasks:
    - Disables SSL warnings to allow connections to HTTPS sites without certificate verification.
    - Fetches the content of the DHMI statistics page.
    - Parses the HTML to extract links to Excel files.
    - Downloads and processes each Excel file, transforming the data into a structured format.
    - Saves the combined data into a single Excel file named `DHMI_all.xlsx`.

##### **Installation**
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

#### **Monthly Data Checker**
##### Description:
 Automates the process of checking for new monthly data from the DHMI (State Airports Authority) website, downloading the latest Excel files, and updating a local Excel file with the new data.

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

##### **Installation**
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

#### **Monthly Data Scheduler**
##### Description:
Automates the retrieval of monthly data from the DHMI (State Airports Authority) website. The script fetches Excel files containing statistics, processes the data, and saves it into a unified Excel file. It runs on a predefined schedule to ensure that data is regularly updated.

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

##### **Installation**
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

### **Requirements**
- Python 3.x
- Required Python packages are listed in []`requirements.txt`](https://github.com/melisacar/monthly-scrape/blob/main/requirements.txt), including
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
### File Structure
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
├── main_month_checker.py      # Script for checking available new month data.
├── main_schedule.py           # Script to automate data scraping on a schedule.
├── main_scraper.py            # Script for scraping and downloading DHMI Excel files.
├── main_scraper_test.py       # Script for testing main_scraper.py
├── requirements.txt           # List of Python libraries required for the project.
├── ~$DHMI_all.xlsx            # Temporary Excel file (generated by Excel during editing).
```

### License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/melisacar/monthly-scrape/blob/main/LICENSE.md) file for details.