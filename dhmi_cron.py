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
    Returns a list of hrefs.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    elements = soup.find_all(
        'a',
        class_="badge border border-primary align-middle p-2 rounded-pill list-group-item-action"
    )
    hrefs = [element.get('href') for element in elements]
    return hrefs

def download_excel_file(href):
    """
    Downloads the Excel file from the given href.
    Returns the content of the file if successful, else None.
    """
    # Encode the URL to handle non-ASCII characters
    encoded_href = urllib.parse.quote(href, safe=':/')
    # Make the request while ignoring SSL verification
    response = requests.get(encoded_href, verify=False)
    if response.status_code == 200:
        #print(f"Downloaded file size: {len(response.content)} bytes") # Dosya boyutunu yazdır (kontrol-1).
        return response.content
    else:
        print(f"Failed to retrieve {href}, status code: {response.status_code}") 
        return None

def transform_excel_file(excel_content):
    """
    Reads the Excel content into a pandas DataFrame and processes it.
    """
    sheets_dict = pd.read_excel(BytesIO(excel_content), sheet_name=None) # Get all sheets.
    
    all_sheets = []

    for sheet_name, sheet_data in sheets_dict.items():
        
        additional_info = sheet_data.iloc[0, 4]  # Select the date cell.

        processed_data = sheet_data.iloc[2:59, [0, 4, 5, 6]]
        processed_data.columns = ['Havalimanı', 'İç Hat', 'Dış Hat', 'Toplam']
        processed_data.fillna(0, inplace=True) 
        processed_data['Kategori'] = sheet_name # Add sheet names as a column.
        processed_data['Tarih'] = additional_info  # Add date as a new column.

        all_sheets.append(processed_data) # Append the processed DataFrame to the all_sheets list.
    
    merged_all_sheets = pd.concat(all_sheets) # Concatenate all dfs.

    final_data = []

    for index, row in merged_all_sheets.iterrows():
        havalimani = row['Havalimanı']
        ic_hat = row['İç Hat']
        dis_hat = row['Dış Hat']
        toplam = row['Toplam']
        kategori = row['Kategori']
        tarih = row['Tarih']

        final_data.append([havalimani, 'İç Hat', ic_hat, kategori, tarih]) # The append function takes a single parameter, so append this as a list.
        final_data.append([havalimani, 'Dış Hat', dis_hat, kategori, tarih])
        final_data.append([havalimani, 'Toplam', toplam, kategori, tarih])
    

    final_df = pd.DataFrame(final_data, columns=['Havalimanı', 'Hat Türü', 'Num', 'Kategori', 'Tarih']) # Converted to df because it will be concatenated in the main function.
    return final_df

def dhmi_scrape():
    # Disable SSL warnings
    disable_ssl_warnings()

    # URL of the site
    url = "https://www.dhmi.gov.tr/Sayfalar/Istatistikler.aspx"

    # Fetch the page content
    html_content = fetch_page_content(url)
    if not html_content:
        return  # Exit if the page couldn't be retrieved

    # Parse the HTML to get Excel links
    hrefs = parse_excel_links(html_content)

    all_data = []  # List to hold all df DataFrames

    # Loop through the URLs and process each Excel file
    for href in hrefs:
        print(f"Processing file from {href}")
        excel_content = download_excel_file(href)
        if excel_content:
            df = transform_excel_file(excel_content)  # Transform the file
            all_data.append(df)  # Append each df to the list
        else:
            print(f"Skipping {href} due to download error.")
    
    # Concatenate all DataFrames into a single DataFrame
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)

        # Save the final DataFrame to a single Excel file
        final_df.to_excel("DHMI_all.xlsx", index=False)
        print("Data has been saved to 'DHMI_all.xlsx'.")

dhmi_scrape()

#Cron Job will ve used from terminal.






