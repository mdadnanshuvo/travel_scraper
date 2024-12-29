import scrapy
import json
import re
from tripcom_scraper.items import TripcomItem

class TripcomSpider(scrapy.Spider):
    name = "tripcom_spider"
    allowed_domains = ["uk.trip.com"]
    start_urls = [
        "https://uk.trip.com/hotels/?locale=en-GB"
    ]

    def parse(self, response):
        print("\n--- Parsing the initial page to find city data... ---\n")

        # Extract the script containing JSON data
        json_script = response.xpath(
            "//script[contains(text(), 'window.IBU_HOTEL')]/text()"
        ).get()

        if json_script:
            print("Script containing city data found. Extracting JSON...")

            match = re.search(r"window\.IBU_HOTEL\s*=\s*(\{.*?\});", json_script, re.DOTALL)
            if match:
                try:
                    # Parse JSON data
                    data = json.loads(match.group(1))

                    # Extract inbound and outbound cities
                    htls_data = data.get("initData", {}).get("htlsData", {})
                    inbound_cities = htls_data.get("inboundCities", [])
                    outbound_cities = htls_data.get("outboundCities", [])

                    print(f"Total Inbound Cities: {len(inbound_cities)}, Outbound Cities: {len(outbound_cities)}\n")

                    # Process each inbound city one by one
                    for city in inbound_cities:
                        city_id = city.get("id", "")
                        city_name = city.get("name", "Unknown City")

                        print(f"Processing City: {city_name} (ID: {city_id})\n")

                        city_url = f"https://uk.trip.com/hotels/list?city={city_id}"
                        print(f"Fetching hotels for city '{city_name}' using URL: {city_url}\n")

                        yield scrapy.Request(
                            url=city_url,
                            callback=self.parse_hotels,
                            meta={'city_id': city_id, 'city_name': city_name}
                        )
                except Exception as e:
                    print(f"Error parsing JSON data: {e}")
            else:
                print("No JSON data matched with regex.")
        else:
            print("No script tag containing 'window.IBU_HOTEL' found.")

    def parse_hotels(self, response):
        city_id = response.meta['city_id']
        city_name = response.meta['city_name']

        print(f"\n--- Fetching hotels for city '{city_name}'... ---\n")

        # Extract the script containing JSON hotel data
        json_script = response.xpath(
            "//script[contains(text(), 'window.IBU_HOTEL')]/text()"
        ).get()

        if json_script:
            match = re.search(r"window\.IBU_HOTEL\s*=\s*(\{.*?\});", json_script, re.DOTALL)
            if match:
                try:
                    # Parse JSON data
                    data = json.loads(match.group(1))
                    hotels = data.get("initData", {}).get("firstPageList", {}).get("hotelList", [])

                    print(f"Found {len(hotels)} hotels for city '{city_name}'.\n")

                    for hotel in hotels:
                        item = TripcomItem()
                        item["hotelName"] = hotel.get("hotelBasicInfo", {}).get("hotelName", "")
                        item["rating"] = hotel.get("commentInfo", {}).get("commentScore", "")
                        item["location"] = hotel.get("positionInfo", {}).get("positionName", "")
                        item["latitude"] = hotel.get("positionInfo", {}).get("coordinate", {}).get("lat", "")
                        item["longitude"] = hotel.get("positionInfo", {}).get("coordinate", {}).get("lng", "")
                        item["roomName"] = hotel.get("roomInfo", {}).get("physicalRoomName", "")
                        item["price"] = hotel.get("hotelBasicInfo", {}).get("price", "")
                        item["imageUrl"] = hotel.get("hotelBasicInfo", {}).get("hotelImg", "")
                        item["city_id"] = city_id
                        yield item

                        print(f"Hotel: {item['hotelName']}")
                        print(f"Price: {item['price']}, Rating: {item['rating']}")
                        print(f"Location: {item['location']}")
                        print(f"Coordinates: ({item['latitude']}, {item['longitude']})")
                        print(f"Image URL: {item['imageUrl']}\n")

                except Exception as e:
                    print(f"Error parsing hotel data JSON: {e}")
            else:
                print("No JSON data matched with regex.")
        else:
            print("No hotel data script tag found.")
