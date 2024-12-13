# Scrapy settings for tripcom_scraper project

BOT_NAME = "tripcom_scraper"

SPIDER_MODULES = ["tripcom_scraper.spiders"]
NEWSPIDER_MODULE = "tripcom_scraper.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "tripcom_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
#DOWNLOAD_DELAY = 3

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Enable or disable spider middlewares
#SPIDER_MIDDLEWARES = {
#    "tripcom_scraper.middlewares.TripcomScraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
#DOWNLOADER_MIDDLEWARES = {
#    "tripcom_scraper.middlewares.TripcomScraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,  # Built-in image pipeline
    'tripcom_scraper.pipelines.CustomImagesPipeline': 2,  # Custom image pipeline
    'tripcom_scraper.pipelines.TripcomScraperPipeline': 3,  # Your property database pipeline
}

# Set the directory to store images in the root directory
IMAGES_STORE = './images'  # Relative path to store images in a folder named 'images'

# Specify the field that contains the URLs of the images
IMAGES_URLS_FIELD = 'image_urls'

# Specify the field to store the paths of the downloaded images
IMAGES_RESULT_FIELD = 'image_paths'

# Enable the ImagesPipeline for image downloads
# This is the same as ITEM_PIPELINES, just mentioned here for clarity
# ITEM_PIPELINES is already configured with 'scrapy.pipelines.images.ImagesPipeline': 1

# Uncomment and configure if you want to create thumbnails for images
# IMAGES_THUMBS = {
#     'small': (50, 50),
#     'big': (270, 270),
# }

# Database URL for PostgreSQL
DATABASE_URL = "postgresql://myuser:mypassword@db:5432/tripcom_data"  # Replace with your actual database credentials
