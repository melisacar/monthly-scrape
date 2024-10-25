from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String, Date

from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# Define the Flights table.
class Flight(Base):
    __tablename__ = 'flights' 

    id=Column(Integer, primary_key=True, autoincrement=True)  
    havalimani=Column(String, nullable=True)
    hat_turu=Column(String, nullable=True)
    num=Column(Float, nullable=True)
    kategori=Column(String, nullable=True)
    tarih=Column(Date, nullable=True)

# Define the Flights Check table.
class Flight_Check(Base):
    __tablename__ = 'flight_check' 
    
    id=Column(Integer, primary_key=True, autoincrement=True)  
    havalimani=Column(String, nullable=True)
    hat_turu=Column(String, nullable=True)
    num=Column(Float, nullable=True)
    kategori=Column(String, nullable=True)
    tarih=Column(Date, nullable=True)
    erisim_tarihi = Column(Date, nullable=True) 

# Database connection.
engine = create_engine('postgresql://postgres:secret@localhost:5432/dhmi-scrape')

# Create tables in the database.
Base.metadata.create_all(engine)

# Create a session for adding data.
Session = sessionmaker(bind=engine)