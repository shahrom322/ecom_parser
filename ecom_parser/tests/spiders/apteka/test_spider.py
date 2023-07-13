import os

import pytest
from scrapy import Request

from ecom_parser.models.product import ProductData
from ecom_parser.settings import BASE_DIR
from ecom_parser.spiders.apteka.apteka import AptekaSpider

APTEKA_TEST_RESPONSES_DIR = os.path.join(BASE_DIR, 'tests', 'spiders', 'apteka', 'responses')


@pytest.fixture
def spider(get_crawler):
    crawler = get_crawler(AptekaSpider)
    return AptekaSpider.from_crawler(crawler)


def test_request_category(spider):
    test_url = 'https://test.com'
    request = spider.request_category(test_url)

    assert isinstance(request, Request)
    assert request.url == test_url
    assert request.callback == spider.parse_category
    assert request.cookies == spider.default_cookies
    assert request.meta == spider.default_meta


def test_parse_category_if_more_page_exist(spider, get_response):
    response = get_response(APTEKA_TEST_RESPONSES_DIR, 'first_page_products_list_response.html')
    results = [*spider.parse_category(response)]

    assert len(results) == 13
    assert isinstance(results[-1], Request)
    assert all([isinstance(obj, ProductData) for obj in results[:-1]])


def test_parse_category_if_last_page_received(spider, get_response):
    response = get_response(APTEKA_TEST_RESPONSES_DIR, 'last_page_products_list_response.html')
    results = [*spider.parse_category(response)]

    assert len(results) == 8
    assert all([isinstance(obj, ProductData) for obj in results])


@pytest.mark.parametrize('response_file, expected_result',
                         [('first_page_products_list_response.html', False),
                          ('last_page_products_list_response.html', True)])
def is_last_products_page_received(spider, get_response, response_file, expected_result):
    response = get_response(APTEKA_TEST_RESPONSES_DIR, response_file)
    assert spider.is_last_products_page_received(response) is expected_result
