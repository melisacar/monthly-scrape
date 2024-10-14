from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  # TimeoutException'ı içe aktar
import time

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
                    time.sleep(2)  # İndirme süresini beklemek için
            else:
                print("Tümünü indir butonu bulunamadı")
    except TimeoutException:
        print(f"{month_name} için satır bulunamadı. Sayfa zaman aşımına uğradı.")
    finally:
        driver.quit()  # Tarayıcıyı kapat

# Fonksiyonu çağır
download_excel(month_name)