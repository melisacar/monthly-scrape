## Libraries

- ssl: Allows operations related to SSL certificates and secure internet connections.
- urllib3: A library used to manage HTTP requests (sending or receiving data to websites). This library can often give warnings when SSL certificates are not verified, and these warnings are turned off in this code.

```py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse
from io import BytesIO
import ssl 
import urllib3 
```
```py
def disable_ssl_warnings():
    """
    SSL sertifika doğrulamasını devre dışı bırakır ve InsecureRequestWarning uyarısını bastırır.
    """

    # Python'un HTTPS bağlantılarında SSL sertifika doğrulamasını devre dışı bırak.
    ssl._create_default_https_context = ssl._create_unverified_context
    
    # urllib3'ten gelen yalnızca InsecureRequestWarning uyarılarını bastırılır
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```
```py
def fetch_page_content(url):
    """
    Verilen URL'nin içeriğini getirir.
    Başarılı olursa yanıt nesnesini, aksi takdirde None döndürür.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None
```
```py
def parse_excel_links(html_content):
    """
    HTML içeriğini analiz eder ve tüm Excel dosyası bağlantılarını bulur.
    href'lerin bir listesini döner.
    """
    soup = BeautifulSoup(html_content, "html.parser") # HTML içeriğini BeautifulSoup ile parse (çözümleme) etme.
    # Belirtilen sınıfa (class) sahip tüm 'a' (bağlantı) etiketlerini bul.
    elements = soup.find_all(
        'a',
        class_="badge border border-primary align-middle p-2 rounded-pill list-group-item-action"
    )
    # Bulunan elemanların 'href' (bağlantı) değerlerini alıyoruz
    hrefs = [element.get('href') for element in elements]
    return hrefs # Tüm bağlantıları içeren listeyi döndür
```
```py
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
```

```py
def transform_excel_file(excel_content):
    """
    Reads the Excel content into a pandas DataFrame and processes it.
    """
    df = pd.read_excel(BytesIO(excel_content), sheet_name=None, skiprows=3)

    sheets = df.keys()

    print(sheets)

    new_data = []

    for s in sheets:
       s_df = df[s]

       result_df = s_df.iloc[0:59, [0, 4, 5, 6]]

       print(result_df)

```

```py
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

    # Loop through the URLs and process each Excel file
    for href in hrefs:
        print(f"Processing file from {href}")
        excel_content = download_excel_file(href)
        if excel_content:
            transform_excel_file(excel_content)
        else:
            print(f"Skipping {href} due to download error.")

```

```py
main()
````
