# -*- coding: utf-8 -*-
import re

from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor

from edscrapers.scrapers.edgov.parser import parse
from edscrapers.scrapers.base import helpers as h

import json
import requests
from pathlib import Path
import os


class Crawler(CrawlSpider):

    name = 'edgov'

    # get the output path for comparison work
    comparison_output_path = Path(os.getenv('ED_OUTPUT_PATH'), "ed_comparison")
    # make the path
    comparison_output_path.mkdir(parents=True, exist_ok=True)

    # allowed_regex = r'^http.*://[w2\.]*ed\.gov/.*$'
    allowed_domains = ['ed.gov', 'www2.ed.gov']

    def __init__(self):

        self.load_ed_gov_json()

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
                #deny_domains=h.retrieve_crawlers_allowed_domains(except_crawlers=['edgov'])
                #restrict_xpaths='//*[@id="maincontent"]',
            ), callback=parse, follow=True, 
               cb_kwargs={'distribution_list': self.dataset_distributions_list}),
        ]


        # Inherit parent
        super(Crawler, self).__init__()
    
    @classmethod
    def load_ed_gov_json(cls):
        
        req = requests.get("https://www2.ed.gov/data.json", verify=False)

        # dump the returned datajson to a file
        with open(Path(cls.comparison_output_path, "ed_data.json"), 'w') as file:
            json.dump(req.json(), file, indent=2, sort_keys=False)
        
        # add the returned json object to the class
        cls.ed_json = req.json()
        
        # create the list of dataset distributions from the edgov datajson
        cls.reduce_datasets_distributions()
    
    @classmethod
    def reduce_datasets_distributions(cls):
        
        distributions_list = []
        if not cls.ed_json:
            raise AttributeError("class attribute 'ed_json' does not exist")

        for dataset in cls.ed_json['dataset']:
            distributions_list.extend(dataset.get('distribution', []))
        
        cls.dataset_distributions_list = distributions_list

        with open(Path(cls.comparison_output_path, "ed_distributions.json"), 'w') as file:
            json.dump(cls.dataset_distributions_list, file, indent=2, sort_keys=False)
            
