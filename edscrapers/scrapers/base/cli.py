# -*- coding: utf-8 -*-
import sys
import logging
import importlib
from edscrapers.scrapers.base import config
from edscrapers.scrapers.base import helpers
logger = logging.getLogger(__name__)


# Module API

def cli(argv):
    # Prepare conf dict
    conf = helpers.get_variables(config, str.isupper)

    # Get and call scraper
    scrape = importlib.import_module('edscrapers.scrapers.{}'.format(argv[1])).scrape
    scrape(conf, *argv[2:])


if __name__ == '__main__':
    cli(sys.argv)
