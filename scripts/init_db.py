from api import models
from api.db import create_database_schema

if __name__ == "__main__":
    create_database_schema()
    print("✅ Database schema created.")
