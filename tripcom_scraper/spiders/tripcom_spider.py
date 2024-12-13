import scrapy
from tripcom_scraper.items import TripcomScraperItem
from urllib.parse import urljoin

class TripcomSpider(scrapy.Spider):
    name = "tripcom_spider"
    allowed_domains = ["uk.trip.com"]
    start_urls = [
        "https://uk.trip.com/hotels/list?city=338&checkin=2025/04/1&checkout=2025/04/03"
    ]

    def start_requests(self):
        # Send requests to the start URLs using regular Scrapy Request
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        # Select all hotel listings from the page (you may need to update the selector based on the actual page)
        listings = response.css('div.hotel-listing')  # Update with actual class name

        for listing in listings:
            item = TripcomScraperItem()

            # Extracting hotel details
            item['title'] = listing.css('h3.hotel-title::text').get() or ''
            item['rating'] = listing.css('span.rating-value::text').get() or ''
            item['location'] = listing.css('span.hotel-location::text').get() or ''
            
            # Extract latitude and longitude from meta tags if available
            item['latitude'] = listing.css('meta[name="latitude"]::attr(content)').get() or ''
            item['longitude'] = listing.css('meta[name="longitude"]::attr(content)').get() or ''
            
            item['room_type'] = listing.css('span.room-type::text').get() or ''
            # Clean up price formatting
            price = listing.css('span.price::text').get() or ''
            item['price'] = price.strip().replace("£", "").replace(",", "")  # Remove "£" and commas in price

            # Extracting image URLs and ensure they are absolute URLs
            image_urls = listing.css('img::attr(src)').getall()
            item['image_urls'] = [urljoin(response.url, url) for url in image_urls]

            # Extract property ID if available
            item['id'] = listing.css('div.property-id::text').get() or ''

            yield item

        # Handle pagination (if applicable, ensure the correct CSS selector for pagination is used)
        next_page = response.css('a.pagination-next::attr(href)').get()  # Update with correct pagination selector
        if next_page:
            # Use Scrapy Request to load the next page if it exists
            yield scrapy.Request(urljoin(response.url, next_page), self.parse)
