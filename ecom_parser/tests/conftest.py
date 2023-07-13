import os
from unittest.mock import Mock

import pytest as pytest
from scrapy import Request
from scrapy.crawler import CrawlerRunner
from scrapy.http import HtmlResponse


@pytest.fixture
def get_crawler():
    def _get_crawler(spider_class, settings=None):
        runner = CrawlerRunner(settings=settings or {})
        crawler = runner.create_crawler(spider_class)
        crawler.engine = Mock()
        return crawler

    return _get_crawler


@pytest.fixture(scope='module')
def get_response_data():
    def _get_data(test_data_dir, filename) -> str:
        with open(os.path.join(test_data_dir, filename)) as file:
            return file.read()

    return _get_data


@pytest.fixture(scope='module')
def get_response(get_response_data):
    def _get_response(test_data_dir=None, filename=None):
        request = Request(url='http://test.com')
        data = ''

        if test_data_dir is not None and filename is not None:
            data = get_response_data(test_data_dir, filename)

        return HtmlResponse(url=request.url,
                            status=200,
                            body=data.encode(),
                            encoding='utf-8',
                            request=request)

    return _get_response
