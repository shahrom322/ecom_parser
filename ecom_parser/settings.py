BOT_NAME = "ecom_parser"

SPIDER_MODULES = ["ecom_parser.spiders"]
NEWSPIDER_MODULE = "ecom_parser.spiders"

ROBOTSTXT_OBEY = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
