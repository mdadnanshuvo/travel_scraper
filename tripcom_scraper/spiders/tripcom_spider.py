import scrapy
from tripcom_scraper.items import TripcomScraperItem
from urllib.parse import urljoin

class TripcomSpider(scrapy.Spider):
    name = "tripcom_spider"
    allowed_domains = ["uk.trip.com"]
    start_urls = [
        "https://uk.trip.com/hotels/list?city=338&checkin=2025/04/1&checkout=2025/04/03"
    ]

    def parse(self, response):
        # Example: Adjust the selector to target the correct listings on the page
        listings = response.css('div.hotel-listing')  # Update with actual class

        for listing in listings:
            item = TripcomScraperItem()

            item['title'] = listing.css('h3.hotel-title::text').get()
            item['rating'] = listing.css('span.rating-value::text').get()
            item['location'] = listing.css('span.hotel-location::text').get()
            
            # Extract latitude and longitude from meta tags if available
            item['latitude'] = listing.css('meta[name="latitude"]::attr(content)').get()
            item['longitude'] = listing.css('meta[name="longitude"]::attr(content)').get()
            
            item['room_type'] = listing.css('span.room-type::text').get()
            item['price'] = listing.css('span.price::text').get().strip().replace("£", "")  # Clean up price formatting
            
            # Extracting image URLs
            image_urls = listing.css('img::attr(src)').getall()
            # Ensure all URLs are absolute URLs
            item['image_urls'] = [urljoin(response.url, url) for url in image_urls]

            # If you need additional metadata, you can add it here
            item['id'] = listing.css('div.property-id::text').get()

            yield item

        # Handle pagination (if applicable)
        next_page = response.css('a.next-page::attr(href)').get()  # Update with correct pagination selector
        if next_page:
            yield response.follow(next_page, self.parse)
