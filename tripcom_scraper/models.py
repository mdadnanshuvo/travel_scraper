from sqlalchemy import create_engine, Column, String, Float, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
import os

# Base class for models
Base = declarative_base()

# Property model
class Property(Base):
    __tablename__ = 'properties'

    id = Column(String, primary_key=True, index=True)
    title = Column(String(255), nullable=True)
    rating = Column(Float, nullable=True)
    location = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    geom = Column(Geometry('POINT', srid=4326), nullable=True)  # Spatial data
    price = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    city_id = Column(String(255), nullable=True)
    created_at = Column(String, default=func.now())
    updated_at = Column(String, onupdate=func.now())

# Function to get database engine
def get_database_engine():
    database_url = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/tripcom_data")
    return create_engine(database_url)

# Create a shared engine
engine = get_database_engine()

# Create a session factory
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to create tables
def create_tables():
    Base.metadata.create_all(engine)
