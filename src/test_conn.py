from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:secret@localhost:5432/dhmi-scrape"
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("Veritabanı bağlantısı başarılı!")
except Exception as e:
    print(f"Bağlantı başarısız: {e}")
