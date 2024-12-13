# Scrapy settings for tripcom_scraper project
from twisted.internet import epollreactor
epollreactor.install()

BOT_NAME = "tripcom_scraper"

SPIDER_MODULES = ["tripcom_scraper.spiders"]
NEWSPIDER_MODULE = "tripcom_scraper.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "tripcom_scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Remove Splash settings
# SPLASH_URL = 'http://localhost:8050'  # This is no longer needed

# Remove all the Splash middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy_playwright.middleware.PlaywrightMiddleware': 100,  # Use Playwright middleware
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,  # Default for compression
}

# Remove the Splash-aware dupefilter and cache
SPIDER_MIDDLEWARES = {
    # 'scrapy_splash.SplashDeduplicateArgsMiddleware': None,  # Remove this line
}

DUPEFILTER_CLASS = 'scrapy.dupefilters.RFPDupeFilter'  # Use default DupeFilter
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'  # Use default HTTP cache storage

# Configure item pipelines
ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,  # Built-in image pipeline
    'tripcom_scraper.pipelines.CustomImagesPipeline': 2,  # Your custom image pipeline
    'tripcom_scraper.pipelines.TripcomScraperPipeline': 3,  # Your property database pipeline
}

# Set the directory to store images in the root directory
IMAGES_STORE = './images'  # Relative path to store images in a folder named 'images'

# Specify the field that contains the URLs of the images
IMAGES_URLS_FIELD = 'image_urls'

# Specify the field to store the paths of the downloaded images
IMAGES_RESULT_FIELD = 'image_paths'

# Database URL for PostgreSQL
DATABASE_URL = "postgresql://myuser:mypassword@db:5432/tripcom_data"  # Replace with your actual database credentials

# Enable and configure AutoThrottle to prevent overwhelming the server
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False  # Disable debug info for auto-throttle

# Configure logging to help with debugging
LOG_LEVEL = 'INFO'  # Change to DEBUG for more detailed logs
LOG_FORMAT = '%(asctime)s [%(name)s] [%(levelname)s]: %(message)s'

# Configure Scrapy's maximum concurrent requests
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Set a delay for requests to prevent overloading the server (optional)
DOWNLOAD_DELAY = 2  # Adjust based on your target website's requirements

# Enable HTTP cache for faster crawling and rendering
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400  # Cache lifetime in seconds (1 day)
HTTPCACHE_DIR = 'httpcache'  # Directory to store cached responses
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504]  # Ignore server errors

# Set up retry configuration
RETRY_ENABLED = True
RETRY_TIMES = 3  # Number of retries for failed requests
RETRY_HTTP_CODES = [500, 502, 503, 504, 408]

# Configure Playwright settings
PLAYWRIGHT_LAUNCH_OPTIONS = {
    'headless': True,  # Run in headless mode, set to False if you want to see the browser
}

# Playwright browser type options
PLAYWRIGHT_BROWSER_TYPE = 'chromium'  # You can also use 'firefox' or 'webkit'

# Configure User-Agent (optional, depending on your scraping needs)
# USER_AGENT = 'tripcom_scraper (+http://www.yourdomain.com)'

# Enable extensions (optional)
# EXTENSIONS = {
#     'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Set the maximum depth for crawling (optional)
# DEPTH_LIMIT = 3

# Additional settings for PostgreSQL and PostGIS (optional)
# You may need to define SQLAlchemy settings or adjust the custom pipeline for PostGIS
