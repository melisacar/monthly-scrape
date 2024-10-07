import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Ay numaralarını ve isimlerini eşle
months_mapping = {
    1: "Ocak",
    2: "Şubat",
    3: "Mart",
    4: "Nisan",
    5: "Mayıs",
    6: "Haziran",
    7: "Temmuz",
    8: "Ağustos",
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


#def download_excel(month):
    url = 'https://www.dhmi.gov.tr/Sayfalar/Istatistikler.aspx'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

#Ay ismi içeren satır bulunur
row = soup.find(string=month_name)

#Eğer satır bulunduysa
if row:
    parent_row = row.find_parent() #satırın parenti bulunur
    button = parent_row.find("a", "Tümünü indir")

    if button and 'href' in button.attrs:
        #indirme linki alınır
        download_url = button['href']
        print("İndirme linki", download_url)

        #dosya indirilir
        excel_response = requests.get(download_url)
        with open("deneme_dosya.xlsx", "wb") as f:
            f.write(excel_response.content)
        print("Dosya indirildi")
else:
    print("Satır bulunamadı")
