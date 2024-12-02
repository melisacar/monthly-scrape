from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:secret@localhost:5432/dhmi-scrape"
engine = create_engine(DATABASE_URL)

def test_database_connection():
    try:
        with engine.connect() as conn:
            assert conn.closed == False, "Bağlantı açık değil"
            print("Veritabanı bağlantısı başarılı!")
    except Exception as e:
        assert False, f"Veritabanı bağlantısı başarısız: {e}"
