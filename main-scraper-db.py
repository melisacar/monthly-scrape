import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
from io import BytesIO
import ssl
import urllib3
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Flight_Check, engine  # Importing the model and engine from models.py

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
    ssl._create_default_https_context = ssl._create_unverified_context
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
    return hrefs[-1]

def extract_month_number(month_string):
    """
    Extracts the month number from the month string (e.g. "TEMMUZ SONU"). 
    Returns the month number as an integer.
    """
    for month, name in months_mapping.items():
        if month_string.strip().upper() == name:
            return month
    return None

def get_latest_month_from_db(session):
    """
    Gets the latest month number from the 'flight_check' table.
    """
    latest_date = session.query(Flight_Check).order_by(Flight_Check.tarih.desc()).first()
    if latest_date:
        return latest_date.tarih.month
    return 0

def find_newest_month_html(html_content):
    """
    Checks the month texts from HTML content and returns the largest month number.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    month_numbers = []

    td_elements = soup.find_all('td', class_="text-left")
    for td in td_elements:
        month_string = td.get_text()
        month_number = extract_month_number(month_string)
        if month_number:
            month_numbers.append(month_number)

    return max(month_numbers, default=None)

def download_excel_file(href):
    """
    Downloads the Excel file from the given href.
    Returns the content of the file if successful, else None.
    """
    encoded_href = urllib.parse.quote(href, safe=':/')
    response = requests.get(encoded_href, verify=False)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve {href}, status code: {response.status_code}") 
        return None

def extract_year_month(date_info):
    """
    Extracts the year and month from the given date information string.
    Converts month name to its numerical value and formats as "YYYY-MM-DD".
    """
    month_mapping = {
        "OCAK": "01", "ŞUBAT": "02", "MART": "03", "NİSAN": "04",
        "MAYIS": "05", "HAZİRAN": "06", "TEMMUZ": "07", "AĞUSTOS": "08",
        "EYLÜL": "09", "EKİM": "10", "KASIM": "11", "ARALIK": "12"
    }
    parts = date_info.split()
    year = parts[0]
    month_text = parts[1]
    month = month_mapping.get(month_text.upper(), "00")
    
    return f"{year}-{month}-01"

def transform_excel_file(excel_content):
    """
    Reads the Excel content into a pandas DataFrame and processes it.
    """
    sheets_dict = pd.read_excel(BytesIO(excel_content), sheet_name=None)
    all_sheets = []

    for sheet_name, sheet_data in sheets_dict.items():
        additional_info = sheet_data.iloc[0, 4]
        formatted_date = extract_year_month(additional_info)

        dhmi_toplami_index = sheet_data[sheet_data.iloc[:,0].str.contains("DHMİ TOPLAMI", na=False)].index.min()
        end_row = dhmi_toplami_index if dhmi_toplami_index else sheet_data.shape[0] - 8

        processed_data = sheet_data.iloc[2:end_row, [0, 4, 5, 6]]
        processed_data.columns = ['Havalimanı', 'İç Hat', 'Dış Hat', 'Toplam']
        processed_data.fillna(0, inplace=True)
        processed_data['Kategori'] = sheet_name
        processed_data['Tarih'] = formatted_date

        all_sheets.append(processed_data)

    merged_all_sheets = pd.concat(all_sheets)
    final_data = []

    for _, row in merged_all_sheets.iterrows():
        airport = row['Havalimanı']
        domestic = row['İç Hat']
        international = row['Dış Hat']
        total = row['Toplam']
        category = row['Kategori']
        date = row['Tarih']

        final_data.append([airport, 'İç Hat', domestic, category, date])
        final_data.append([airport, 'Dış Hat', international, category, date])
        final_data.append([airport, 'Toplam', total, category, date])

    final_df = pd.DataFrame(final_data, columns=['Havalimanı', 'Hat Türü', 'Num', 'Kategori', 'Tarih'])
    return final_df

def save_to_database(df, session):
    """
    Saves the transformed data to the database.
    """
    for _, row in df.iterrows():
        new_record = Flight_Check(
            havalimani = str(row['Havalimanı']),
            hat_turu = str(row['Hat Türü']),
            num = float(row['Num']), # Change: Convert 'Num' to float to match database schema.
            kategori = str(row['Kategori']),
            tarih = row['Tarih'],
            erisim_tarihi=datetime.today().strftime("%Y-%m-%d")  # Add the current date as the retrieved_at field.
        )
        session.add(new_record)

    session.commit()
    print("Veri başarıyla veritabanına eklendi.")

def main_check():
    """
    Main function to check for new data, download, and update the database if needed.
    """
    disable_ssl_warnings()

    Session = sessionmaker(bind=engine)
    session = Session()

    url = "https://www.dhmi.gov.tr/Sayfalar/Istatistikler.aspx"
    html_content = fetch_page_content(url)
    if not html_content:
        return

    latest_href = parse_excel_links(html_content)
    latest_month = get_latest_month_from_db(session)
    newest_month = find_newest_month_html(html_content)

    if newest_month and newest_month > latest_month:  
        print(f"Yeni dosya işleniyor: {latest_href}")
        excel_content = download_excel_file(latest_href)
        if excel_content:
            df = transform_excel_file(excel_content)
            print("Yeni veri bulundu. Veritabanına ekleniyor...")
            save_to_database(df, session)  # Veriyi kaydetmek için save_to_database fonksiyonunu çağır.
        else:
            print(f"{latest_href} indirme hatasından dolayı atlandı.")
    else:
        print("Yeni bir ay verisi bulunamadı.")

    session.close()

main_check()