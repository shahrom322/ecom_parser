from typing import Optional

from pydantic import BaseModel
from scrapy import Selector

from ecom_parser.spiders.apteka.utils import get_element_content

PRODUCT_NAME_CSS = 'span[itemprop=name]::text'
PRODUCT_URL_CSS = 'a[itemprop=url]::attr(href)'
PRODUCT_LOCATION_CSS = 'span[itemtype=location]::text'
PRODUCT_LEGAL_NAME_CSS = 'span[itemtype=legalName]::text'
PRODUCT_IMG_URL_CSS = 'img[itemprop=image]::attr(src)'
PRODUCT_DELIVERY_AVAILABILITY_CSS = '.ui-link__text::text'
PRODUCT_DELIVERY_DATE_CSS = 'div[class*=delivery-date] span::text'
PRODUCT_PRICE_CSS = 'meta[itemprop=price]::attr(content)'
PRODUCT_OLD_PRICE_CSS = 'span[class*=cost-old]::text'
PRODUCT_PRICE_CURRENCY_CSS = 'meta[itemprop=priceCurrency]::attr(content)'


class ProductResponseData(BaseModel):
    name: str
    url: str
    location: str
    legal_name: str
    sections: list[str]
    img_url: str
    delivery_availability: Optional[str]
    delivery_date: Optional[str]
    price: Optional[float]
    old_price: Optional[str]
    price_currency: Optional[str]

    @classmethod
    def from_html(cls, html: Selector, sections: list[str]) -> 'ProductResponseData':
        return cls(name=get_element_content(html, PRODUCT_NAME_CSS),
                   url=get_element_content(html, PRODUCT_URL_CSS),
                   location=get_element_content(html, PRODUCT_LOCATION_CSS),
                   legal_name=get_element_content(html, PRODUCT_LEGAL_NAME_CSS),
                   sections=sections,
                   img_url=get_element_content(html, PRODUCT_IMG_URL_CSS),
                   delivery_availability=get_element_content(html, PRODUCT_DELIVERY_AVAILABILITY_CSS),
                   delivery_date=get_element_content(html, PRODUCT_DELIVERY_DATE_CSS),
                   price=get_element_content(html, PRODUCT_PRICE_CSS),
                   old_price=get_element_content(html, PRODUCT_OLD_PRICE_CSS),
                   price_currency=get_element_content(html, PRODUCT_PRICE_CURRENCY_CSS))
