import os
import re
import uuid
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from scrapy.exceptions import DropItem
from .models import Property, create_tables, Session


class TripcomScraperPipeline:
    def __init__(self):
        create_tables()  # Ensure tables are created before processing items
        self.session = Session()  # Initialize a database session

    def process_item(self, item, spider):
        # Validate essential fields
        if not item.get('hotelName') or not item.get('latitude') or not item.get('longitude'):
            spider.logger.warning(f"Item missing essential fields: {item}")
            raise DropItem("Missing essential fields in item")

        try:
            # Generate geometry for PostGIS
            geom = from_shape(
                Point(float(item['longitude']), float(item['latitude'])),
                srid=4326
            )

            # Clean and validate price
            price = item.get('price')
            if price is not None:
                if isinstance(price, str):
                    try:
                        price = float(re.sub(r'[^\d.]', '', price))  # Remove non-numeric characters
                    except ValueError:
                        spider.logger.warning(f"Invalid price format: {price}")
                        price = None
                elif isinstance(price, (int, float)):
                    price = float(price)  # Convert numeric prices to float

            # Generate a unique UUID for the `id` field
            unique_id = str(uuid.uuid4())

            # Prepare the property data for database insertion
            property_data = Property(
                id=unique_id,  # Assign a unique identifier
                title=item['hotelName'],
                rating=item.get('rating'),
                location=item['location'],
                latitude=item['latitude'],
                longitude=item['longitude'],
                geom=geom,
                price=price,
                image_url=item.get('imageUrl'),
                city_id=item.get('city_id')
            )

            # Save to database
            self.session.add(property_data)
            self.session.commit()  # Commit changes to the database

        except Exception as e:
            spider.logger.error(f"Database error for item {item}: {e}")
            self.session.rollback()  # Roll back in case of an error
            raise DropItem(f"Failed to save item to database: {e}")

        return item

    def close_spider(self, spider):
        # Ensure the session is closed when the spider finishes
        self.session.close()
