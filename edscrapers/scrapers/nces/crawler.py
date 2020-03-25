# -*- coding: utf-8 -*-
import re

from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor

from edscrapers.scrapers.nces.parser import parse
from edscrapers.scrapers.base import helpers as h


class Crawler(CrawlSpider):

    name = 'nces'

    allowed_regex = r'(nces|ies)\.ed\.gov'
    allowed_domains = ['nces.ed.gov','ies.ed.gov']

    def __init__(self):

        self.start_urls = [
            'https://nces.ed.gov/datatools/',
            'https://ies.ed.gov/data.asp',
            'https://nces.ed.gov/pubsearch/index.asp?PubSectionID=1&HasSearched=1&pubspagenum=1&sort=3&order=0&L1=&L2=&searchstring=&searchtype=AND&searchcat2=&searchcat=title&pagesize=15&searchmonth=3&searchyear=2018&datetype=ge&pubtype=010&surveyname=&surveyid=&centername=NCES&center=NCES',
            'https://nces.ed.gov/Datalab/TablesLibrary',
            #'https://nces.ed.gov/pubs2009/expenditures/tables/table_08.asp?referrer=report'
            #'https://nces.ed.gov/surveys/els2002/tables/APexams_01.asp'
            #'https://nces.ed.gov/ipeds/deltacostproject/'
            #'https://nces.ed.gov/pubs2009/expenditures/tables.asp'
        ]

        # Make rules
        self.rules = [
            Rule(LinkExtractor(
                allow=self.allowed_regex,
                deny=["\\" + regex for regex in h.get_data_extensions().keys()],
                # restrict_xpaths='//*[@id="maincontent"]'
                # process_value=lambda value: value.replace('http', 'https', 1),
            ), callback=parse, follow=True),
        ]


        # Inherit parent
        super(Crawler, self).__init__()
