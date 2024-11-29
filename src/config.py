# Define url manually:
#DATABASE_URL = ("postgresql://postgres:secret@localhost:5432/dhmi-scrape") # While using Alembic
#DATABASE_URL = ("postgresql://postgres:secret@database:5432/dhmi-scrape") # While using Docker

import os
# Get the environment
env = os.getenv("ENV", "local")

# Set the default DATABASE_URL if not provided
if env == "docker":
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:secret@database:5432/dhmi-scrape")
elif env == "local":
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:secret@localhost:5432/dhmi-scrape")
#elif env == "prod":
#    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:secret@proddb:5432/dhmi-scrape")
else:
    DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise Exception("DATABASE_URL not found in environment")
