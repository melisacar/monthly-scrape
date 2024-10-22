
from sqlalchemy import create_engine, Column, Integer, Float, String, CHAR, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date

Base = declarative_base()

# Define the Flights table.
class Flight(Base):
    __tablename__ = 'flights' 

    id = Column(Integer, primary_key=True, autoincrement=True)  
    airport_name = Column(String)
    flight_type = Column(String)
    quantity = Column(Float)
    category = Column(String)
    flight_time = Column(CHAR(7))
    retrieved_at = Column(Date)      

engine = create_engine('postgresql://postgres:secret@localhost:5432/dhmi-scrape')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

sample_flights = [
    Flight(airport_name='Istanbul Airport', flight_type='Domestic', quantity=150.5, category='Economy', flight_time='12:30', retrieved_at=date(2024, 6, 1)),
    Flight(airport_name='Sabiha Gokcen', flight_type='International', quantity=200.0, category='Business', flight_time='14:45', retrieved_at=date(2024, 6, 1)),
    Flight(airport_name='Ankara Esenboga', flight_type='Domestic', quantity=100.0, category='Economy', flight_time='09:00', retrieved_at=date(2024, 6, 2)),
]

session.add_all(sample_flights)
session.commit() 

session.close()