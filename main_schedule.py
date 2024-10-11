import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
from io import BytesIO
import ssl
import urllib3

import schedule


# Ay numaralarını ve isimleri eşle
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

EXCEL_FILE = 'DHMI_all.xlsx'


def fetch_page_content(url):
    """
    Fetches the content of the given URL.
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
    """
    encoded_href = urllib.parse.quote(href, safe=':/')
    response = requests.get(encoded_href, verify=False)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve {href}, status code: {response.status_code}")
        return None

def transform_excel_file(excel_content):
    """
    Transforms the Excel file into the desired format.
    """
    sheets_dict = pd.read_excel(BytesIO(excel_content), sheet_name=None) 
    all_sheets = []

    for sheet_name, sheet_data in sheets_dict.items():
        additional_info = sheet_data.iloc[0, 4]  # Tarih hücresini seç
        processed_data = sheet_data.iloc[2:, [0, 4, 5, 6]]  
        processed_data.columns = ['Havalimanı', 'İç Hat', 'Dış Hat', 'Toplam']
        processed_data.fillna(0, inplace=True)
        processed_data['Kategori'] = sheet_name 
        processed_data['Tarih'] = additional_info  
        all_sheets.append(processed_data)
    
    merged_all_sheets = pd.concat(all_sheets) 
    return merged_all_sheets




