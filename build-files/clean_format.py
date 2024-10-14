import pandas as pd

# Excel dosyasını okuyoruz (örneğin 'havalimanlari.xlsx' dosyasını)
df = pd.read_excel('filtered_data.xlsx', header=None)  # Başlık yoksa 'header=None'

# Yeni bir DataFrame oluşturmak için boş liste
new_data = []

# Her satır için, istenilen formatta yeni satırlar oluşturuyoruz
for index, row in df.iterrows():
    havalimani = row[0]  # Havalimanı adı (1. sütun)
    ic_hat = row[1]  # İç Hat (2. sütun)
    dis_hat = row[2]  # Dış Hat (3. sütun)
    toplam = row[3]  # Toplam (4. sütun)

    # Her bir havaalanı için üç yeni satır oluştur
    new_data.append([havalimani, 'İç Hat', ic_hat])
    new_data.append([havalimani, 'Dış Hat', dis_hat])
    new_data.append([havalimani, 'Toplam', toplam])

# Yeni DataFrame
new_df = pd.DataFrame(new_data, columns=['Havalimanı', 'Hat Türü', 'Yolcu Sayısı'])

# Yeni DataFrame'i bir Excel dosyasına kaydediyoruz
new_df.to_excel('clean_format.xlsx', index=False)

print("Yeni Excel dosyası başarıyla oluşturuldu.")

