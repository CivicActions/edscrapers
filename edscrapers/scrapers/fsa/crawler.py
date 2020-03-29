# -*- coding: utf-8 -*-
import re

from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor

from edscrapers.scrapers.fsa.parser import parse
from edscrapers.scrapers.base import helpers as h


class Crawler(CrawlSpider):

    name = 'fsa'

    allowed_regex = r'https://studentaid.gov/.*$'

    def __init__(self):

        self.start_urls = [
            'https://studentaid.gov/',
            'https://studentaid.gov/data-center',
            'https://studentaid.gov/data-center/student/application-volume/fafsa-school-state'
        ]

        # Make rules
        self.rules = [
            Rule(LinkExtractor(
                allow=self.allowed_regex,
            ), callback=parse, follow=True),
        ]


        # Inherit parent
        super(Crawler, self).__init__()
