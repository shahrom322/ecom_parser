import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ecom_parser.spiders.apteka.serializers import ProductResponseData

NUMBER_PATTERN = re.compile(r'(\d+(?:\.\d+)?)')


@dataclass
class PriceData:
    current: float
    original: float
    sale_tag: Optional[str]

    @classmethod
    def create(cls, price: float, old_price: Optional[str]) -> 'PriceData':
        sale_tag = None
        if old_price is not None:
            cleaned_old_price = float(old_price.split()[0])
            sale_tag = cleaned_old_price - price

        return cls(current=price,
                   original=old_price if old_price else price,
                   sale_tag=f'Скидка {sale_tag}%' if sale_tag else None)


@dataclass
class StockData:
    in_stock: bool
    count: int

    @classmethod
    def create(cls, delivery_availability: Optional[str]) -> 'StockData':
        count = None
        if delivery_availability is not None:
            count = NUMBER_PATTERN.search(delivery_availability).group(1)

        return cls(in_stock=bool(delivery_availability),
                   count=count or 0)


@dataclass
class AssetsData:
    main_image: str
    set_images: Optional[list[str]] = None
    view360: Optional[list[str]] = None
    video: Optional[list[str]] = None

    @classmethod
    def create(cls, image_url: str) -> 'AssetsData':
        return cls(main_image=image_url)


@dataclass
class ProductData:
    timestamp: datetime
    url: str
    title: str
    brand: str
    section: list[str]
    price_data: PriceData
    stock: StockData
    assets: AssetsData

    @classmethod
    def create(cls, response_data: ProductResponseData) -> 'ProductData':
        price_data = PriceData.create(response_data.price, response_data.old_price)
        stock_data = StockData.create(response_data.delivery_availability)
        assets_data = AssetsData.create(response_data.img_url)
        return cls(timestamp=datetime.now(),
                   url=response_data.url,
                   title=response_data.name,
                   brand=response_data.legal_name,
                   section=response_data.sections,
                   price_data=price_data,
                   stock=stock_data,
                   assets=assets_data)
