import os
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # TimeoutException'ı içe aktar
import time
import pandas as pd

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

# Kullanıcının istediği ayı seçmesi
month_num = 8  

if month_num in months_mapping:
    month_name = months_mapping[month_num]
else:
    print("Geçersiz ay")
    exit()

def get_latest_downloaded_file(download_folder):
    # İndirilmiş en son dosyayı bul
    list_of_files = glob.glob(os.path.join(download_folder, '*.xlsx'))  # Tüm Excel dosyalarını listele
    if not list_of_files:
        print("İndirilen dosya bulunamadı.")
        return None
    latest_file = max(list_of_files, key=os.path.getctime)  # En son indirilen dosyayı al
    return latest_file

def download_excel(month_name):
    driver = webdriver.Safari()
    driver.get('https://www.dhmi.gov.tr/Sayfalar/Istatistikler.aspx')

    wait = WebDriverWait(driver, 10)  # 10 saniye bekle
    
    try:
        # Ay ismi içeren satırı bulma
        row = wait.until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{month_name}')]")))
        
        if row:
            parent_row = row.find_element(By.XPATH, './ancestor::tr')  # Satırın parentını bul
            
            download_buttons = parent_row.find_elements(By.XPATH, ".//a[span[text()='Tümünü İndir']]")

            if download_buttons:
                for button in download_buttons:
                    download_url = button.get_attribute('href')  # İndirme linki
                    print("İndirme linki:", download_url)
                    
                    button.click()  # Dosyayı indirmek için butona tıklayın
                    print("Dosya indirildi")
                    time.sleep(5)  # İndirme süresini beklemek için

                    # İndirilen dosyanın yolunu otomatik olarak bulma
                    download_folder = os.path.expanduser('~/Downloads')  # İndirme klasörü
                    file_path = get_latest_downloaded_file(download_folder)  # En son indirilen dosyayı al
                    if file_path is None:
                        return  # Dosya bulunamazsa çıkış yap
                    
                    # Excel dosyasını okuma
                    df = pd.read_excel(file_path, sheet_name=0, header=3)  # İlk sayfayı 4. satırdan başlat
                    print(df.head())

                    # Gerekli sütunları seçme
                    result_df = df.iloc[0:59, [0, 4, 5, 6]]  # İlk sütun ve E, F, G sütunları
                    result_df.columns = ['Havalimanı', 'İç Hat', 'Dış Hat', 'Toplam']
                    # Boş hücreler varsa, onları doldur
                    result_df.fillna(0, inplace=True)  # Boş hücreleri 0 ile doldur
                    print(result_df.head())

                    # Yeni bir DataFrame oluşturmak için boş liste
                    new_data = []

                    # Her satır için, istenilen formatta yeni satırlar oluşturuyoruz
                    for index, row in result_df.iterrows():
                        havalimani = row['Havalimanı']  # Havalimanı adı (1. sütun)
                        ic_hat = row['İç Hat']  # İç Hat (2. sütun)
                        dis_hat = row['Dış Hat']  # Dış Hat (3. sütun)
                        toplam = row['Toplam']  # Toplam (4. sütun)

                        # Her bir havaalanı için üç yeni satır oluştur
                        new_data.append([havalimani, 'İç Hat', ic_hat])
                        new_data.append([havalimani, 'Dış Hat', dis_hat])
                        new_data.append([havalimani, 'Toplam', toplam])

                    # Yeni DataFrame
                    new_df = pd.DataFrame(new_data, columns=['Havalimanı', 'Hat Türü', 'Yolcu Sayısı'])

                    # Yeni dosyayı kaydetme
                    output_file_path = 'filtered_data.xlsx'  # Çıktı dosyasının adı
                    new_df.to_excel(output_file_path, index=False)  # Yeni dosyayı oluştur
                    print(f"Filtrelenmiş veri kaydedildi: {output_file_path}")
            else:
                print("Tümünü indir butonu bulunamadı")
    except TimeoutException:
        print(f"{month_name} için satır bulunamadı. Sayfa zaman aşımına uğradı.")
    finally:
        driver.quit()  # Tarayıcıyı kapat

# Fonksiyonu çağır
download_excel(month_name)