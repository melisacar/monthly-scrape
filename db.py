from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:secret@localhost:5432/dhmi-scrape')


