from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String, Date

from sqlalchemy.orm import declarative_base, sessionmaker

from sqlalchemy import UniqueConstraint

#import os

#DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

# Define the Flights Check table.
class Flight_Check(Base):
    __tablename__ = 'tum_ucuslar_aylik' 
    __table_args__ = (
                      UniqueConstraint('havalimani', 'hat_turu','kategori', 'tarih', name='unique_ucuslar'), # Avoid duplicate data.
                      {'schema': 'turizm'}
                      )

    id=Column(Integer, primary_key=True, autoincrement=True)  
    havalimani=Column(String, nullable=True)
    hat_turu=Column(String, nullable=True)
    num=Column(Float, nullable=True)
    kategori=Column(String, nullable=True)
    tarih=Column(Date, nullable=True)
    erisim_tarihi = Column(Date, nullable=True) 

# Database connection.
#engine = create_engine('postgresql://postgres:secret@localhost:5432/dhmi-scrape')
#engine = create_engine('postgresql://postgres:secret@database:5432/dhmi-scrape')

DATABASE_URL = 'postgresql://postgres:secret@localhost:5432/dhmi-scrape'
engine = create_engine(DATABASE_URL)


#Create the schema if it doesn't exist
#with engine.connect() as connection:
#   connection.execute("""
#                            CREATE SCHEMA IF NOT EXISTS turizm;
#                      """)

# Create tables in the database.
#Base.metadata.create_all(engine)

# Create a session for adding data.
Session = sessionmaker(bind=engine)