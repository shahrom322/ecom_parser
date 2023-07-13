import os

from ecom_parser.models.product import ProductData, AssetsData, StockData, PriceData

BASE_DIR = os.path.dirname(__file__)
BASE_FEEDS_URI = os.path.join(BASE_DIR, 'data')

ZENROW_API_KEY = os.getenv('ZENROW_API_KEY')
ZENROW_PROXY = f'http://{ZENROW_API_KEY}:@original_status=true@proxy.zenrows.com:8001'

BOT_NAME = "ecom_parser"

SPIDER_MODULES = ["ecom_parser.spiders"]
NEWSPIDER_MODULE = "ecom_parser.spiders"

ROBOTSTXT_OBEY = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

FEEDS = {
    f'{BASE_FEEDS_URI}/products.json': {
        'format': 'json',
        'overwrite': False,
        'item_classes': [ProductData, AssetsData, StockData, PriceData]
    }
}
