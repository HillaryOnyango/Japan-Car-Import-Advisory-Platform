from sqlalchemy import create_engine
from config.settings import settings

engine = create_engine(settings.database_url)

def get_engine():
    return engine
