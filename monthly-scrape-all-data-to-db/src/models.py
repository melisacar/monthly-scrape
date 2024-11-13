from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String, Date

from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# Define the Flights Check table.
class Flights(Base):
    __tablename__ = 'tum_ucuslar' 
    
    id=Column(Integer, primary_key=True, autoincrement=True)  
    havalimani=Column(String, nullable=True)
    hat_turu=Column(String, nullable=True)
    num=Column(Float, nullable=True)
    kategori=Column(String, nullable=True)
    tarih=Column(Date, nullable=True)
    erisim_tarihi = Column(Date, nullable=True) 

# Database connection.
#engine = create_engine(connection_type://database_username:password@host:port/database_name)

#engine = create_engine('postgresql://postgres:secret@localhost:5432/dhmi-scrape')
engine = create_engine('postgresql://postgres:secret@localhost:5432/automation?client_encoding=utf8')

# Create tables in the database.
Base.metadata.create_all(engine)

# Create a session for adding data.
Session = sessionmaker(bind=engine)