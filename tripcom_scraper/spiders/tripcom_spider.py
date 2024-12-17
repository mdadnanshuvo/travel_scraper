import scrapy
from scrapy_selenium import SeleniumRequest
from tripcom_scraper.items import TripcomScraperItem  # Assuming this exists
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
                wait_time=20,  # Wait for JS to load
                dont_filter=True
            )

    def parse(self, response):
        item = TripcomScraperItem()

        # Hotel Title
        item['title'] = response.css("h1.headInit_headInit-title_nameA__EE_LB::text").get(default='').strip()
        
        # Location
        item['location'] = response.css(".headInit_headInit-address_text__D_Atv::text").get(default='').strip()
        
        # Rating
        item['rating'] = response.css("em.reviewTop_reviewTop-score__FpKsA::text").get(default='').strip()

        # Fetching Room Types and Prices
        rooms = []
        for room in response.css(".commonRoomCard__BpNjl"):
            room_type = room.css(".commonRoomCard-title__iYBn2::text").get(default='').strip()
            price = room.css(".saleRoomItemBox-priceBox-displayPrice__gWiOr span::text").get(default='').strip()
            if room_type and price:
                rooms.append({
                    'room_type': room_type,
                    'price': price
                })
        item['room_type'] = rooms

        # Extract Main Price
        item['price'] = response.css("span.priceBox_priceBox-container_realPrice__4VuNW::text").get(default='').strip()

        # Image URLs
        image_urls = response.css(".headAlbum_headAlbum_img__vfjQm::attr(src)").getall()
        item['image_urls'] = [urljoin(response.url, url) for url in image_urls if url]

        # Latitude and Longitude Parsing
        map_marker = response.css("div[id^='map-list-']::attr(id)").get()
        if map_marker:
            try:
                coords = map_marker.replace("map-list-", "").split('.')
                if len(coords) >= 4:
                    item['latitude'] = f"{coords[0]}.{coords[1]}"
                    item['longitude'] = f"{coords[2]}.{coords[3]}"
                else:
                    raise ValueError("Invalid map marker format.")
            except Exception as e:
                self.logger.warning(f"Error parsing coordinates: {e}")
                item['latitude'] = ''
                item['longitude'] = ''
        else:
            self.logger.warning("Map marker not found.")
            item['latitude'] = ''
            item['longitude'] = ''

        # Log Extracted Data for Debugging
        self.logger.info(f"Extracted Data: {item}")
        yield item

        # Handle Pagination
        next_page = response.css("a.pagination-next::attr(href)").get()
        if next_page:
            yield SeleniumRequest(
                url=urljoin(response.url, next_page),
                callback=self.parse,
                wait_time=15
            )
