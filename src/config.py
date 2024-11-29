# Define url manually:
DATABASE_URL = ("postgresql://postgres:secret@localhost:5432/dhmi-scrape") # While using Alembic
#DATABASE_URL = ("postgresql://postgres:secret@database:5432/dhmi-scrape") # While using Docker


#import os

# Toggle between Alembic and Docker
#USE_DOCKER = True  # True if using Docker, False if using Alembic locally

#if USE_DOCKER:
#    DATABASE_URL = "postgresql://postgres:secret@database:5432/dhmi-scrape"  # Docker
#else:
#    DATABASE_URL = "postgresql://postgres:secret@localhost:5432/dhmi-scrape"  # Localhost

#print(f"Kullanılan DATABASE_URL: {DATABASE_URL}")
