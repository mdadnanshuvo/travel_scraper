from geoalchemy2.shape import from_shape
import scrapy
from shapely.geometry import Point
from .models import Property, create_tables, Session
from scrapy.pipelines.images import ImagesPipeline
import os
from scrapy.exceptions import DropItem


class TripcomScraperPipeline:
    def __init__(self):
        # Ensure that tables are created when the pipeline is initialized
        create_tables()
        self.session = Session()

    def process_item(self, item, spider):
        # Create a POINT geometry for latitude and longitude
        geom = from_shape(Point(float(item['longitude']), float(item['latitude'])), srid=4326)

        # Map Scrapy item to SQLAlchemy model
        property_data = Property(
            title=item['title'],
            rating=item.get('rating'),
            location=item['location'],
            geom=geom,  # Store POINT geometry
            room_type=item['room_type'],
            price=item.get('price'),
            image_path=item.get('image_paths')[0] if item.get('image_paths') else None  # Reference to image path
        )
        
        # Add the property data to the session
        self.session.add(property_data)
        self.session.commit()

        return item

    def close_spider(self, spider):
        # Commit any remaining data and close the session when the spider is closed
        self.session.close()

class CustomImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        # Use the property ID to name the image
        property_id = request.meta.get('property_id', 'default_id')
        image_name = f"{property_id}_{os.path.basename(request.url)}"
        return os.path.join('images', image_name)  # Store in the 'images/' folder

    def get_media_requests(self, item, info):
        # Pass the property_id through the request's metadata
        for url in item['image_urls']:
            request = scrapy.Request(url)
            request.meta['property_id'] = item.get('id')  # Assuming 'id' contains the property ID
            yield request

    def item_completed(self, results, item, info):
        # Handle image download completion and add file paths to item
        images = [x for ok, x in results if ok]
        if not images:
            raise DropItem("No images downloaded")

        item['image_paths'] = [image['path'] for image in images]  # Store paths of downloaded images
        return item