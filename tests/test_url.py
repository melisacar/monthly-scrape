from src.config import DATABASE_URL

def test_database_url():
    assert DATABASE_URL is not None, "DATABASE_URL is not set"
    print(f"Using database URL: {DATABASE_URL}")


# To see test output run:
# pytest -s 