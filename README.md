# monthly-scrape
DHMI statistics

## Requirements
pip3 install -r requirements.txt

## Error while updating/installing a package
MacOS'ta pip kullanarak sistem genelinde bir Python paketi yüklemeye çalıştığınızda ve sistem yüklemeye izin vermeyebilir. Bununla başa çıkmak için aşağıdaki yöntemi deneyebilirsin:

### Sanal Ortam Kullanma
Sanal bir ortam oluşturarak bu sorunu çözebilirsin. Sanal ortam, bağımsız bir Python yüklemesi sağlar ve sistem genelindeki paketleri etkilemeden çalışmanı sağlar.

1. Terminalde Proje Dizini: Projenin bulunduğu dizine git:
cd /path/to/your/repo

2. Sanal Ortam Oluştur:
python3 -m venv venv

3. Sanal Ortamı Aktifleştir (Mac/Linux için):
source venv/bin/activate

4. pip'i Güncelle
pip install --upgrade pip

5. Requirements.txt'deki Kütüphaneleri Yükle:
pip install -r requirements.txt

