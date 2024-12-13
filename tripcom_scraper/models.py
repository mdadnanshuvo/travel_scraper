from sqlalchemy import Column, Integer, String, Float, create_engine
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    rating = Column(Float, nullable=True)
    location = Column(String, nullable=True)
    geom = Column(Geometry('POINT'), nullable=False)  # PostGIS geometry column
    room_type = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    image_path = Column(String, nullable=True)  # Store relative path to images

# Configure database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/tripcom_data")

# Database connection setup
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_tables():
    """Create the tables if they don't exist."""
    Base.metadata.create_all(engine)  # Create the tables in the DB
    print("Tables created successfully.")

def insert_properties(properties):
    """Yield each property after adding it to the database."""
    session = Session()
    
    try:
        for property in properties:
            session.add(property)  # Add property to the session
            yield property  # Yield property for processing
        
        session.commit()  # Commit after all properties are processed
    except Exception as e:
        session.rollback()  # Rollback in case of error
        print(f"Error inserting properties: {e}")
    finally:
        session.close()  # Close the session

# Ensure the tables are created automatically when the app starts
create_tables()
