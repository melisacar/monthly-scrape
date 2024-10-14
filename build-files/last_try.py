import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
from io import BytesIO
import ssl
import urllib3

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
        return response.content
    else:
        print(f"Failed to retrieve {href}, status code: {response.status_code}")
        return None

def transform_excel_file(excel_content):
    """
    Reads the Excel content into a pandas DataFrame and processes it.
    """
    sheets_dict = pd.read_excel(BytesIO(excel_content), sheet_name=None)
    
    all_sheets = []

    for sheet_name, sheet_data in sheets_dict.items():
        
        additional_info = sheet_data.iloc[0, 4]  # 2. satır, 3. sütundaki hücre

        processed_data = sheet_data.iloc[2:61, [0, 4, 5, 6]]
        processed_data.columns = ['Havalimanı', 'İç Hat', 'Dış Hat', 'Toplam']
        processed_data.fillna(0, inplace=True)
        processed_data['Kategori'] = sheet_name
        # 2. satır ve 3. sütundaki bilgiyi al
        
        processed_data['Tarih'] = additional_info  # Yeni sütun ekleniyor
    
        all_sheets.append(processed_data)
    return pd.concat(all_sheets)


def main():
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
        final_df.to_excel("merged_excel_data.xlsx", index=False)
        print("Data has been saved to 'merged_excel_data.xlsx'.")

main()