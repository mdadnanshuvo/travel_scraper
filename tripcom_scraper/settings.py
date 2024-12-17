import os

# Check if running in Docker and configure reactor accordingly
if os.environ.get('DOCKER_ENV'):
    from twisted.internet import epollreactor
    epollreactor.install()

    # Disable signal handling for the reactor to avoid the `_handleSignals` issue
    from twisted.internet import reactor
    reactor._handleSignals = lambda: None

BOT_NAME = "tripcom_scraper"

SPIDER_MODULES = ["tripcom_scraper.spiders"]
NEWSPIDER_MODULE = "tripcom_scraper.spiders"

# Other settings remain unchanged
ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800,
}

ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
    'tripcom_scraper.pipelines.CustomImagesPipeline': 2,
    'tripcom_scraper.pipelines.TripcomScraperPipeline': 3,
}

IMAGES_STORE = './images'
DATABASE_URL = "postgresql://myuser:mypassword@localhost/tripcom"

AUTOTHROTTLE_ENABLED = True
