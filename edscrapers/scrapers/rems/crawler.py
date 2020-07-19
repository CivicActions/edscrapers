# -*- coding: utf-8 -*-
import re

from urllib.parse import urlparse, urljoin
from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor

from edscrapers.scrapers.rems.parser import parse
from edscrapers.scrapers.base import helpers as h


class Crawler(CrawlSpider):

    name = 'rems'

    #allowed_regex = r'^http.*://rems\.ed\.gov/(?!.*\(X\(1\)S).*$'
    allowed_regex = r'^http.*://rems\.ed\.gov/.*'

    #allowed_domains = ['rems.ed.gov']

    def __init__(self):

        self.start_urls = [
            'http://rems.ed.gov/',
            'https://rems.ed.gov/REMSPublications.aspx',
            'https://rems.ed.gov/#resources',
        ]

        extensions_to_avoid = []
        for ext in [h.get_data_extensions(), h.get_document_extensions(), h.get_avoidable_extensions()]:
            extensions_to_avoid.extend(ext.keys())

        # Make rules
        self.rules = [
            Rule(LinkExtractor(
                #allow_domains=self.allowed_domains,
                #allow=self.allowed_regex,
                #deny_extensions=[ext[1:] for ext in extensions_to_avoid],
                process_value=self.process_value,
                unique=True,
            ), callback=parse, follow=True,
               process_links='process_links', process_request='process_request'),
        ]

        # Inherit parent
        super(Crawler, self).__init__()

    def process_value(self, value):
        
        url = value

        if re.match(self.allowed_regex, url) is None:
            return None

        regex_search = re.search(r'\(X\(1\)S.*\)\)/', url)
        if regex_search:
            matched_str = regex_search.group()
            url = url.replace(matched_str, '')

        url_parsed = urlparse(url)
        url = urljoin(url, url_parsed.path) 
        
        return url

    def process_links(self, links):
        filtered = []
        for link in links:
            url = self.process_value(link.url)
            if url:
                link.url = url
                filtered.append(link)
        return filtered

    def process_request(self, request):

        url = request.url
        url = self.process_value(url)
        if url:
            request = request.replace(url=url)

        return request

    


