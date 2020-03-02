# -*- coding: utf-8 -*-
import sys
import logging
import importlib
from scrapy.crawler import CrawlerProcess
from edscrapers.scrapers.base import config
from edscrapers.scrapers.base import helpers
logger = logging.getLogger(__name__)


# Module API

def cli(argv):
    # Prepare conf dict
    conf = helpers.get_variables(config, str.isupper)

    # Get the crawler & start the scrape
    crawler = importlib.import_module(f'edscrapers.scrapers.{argv[1]}').Crawler
    scrape(conf, crawler, *argv[2:])


def scrape(conf, Crawler):
    process = CrawlerProcess(conf['SCRAPY_SETTINGS'])
    process.crawl(Crawler)
    process.start()


if __name__ == '__main__':
    cli(sys.argv)
