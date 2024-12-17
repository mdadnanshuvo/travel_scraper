import os
import scrapy
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from .models import Property, create_tables, Session


class TripcomScraperPipeline:
    def __init__(self):
        # Ensure the database tables are created
        create_tables()
        self.session = Session()

    def process_item(self, item, spider):
        # Ensure essential fields are present
        if not item.get('title') or not item.get('latitude') or not item.get('longitude'):
            raise DropItem("Missing essential fields in item")

        try:
            # Create geometry object from latitude and longitude
            geom = from_shape(
                Point(float(item['longitude']), float(item['latitude'])),
                srid=4326
            )

            # Prepare the database object
            property_data = Property(
                title=item['title'],
                rating=item.get('rating'),
                location=item['location'],
                geom=geom,
                room_type=item.get('room_type', []),
                price=float(item['price'].replace('£', '').replace(',', '')) if item.get('price') else None,
                image_path=item.get('image_paths')[0] if item.get('image_paths') else None
            )

            # Add to the session and commit
            self.session.add(property_data)
            self.session.commit()

        except Exception as e:
            # Rollback and log any errors encountered
            spider.logger.error(f"Database error: {e}")
            self.session.rollback()
            raise DropItem(f"Database error while processing item: {item}")

        return item

    def close_spider(self, spider):
        # Close the database session when the spider finishes
        self.session.close()


class CustomImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        """
        Custom path for saving downloaded images.
        Images are saved in the 'images/' directory with a unique filename
        combining the property ID and the original image's basename.
        """
        property_id = request.meta.get('property_id', 'default_id')
        image_name = os.path.basename(request.url)
        return os.path.join('images', f"{property_id}_{image_name}")

    def get_media_requests(self, item, info):
        """
        Schedule image download requests.
        Associates each image request with a `property_id` for custom file naming.
        """
        for url in item.get('image_urls', []):
            request = scrapy.Request(url)
            request.meta['property_id'] = item.get('id', 'default_id')
            yield request

    def item_completed(self, results, item, info):
        """
        Process results after images have been downloaded.
        Adds the file paths of successfully downloaded images to the item.
        """
        images = [x for ok, x in results if ok]
        if not images:
            raise DropItem("No images downloaded")
        item['image_paths'] = [image['path'] for image in images]
        return item
