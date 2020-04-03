# -*- coding: utf-8 -*-
import re

from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor

from edscrapers.scrapers.edgov.parser import parse
from edscrapers.scrapers.base import helpers as h


class Crawler(CrawlSpider):

    name = 'edgov'

    # allowed_regex = r'^http.*://[w2\.]*ed\.gov/.*$'
    allowed_domains = ['ed.gov', 'www2.ed.gov']

    def __init__(self):

        self.start_urls = [
            'https://www2.ed.gov/finaid/prof/resources/data/teach-institution.html',
            'https://www2.ed.gov/',
            'https://www2.ed.gov/about/offices/list/index.html'
        ]

        # Make rules
        self.rules = [
            Rule(LinkExtractor(
                #allow=self.allowed_regex,
                deny_extensions=[regex[1:] for regex in h.get_data_extensions().keys()],
                deny_domains=h.retrieve_crawlers_allowed_domains(except_crawlers=['edgov'])
                #restrict_xpaths='//*[@id="maincontent"]',
            ), callback=parse, follow=True),
        ]


        # Inherit parent
        super(Crawler, self).__init__()
