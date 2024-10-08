import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Ay numaralarını ve isimleri eşle
months_mapping = {
    1: "Ocak",
    2: "Şubat",
    3: "Mart",
    4: "Nisan",
    5: "Mayıs",
    6: "Haziran",
    7: "Temmuz",
    8: "AĞUSTOS SONU",
    9: "Eylül",
    10: "Ekim",
    11: "Kasım",
    12: "Aralık"
}

# Kullanıcının istediği ayı seçmesi
month_num = 8  # Buraya istenilen ay numarası yazılır

if month_num in months_mapping:
    month_name = months_mapping[month_num]
else:
    print("Geçersiz ay")
    exit()


def download_excel(month_name):
    url = 'https://www.dhmi.gov.tr/Sayfalar/Istatistikler.aspx'
    r = requests.get(url)

    # Eğer sayfaya erişim sağlanamazsa
    if r.status_code != 200:
        print("Sayfaya erişim sağlanamadı.")
        return

    #Sayfa içeriğini analiz etme
    soup = BeautifulSoup(r.content, 'html.parser')

    #Ay ismi içeren satır bulunur
    row = soup.find(string=month_name)

    #Eğer satır bulunduysa
    if row:
        parent_row = row.find_parent("tr") #satırın parenti bulunur
        #print("Parent Element İçeriği:", parent_row.prettify())
        #button = parent_row.find("a", string = "Tümünü indir") #Buton bulunur
        if parent_row:
            #Parent satırındaki tüm <a> etkiketlerini bul
            all_links = parent_row.find_all("a")

            #7. butonu al, which is tümünü indir
            if len(all_links) >= 7:
                download_button = all_links[6]
                download_url = download_button['href'] #İndirme linki
                print("İndirme linki", download_url)

                #dosya indirilir
                excel_response = requests.get(download_url)
                if excel_response.status_code == 200:
                    with open("deneme_dosya.xlsx", "wb") as f:
                        f.write(excel_response.content)
                    print("Dosya indirildi")
                else:
                    print("Dosya indirilemedi")
            else:
                print("Tümünü indir butonu bulunamadı")
        else:
            print("Satırın parent elementi bulunamadı")
    else:
        print("Satır bulunamadı")

# Fonksiyonu çağır
download_excel(month_name)