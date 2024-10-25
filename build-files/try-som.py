import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
from io import BytesIO
import ssl
import urllib3
from sqlalchemy.orm import sessionmaker
from models import Flight_Check, Base, engine
from datetime import date, datetime

def disable_ssl_warnings():
    """
    Disables SSL certificate verification and suppresses InsecureRequestWarning.
    """
    # Disable SSL certificate verification (be cautious with this).
    ssl._create_default_https_context = ssl._create_unverified_context
    # Suppress only the InsecureRequestWarning from urllib3.
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
    month = month_mapping.get(month_text.upper(), "01")  # Default to "01" if month not found
    
    #return f"{year}-{month}-01" # Convert to "YYYY-MM-01" format to store as a DATE (YYYY-MM-DD) type in SQL.
    # Convert the string to a date object
    date_str = f"{year}-{month}-01"  # "YYYY-MM-01"
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

    return date_obj

def transform_excel_file(excel_content):
    """
    Reads the Excel content into a pandas DataFrame and processes it.
    """
    sheets_dict = pd.read_excel(BytesIO(excel_content), sheet_name=None) # Read all sheets into a dictionary.
    
    all_sheets = []

    for sheet_name, sheet_data in sheets_dict.items():
        
        additional_info = sheet_data.iloc[0, 4]  # Select the date cell from the first row.
        formatted_date = extract_year_month(additional_info)

        # Find the row number that contains "DHMİ TOPLAMI" phrase.
        dhmi_toplami_index = sheet_data[sheet_data.iloc[:,0].str.contains("DHMİ TOPLAMI", na=False)].index.min() #DHMI TOPLAM ifadesinin geçtiği ilk satırı alır.

        # If "DHMİ TOPLAMI" is found, take the data up to this row.
        # If not found, take up to the 9th row from the end.
        end_row = dhmi_toplami_index if dhmi_toplami_index else sheet_data.shape[0] - 8

        processed_data = sheet_data.iloc[2:end_row, [0, 4, 5, 6]]
        processed_data.columns = ['havalimani', 'İç Hat', 'Dış Hat', 'Toplam']
        processed_data['kategori'] = sheet_name # Add sheet names as a new column. 
        processed_data['tarih'] = formatted_date  # Change: Store date object instead of string.

        all_sheets.append(processed_data) # Append the processed DataFrame to the list.
    
    merged_all_sheets = pd.concat(all_sheets) # Concatenate all DataFrames into one.

    final_data = [] # List to store final transformed data.

    for index, row in merged_all_sheets.iterrows():
        airport = str(row['havalimani'])
        domestic = float(row['İç Hat']) # Change: Ensure values are converted to float.
        international = float(row['Dış Hat']) # Change: Ensure values are converted to float.
        total = float(row['Toplam']) # Change: Ensure values are converted to float.
        category = str(row['kategori'])
        date = row['tarih']

        final_data.append([airport, 'İç Hat', domestic, category, date]) # Append function takes single parameter, thus take as a list.
        final_data.append([airport, 'Dış Hat', international, category, date])
        final_data.append([airport, 'Toplam', total, category, date])
    

    final_df = pd.DataFrame(final_data, columns=['havalimani', 'hat_turu', 'num', 'kategori', 'tarih']) # Transformed to df to use concat in main() func.
    # print(final_df.head()) Debug.
    return final_df

def save_to_database(df):
    """
    Saves a list of Flight objects to the PostgreSQL database.
    """
    flight_objects = []
    # Create a session.
    Session = sessionmaker(bind=engine)
    session = Session()

    for index, row in df.iterrows():
        # Debug: Show which row is being processed
        # print(f"Processing row {index}: {row.to_dict()}")
        # print(f"Before saving to DB: {row['hat_turu']}") # Debug 
        flight = Flight_Check(
            havalimani=str(row['havalimani']),
            hat_turu=str(row['hat_turu']),
            num=float(row['num']),  # Convert 'num' to float to match database schema.
            kategori=str(row['kategori']),
            tarih=row['tarih']
        )
        flight_objects.append(flight)  # Append the flight object to the list
    
    try:
        # Add each flight object to the session.
        session.add_all(flight_objects)
        session.commit()
        print("Data has been written to the PostgreSQL database.")
    except Exception as e:
        session.rollback()  # Rollback in case of error.
        print(f"An error occurred: {e}")
    finally:
        session.close()

def main():
    # Disable SSL warnings.
    disable_ssl_warnings()

    # URL of the site.
    url = "https://www.dhmi.gov.tr/Sayfalar/Istatistikler.aspx"

    # Fetch the page content
    html_content = fetch_page_content(url)
    if not html_content:
        return  # Exit if the page couldn't be retrieved.

    # Parse the HTML to get Excel links.
    hrefs = parse_excel_links(html_content)

    all_data = []  # List to hold all df DataFrames.

    # Loop through the URLs and process each Excel file.
    for href in hrefs:
        print(f"Processing file from {href}")
        excel_content = download_excel_file(href)
        if excel_content:
            flight_df = transform_excel_file(excel_content)  # Transform the file.
            all_data.append(flight_df)  # Append each df to the list.
        else:
            print(f"Skipping {href} due to download error.")
    
    # Concatenate all DataFrames into a single DataFrame.
    if all_data:
        output = pd.concat(all_data, ignore_index=True)
        #print(output.columns) # Debug
        #print(output.head()) # Debug
        # print(output) Control
        save_to_database(output)
    
if __name__ == "__main__":
    main()