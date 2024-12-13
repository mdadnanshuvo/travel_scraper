import scrapy

class TripcomScraperItem(scrapy.Item):
    title = scrapy.Field()
    rating = scrapy.Field()
    location = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    room_type = scrapy.Field()
    price = scrapy.Field()
    image_urls = scrapy.Field()  # For image URLs
    image_paths = scrapy.Field()  # For storing the relative path of the downloaded images

class TripcomSpider(scrapy.Spider):
    name = 'tripcom_spider'
    start_urls = ['https://example.com']  # Your start URL(s)

    def parse(self, response):
        # Example: Let's assume each listing is in a div with class 'listing'
        listings = response.css('div.listing')

        for listing in listings:
            item = TripcomScraperItem()

            item['title'] = listing.css('h3::text').get()
            item['rating'] = listing.css('span.rating::text').get()
            item['location'] = listing.css('span.location::text').get()
            item['latitude'] = listing.css('meta[name="latitude"]::attr(content)').get()
            item['longitude'] = listing.css('meta[name="longitude"]::attr(content)').get()
            item['room_type'] = listing.css('span.room-type::text').get()
            item['price'] = listing.css('span.price::text').get()
            item['image_urls'] = listing.css('img::attr(src)').getall()

            # Yield the item instead of returning
            yield item
