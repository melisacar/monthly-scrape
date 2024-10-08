# Project Overview

This project is an automation tool designed to scrape data from the DHMI (State Airports Authority) website. The script checks for updates on passenger statistics at airports, specifically focusing on monthly data.

## Key Features

- **Web Scraping:** The tool utilizes Selenium to navigate and extract data from the DHMI website.
- **Monthly Checks:** The script is designed to run daily from the first of each month, checking if new data for the current month has been published.
- **Data Storage:** Once new data is detected, it scrapes the relevant passenger statistics and saves them in an organized Excel file format for further analysis.

## **Installation**
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
python3 main_formatted.py
```

### Error Handling
When trying to install a Python package globally using pip on macOS, the system may not allow the installation. To handle this, you can try the following method:

#### Using a Virtual Environment
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
pip install --upgrade pip
```
5. Install Libraries from requirements.txt:
```bash
pip3 install -r requirements.txt
```
