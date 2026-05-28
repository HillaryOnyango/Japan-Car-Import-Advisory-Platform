from etl.database import engine
from etl.models import Base

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database tables created successfully.")
