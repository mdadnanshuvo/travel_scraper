import scrapy
from scrapy_selenium import SeleniumRequest
from tripcom_scraper.items import TripcomScraperItem
from urllib.parse import urljoin

class TripcomSpider(scrapy.Spider):
    name = 'tripcom_spider'
    allowed_domains = ['uk.trip.com']
    start_urls = [
        "https://uk.trip.com/hotels/ukhiya-upazila-hotel-detail-7073640/royal-tulip-sea-pearl-beach-resort-and-spa-coxs-bazar/?checkin=2024-12-23&city=270535&module=list&link=button&from_page=list&adult=1&checkout=2024-12-24"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=20,  # Increased wait time to ensure JavaScript is fully loaded
                dont_filter=True  # Allow retries
            )

    def parse(self, response):
        # Scrape main hotel details
        item = TripcomScraperItem()

        # Title
        item['title'] = response.css("h1.headInit_headInit-title_nameA__EE_LB::text").get(default='').strip()

        # Location
        item['location'] = response.css(".headInit_headInit-address_text__D_Atv::text").get(default='').strip()

        # Rating
        item['rating'] = response.css("em.reviewTop_reviewTop-score__FpKsA::text").get(default='').strip()

        # Room Types
        rooms = []
        for room in response.css(".commonRoomCard__BpNjl"):
            room_type = room.css(".commonRoomCard-title__iYBn2::text").get(default='').strip()
            price = room.css(".saleRoomItemBox-priceBox-displayPrice__gWiOr span::text").get(default='').strip()
            rooms.append({'room_type': room_type, 'price': price})
        item['room_type'] = rooms

        # Price
        item['price'] = response.css("span.priceBox_priceBox-container_realPrice__4VuNW::text").get(default='').strip()

        # Images
        image_urls = response.css(".headAlbum_headAlbum_img__vfjQm::attr(src)").getall()
        item['image_urls'] = [urljoin(response.url, url) for url in image_urls if url]

        # Latitude and Longitude
        map_marker = response.css("div[id^='map-list-']::attr(id)").get()
        retry_count = response.meta.get('retry_count', 0)

        if not map_marker and retry_count < 3:  # Retry up to 3 times
            self.logger.info(f"Map marker not found, retrying... Attempt {retry_count + 1}")
            yield SeleniumRequest(
                url=response.url,
                callback=self.parse,
                wait_time=10 + (5 * retry_count),  # Increment wait time with each retry
                meta={'retry_count': retry_count + 1},  # Pass retry count
                dont_filter=True  # Allow retries of the same URL
            )
            return

        if map_marker:
            try:
                # Remove the "map-list-" prefix and split by "." to extract coordinates
                coords = map_marker.replace("map-list-", "").split('.')
                if len(coords) >= 4:
                    item['latitude'] = f"{coords[0]}.{coords[1]}"
                    item['longitude'] = f"{coords[2]}.{coords[3]}"
                else:
                    self.logger.warning("Invalid map marker format for coordinates.")
                    item['latitude'] = ''
                    item['longitude'] = ''
            except Exception as e:
                self.logger.error(f"Error parsing latitude and longitude: {e}")
                item['latitude'] = ''
                item['longitude'] = ''
        else:
            self.logger.warning("Map marker could not be retrieved after retries.")
            item['latitude'] = ''
            item['longitude'] = ''

        # Debugging log for extracted item
        self.logger.info(f"Extracted data: {item}")

        # Yield the item
        yield item

        # Pagination (if required)
        next_page = response.css("a.pagination-next::attr(href)").get()
        if next_page:
            yield SeleniumRequest(
                url=urljoin(response.url, next_page),
                callback=self.parse,
                wait_time=15
            )
