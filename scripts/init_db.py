from api.db import create_database_schema
from api import models

if __name__ == "__main__":
    create_database_schema()
    print("✅ Database schema created.")
