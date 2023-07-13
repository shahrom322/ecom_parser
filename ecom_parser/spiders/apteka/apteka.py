import csv
from logging import getLogger
from typing import Iterator, Union

from scrapy import Spider, Request
from scrapy.http import HtmlResponse

from ecom_parser.models.product import ProductData
from ecom_parser.settings import ZENROW_PROXY
from ecom_parser.spiders.apteka.serializers import ProductResponseData

logger = getLogger(__name__)

TARGET_CATEGORIES_FILENAME = 'categories.csv'
PRODUCTS_LIST_CSS = 'div[itemtype$=Product]'
IS_LAST_PRODUCTS_PAGE_CSS = 'li[class$=item_next] a[class$=link_disabled]'
NEXT_PAGE_URL_CSS = 'li[class$=item_next] a::attr(href)'
PRODUCT_SECTIONS_LIST_CSS = 'li[itemprop=itemListElement] a span span::text'


class AptekaSpider(Spider):
    name = 'apteka'

    default_cookies = {'city': '92'}  # Дефолтное значение для региона - Томск
    default_meta = {'proxy': ZENROW_PROXY}

    root_url = 'https://apteka-ot-sklada.ru'

    def start_requests(self) -> Iterator[Request]:
        with open(TARGET_CATEGORIES_FILENAME) as file:
            for (category_url,) in csv.reader(file):
                yield self.request_category(category_url)

    def request_category(self, url: str) -> Request:
        return Request(url=url,
                       callback=self.parse_category,
                       cookies=self.default_cookies,
                       meta=self.default_meta)

    def parse_category(self, response: HtmlResponse) -> Iterator[Union[ProductData, Request]]:
        sections = [section.strip()
                    for section in response.css(PRODUCT_SECTIONS_LIST_CSS).getall()]
        response_products_data = [ProductResponseData.from_html(div, sections)
                                  for div in response.css(PRODUCTS_LIST_CSS)]
        for product_data in response_products_data:
            yield ProductData.create(product_data)

        if not self.is_last_products_page_received(response):
            next_page_url = f'{self.root_url}/{response.css(NEXT_PAGE_URL_CSS).get()}'
            assert next_page_url is not None
            yield self.request_category(next_page_url)

    @staticmethod
    def is_last_products_page_received(response: HtmlResponse) -> bool:
        return bool(response.css(IS_LAST_PRODUCTS_PAGE_CSS).get())
