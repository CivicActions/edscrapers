# -*- coding: utf-8 -*-
import re

from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor

from edscrapers.scrapers.edgov.parser import parse
from edscrapers.scrapers.base import helpers as h


class Crawler(CrawlSpider):

    name = 'edgov'

    allowed_regex = r'ed.gov'

    def __init__(self):

        self.start_urls = [
            'https://www2.ed.gov/finaid/prof/resources/data/teach-institution.html',
            'https://www2.ed.gov/',
            'https://www2.ed.gov/about/offices/list/index.html'
        ]

        # Make rules
        self.rules = [
            Rule(LinkExtractor(
                allow='^http.*://.*\.ed\.gov/.*$',
                # deny=f'.*({"|".join(h.get_data_extensions())})',
                restrict_xpaths='//*[@id="maincontent"]'
                # process_value=lambda value: value.replace('http', 'https', 1),
            ), callback=parse, follow=True),
        ]


        # Inherit parent
        super(Crawler, self).__init__()
