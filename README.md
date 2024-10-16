## Project Overview
- This Python script automates the process of scraping, downloading, and transforming monthly airport statistics from the DHMI (State Airports Authority) website. While the script requires manual execution, it is particularly useful for gathering and organizing data from multiple Excel files into a single, structured dataset. The output is an Excel file named DHMI_all.xlsx, which contains organized data across various airports in Türkiye, categorized by type of flight (domestic, international, and total) and date. 

- In the next stage of development, the script will be enhanced to fully automate the data retrieval process, allowing it to check for new data periodically and update the dataset automatically.

### Overview of the Script
- The script performs the following steps:

    1. Disable SSL Warnings:

        Uses a helper function `disable_ssl_warnings()` to disable SSL verification and suppress warnings. This is useful when accessing websites with unverified SSL certificates.

    2. Fetch HTML Content:

        `fetch_page_content(url)` retrieves the HTML content of the DHMI statistics page. If the content is successfully retrieved, it returns the page content; otherwise, it prints an error message.

    3. Parse Excel Links:

        `parse_excel_links(html_content)` parses the HTML content using **BeautifulSoup** to extract links to Excel files. It targets specific anchor tags that contain the Excel file URLs, returning them as a list.

    4. Download Excel Files:

        `download_excel_file(href)` downloads the Excel file from a given link. It encodes the URL to handle non-ASCII characters, sends a GET request, and retrieves the file content if successful.

    5. Transform Excel Files:

        `transform_excel_file(excel_content)` reads the content of each Excel file into a Pandas DataFrame and processes it. This function:

    6. Extracts date information from the file.
        
        Locates the section of data up to the row containing "DHMİ TOPLAMI" (DHMI Total).
        Extracts relevant columns (Airport, Domestic Flights, International Flights, Total Flights).
        Formats the data into separate rows for each airport and flight type, adding metadata like date and category (sheet name).

    7. Main Function:

        - The `main()` function coordinates the entire process:
            - Disables SSL warnings.
            - Fetches the HTML content of the DHMI page.
            - Extracts and processes each Excel file link.
            - Transforms the data from each file into a DataFrame.
            - Combines all DataFrames into a single DataFrame.
            - Saves the final dataset into an Excel file DHMI_all.xlsx.

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
python3 main_.py
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
pip3 install --upgrade pip
```
5. Install Libraries from requirements.txt:
```bash
pip3 install -r requirements.txt
```