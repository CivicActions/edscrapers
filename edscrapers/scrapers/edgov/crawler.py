# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from edscrapers.scrapers.edgov.parser import parse
import re


class Crawler(CrawlSpider):

    name = 'edgov'

    # allowed_domains = [
    #     'www2.ed.gov',
    # ]
    allowed_regex = r'ed.gov'
    # depth = 10

    def __init__(self, conf=None):

        self.conf = conf

        self.start_urls = [
            # 'https://www2.ed.gov/finaid/prof/resources/data/teach-institution.html',
            'https://www2.ed.gov/',
        ]

        # Make rules
        self.rules = [
            Rule(LinkExtractor(
                allow='^http.*://.*\.ed\.gov/.*$',
                deny='.*(xls|xlsx|csv|zip|pdf|doc|docx)',
                restrict_xpaths='//*[@id="maincontent"]'
                # process_value=lambda value: value.replace('http', 'https', 1),
            ), callback=parse, follow=True),
        ]


        # Inherit parent
        super(Crawler, self).__init__()
