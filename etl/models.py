from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class RawCarListing(Base):
    __tablename__ = "cars_raw"

    id = Column(Integer, primary_key=True)
    source_platform = Column(String(100))
    listing_url = Column(Text)
    make = Column(String(100))
    model = Column(String(100))
    year = Column(Integer)
    mileage = Column(Float)
    engine_size = Column(String(50))
    fuel_type = Column(String(50))
    transmission = Column(String(50))
    body_type = Column(String(50))
    price = Column(String(100))
    image_url = Column(Text)
    scraped_at = Column(DateTime, default=datetime.utcnow)

class CleanCarListing(Base):
    __tablename__ = "cars_cleaned"

    id = Column(Integer, primary_key=True)
    source_platform = Column(String(100))
    listing_url = Column(Text)
    make = Column(String(100))
    model = Column(String(100))
    year = Column(Integer)
    mileage_km = Column(Float)
    engine_size_cc = Column(Float)
    fuel_type = Column(String(50))
    transmission = Column(String(50))
    body_type = Column(String(50))
    price_usd = Column(Float)
    price_kes = Column(Float)
    image_url = Column(Text)
    cleaned_at = Column(DateTime, default=datetime.utcnow)
