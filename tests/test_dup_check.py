from sqlalchemy import func
from src.models import Flight_Check, Session


def check_duplicates():
    session = Session()

    # Duplicate kontrolü
    duplicates = session.query(
        Flight_Check.havalimani,
        Flight_Check.hat_turu,
        Flight_Check.kategori,
        Flight_Check.tarih,
        func.count('*').label('count')
    ).group_by(
        Flight_Check.havalimani,
        Flight_Check.hat_turu,
        Flight_Check.kategori,
        Flight_Check.tarih
    ).having(
        func.count('*') > 1
    ).all()

    session.close()
    return duplicates


# Test func
def test_check_duplicates():
    duplicates = check_duplicates()
    assert len(duplicates) == 0, f"Duplicate records found: {duplicates}"
