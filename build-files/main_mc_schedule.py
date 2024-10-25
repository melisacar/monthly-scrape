import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
from io import BytesIO
import ssl
import urllib3
import schedule
import time as tm
import pytz
from datetime import datetime

# Map month numbers to names
months_mapping = {
    1: "OCAK SONU",
    2: "ŞUBAT SONU",
    3: "MART SONU",
    4: "NİSAN SONU",
    5: "MAYIS SONU",
    6: "HAZİRAN SONU",
    7: "TEMMUZ SONU",
    8: "AĞUSTOS SONU",
    9: "EYLÜL SONU",
    10: "EKİM SONU",
    11: "KASIM SONU",
    12: "ARALIK SONU"
}

def disable_ssl_warnings():
    """
    Disables SSL certificate verification and suppresses InsecureRequestWarning.
    """
    # Disable SSL certificate verification (be cautious with this)
    ssl._create_default_https_context = ssl._create_unverified_context
    # Suppress only the InsecureRequestWarning from urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_page_content(url):
    """
    Fetches the content of the given URL.
    Returns the response object if successful, else None.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None

def parse_excel_links(html_content):
    """
    Parses the HTML content to find all Excel file links.
    Returns the last href found (the most recent one).
    """
    soup = BeautifulSoup(html_content, "html.parser")
    elements = soup.find_all(
        'a',
        class_="badge border border-primary align-middle p-2 rounded-pill list-group-item-action"
    )
    hrefs = [element.get('href') for element in elements]
    # print(hrefs[-1]) # Control.
    return hrefs[-1] # Return the last href as it represents the most recent file link available on the page.

def extract_month_number(month_string):
    """
    Extracts the month number from the month string (e.g. "TEMMUZ SONU"). 
    Returns the month number as an integer.
    """
    for month, name in months_mapping.items():
        if month_string.strip().upper() == name:
            return month
    return None

def get_latest_month_excel(file_path):
    """
    Gets the latest month number from the Excel file.
    """
    try:
        last_month_str = pd.read_excel(file_path).iloc[-1]['Tarih']
        month_number = last_month_str.split("-")[1]
        return int(month_number)
    except FileNotFoundError:
        return 0

def find_newest_month_html(html_content):
    """
    Checks the month texts from HTML content and returns the largest month number.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    month_numbers = []

    td_elements = soup.find_all(
        'td', class_="text-left"
        )

    for td in td_elements:
        month_string = td.get_text()
        month_number = extract_month_number(month_string)
        if month_number:
            month_numbers.append(month_number)

    return max(month_numbers, default=None) # Returns newest month.

def download_excel_file(href):
    """
    Downloads the Excel file from the given href.
    Returns the content of the file if successful, else None.
    """
    # Encode the URL to handle non-ASCII characters.
    encoded_href = urllib.parse.quote(href, safe=':/')
    # Make the request while ignoring SSL verification
    response = requests.get(encoded_href, verify=False)
    if response.status_code == 200:
        #print(f"Downloaded file size: {len(response.content)} bytes") # Print the size of the downloaded file (for control).
        return response.content
    else:
        print(f"Failed to retrieve {href}, status code: {response.status_code}") 
        return None

def extract_year_month(date_info):
    """
    Extracts the year and month from the given date information string.
    Converts month name to its numerical value and formats as "YYYY-MM-DD".
    """
    # Map Turkish month names to numerical values
    month_mapping = {
        "OCAK": "01", "ŞUBAT": "02", "MART": "03", "NİSAN": "04",
        "MAYIS": "05", "HAZİRAN": "06", "TEMMUZ": "07", "AĞUSTOS": "08",
        "EYLÜL": "09", "EKİM": "10", "KASIM": "11", "ARALIK": "12"
    }
    # Split the date_info to get the year and month part
    parts = date_info.split()
    year = parts[0]  # The first part is the year, e.g., "2024"
    month_text = parts[1]  # The second part is the month in text, e.g., "MART"
    
    # Convert month text to its corresponding number
    month = month_mapping.get(month_text.upper(), "00")  # Default to "01" if month not found
    
    return f"{year}-{month}-01" # Convert to "YYYY-MM-01" format to store as a DATE (YYYY-MM-DD) type in SQL.

def transform_excel_file(excel_content, access_date):
    """
    Reads the Excel content into a pandas DataFrame and processes it.
    """
    sheets_dict = pd.read_excel(BytesIO(excel_content), sheet_name=None) # Read all sheets into a dictionary.
    
    all_sheets = []

    for sheet_name, sheet_data in sheets_dict.items():
        
        additional_info = sheet_data.iloc[0, 4]  # Select the date cell from the first row.
        formatted_date = extract_year_month(additional_info)  # Convert to "YYYY-MM" format.

        # Find the row number that contains "DHMİ TOPLAMI" phrase.
        dhmi_toplami_index = sheet_data[sheet_data.iloc[:,0].str.contains("DHMİ TOPLAMI", na=False)].index.min() #DHMI TOPLAM ifadesinin geçtiği ilk satırı alır.

        # If "DHMİ TOPLAMI" is found, take the data up to this row.
        # If not found, take up to the 9th row from the end.
        end_row = dhmi_toplami_index if dhmi_toplami_index else sheet_data.shape[0] - 8

        processed_data = sheet_data.iloc[2:end_row, [0, 4, 5, 6]]
        processed_data.columns = ['Havalimanı', 'İç Hat', 'Dış Hat', 'Toplam']
        processed_data.fillna(0, inplace=True) 
        processed_data['Kategori'] = sheet_name # Add sheet names as a new column. 
        processed_data['Tarih'] = formatted_date  # Add the formatted date.
        processed_data['Erişim Tarihi'] = access_date  

        all_sheets.append(processed_data) # Append the processed DataFrame to the list.
    
    merged_all_sheets = pd.concat(all_sheets) # Concatenate all DataFrames into one.

    final_data = [] # List to store final transformed data.

    for index, row in merged_all_sheets.iterrows():
        airport = row['Havalimanı']
        domestic = row['İç Hat']
        international = row['Dış Hat']
        total = row['Toplam']
        category = row['Kategori']
        date = row['Tarih']
        access_date = row['Erişim Tarihi']

        final_data.append([airport, 'İç Hat', domestic, category, date, access_date]) # Append function takes single parameter, thus take as a list.
        final_data.append([airport, 'Dış Hat', international, category, date, access_date])
        final_data.append([airport, 'Toplam', total, category, date, access_date])
    

    final_df = pd.DataFrame(final_data, columns=['Havalimanı', 'Hat Türü', 'Num', 'Kategori', 'Tarih', 'Erişim Tarihi']) # Transformed to df to use concat in main() func.
    return final_df

def main_check():
    """
    Main function to check for new data, download, and update the Excel file if needed.
    """
    # Disable SSL warnings.
    disable_ssl_warnings()

    # URL of the site.
    url = "https://www.dhmi.gov.tr/Sayfalar/Istatistikler.aspx"

    # Fetch the page content
    html_content = fetch_page_content(url)
    if not html_content:
        return  # Exit if the page couldn't be retrieved.

    # Parse the HTML to get the latest Excel link.
    latest_href = parse_excel_links(html_content)
    #print(hrefs) # Control

    # Get the last month number from existing data.
    latest_month = get_latest_month_excel('DHMI_all.xlsx')
    #print(latest_month) # Control
    
    # Get the latest month number from html.
    newest_month = find_newest_month_html(html_content)
    #print(newest_month) # Control

    if newest_month and newest_month > latest_month:  
        print(f"Yeni dosya işleniyor: {latest_href}")
        excel_content = download_excel_file(latest_href)
        if excel_content:
            access_date = datetime.now().strftime("%Y-%m-%d") # Get the current date.
            df = transform_excel_file(excel_content, access_date) 
            print("Yeni veri bulundu. Mevcut dosyaya ekleniyor...")
            
            try:
                df_existing = pd.read_excel("DHMI_all.xlsx")
            except FileNotFoundError:
                df_existing = pd.DataFrame()
            
            combined_df = pd.concat([df_existing, df], ignore_index=True)

            combined_df.to_excel("DHMI_all.xlsx", index=False)
            print("Yeni veri başarıyla eklendi.")
        else:
            print(f"{latest_href} indirme hatasından dolayı atlandı.")
    else:
        print("Yeni bir ay verisi bulunamadı.")

#Cron Job using schedule lib.
def job():
    """
    Job to run on schedule.
    """
    print("Job started...")
    main_check()
    print("Job completed.")    

#Use tz identifier Europe/Istanbul for UTC+3.
timezone = pytz.timezone("Europe/Istanbul")
local_time = datetime.now(timezone).strftime("%H:%M")

# Schedule the job to run every day at a specific time.
schedule.every().monday.at("10:31").do(job)
schedule.every().tuesday.at("10:30").do(job)
schedule.every().wednesday.at("10:30").do(job)
schedule.every().thursday.at("10:30").do(job)
schedule.every().friday.at("11:49").do(job)

 # The last day of the first month of the next year (Specific date given).
end_date = datetime(2025, 1, 31, 23, 59, 59, tzinfo=timezone)

# Run the schedule until the specified end date
while datetime.now(timezone) < end_date:
    schedule.run_pending()
    tm.sleep(30)  # Check every minute
# Ctrl + c for quit.