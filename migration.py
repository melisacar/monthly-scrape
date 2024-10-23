
from sqlalchemy import create_engine, Column, Integer, Float, String, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date

# Base class for models.
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
    #retrieved_at = Column(Date, nullable=True)      

# Database connection.
engine = create_engine('postgresql://postgres:secret@localhost:5432/dhmi-scrape')

Base.metadata.create_all(engine)

# Create a session for adding data.
Session = sessionmaker(bind=engine)

#session = Session()