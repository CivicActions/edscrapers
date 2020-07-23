# -*- coding: utf-8 -*-
import re

from urllib.parse import urlparse, urlunparse, urljoin
from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor

from edscrapers.scrapers.dashboard.parser import parse
from edscrapers.scrapers.base import helpers as h


class Crawler(CrawlSpider):

    name = 'dashboard'

    allowed_regex = r'^http.*://dashboard\.ed\.gov/.*$'
    # allowed_domains = ['ed.gov', 'www2.ed.gov']

    def __init__(self):

        self.start_urls = [
            'https://dashboard.ed.gov/',
        ]

        extensions_to_avoid = []
        for ext in [h.get_data_extensions(), h.get_document_extensions(), h.get_avoidable_extensions()]:
            extensions_to_avoid.extend(ext.keys())

        # Make rules
        self.rules = [
            Rule(LinkExtractor(
                allow=self.allowed_regex,
                deny_extensions=[ext[1:] for ext in extensions_to_avoid],
                process_value=self.process_value,
                unique=True,
                deny_domains=h.retrieve_crawlers_allowed_domains(except_crawlers=['edgov'])
            ), callback=parse, follow=True),
        ]


        # Inherit parent
        super(Crawler, self).__init__()

    def process_value(self, value):
        
        url = value

        if re.match(self.allowed_regex, url) is None:
            return None

        url_parsed = urlparse(url)
        query = url_parsed.query

        regex = r'&id=\d{1,3}&wt=\d{1,3}'
        search = re.search(regex, query)
        if search:
            query = query.replace(search.group(), '')
            url_parsed = url_parsed._replace(query=query)
            url = urlunparse(url_parsed)

        return url
