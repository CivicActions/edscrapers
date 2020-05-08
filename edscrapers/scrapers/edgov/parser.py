""" main parser for edgov. parser
handles branching and delication to
other parsers in the 'parsers' subpackage"""

# -*- coding: utf-8 -*-
import re
import json

import bs4

from edscrapers.scrapers import base
import edscrapers.scrapers.base.parser as base_parser
from edscrapers.scrapers.edgov import parsers
from edscrapers.scrapers.base.models import Dataset, Resource
from slugify import slugify

import urllib.parse

class Distribution():

    def __init__(self, distributions_list, source_url):
        self.distributions_list = distributions_list
        self.source_url = source_url
    
    def resource_checker(self, tag_attr: str):
        """ function is used as a filter for BeautifulSoup to
        locate resource links """

        if tag_attr != '' or tag_attr is None:
            return False

        if urllib.parse.urlparse(tag_attr).scheme:
            href = tag_attr
        else:
            href = urllib.parse.urljoin(self.source_url, tag_attr)
        
        for distribution_json in self.distributions_list:
            if href.lower() == distribution_json.get('downloadURL', '').lower():
                return True
        return False



def parse(res, distribution_list):
    """ function parses content to create a dataset model
    or return None if no resource in content"""

    # ensure that the response text gotten is a string
    if not isinstance(getattr(res, 'text', None), str):
        return None

    try:
        soup_parser = bs4.BeautifulSoup(res.text, 'html5lib')
    except:
        return None
    
    # create a Distribution class
    distribution = Distribution(distribution_list, res.url)

    # check if any resource on this page matches the urls in distribution list
    resource_list = soup_parser.body.find_all(name='a', href=distribution.resource_checker, recursive=True)

    for resource in resource_list:
        dataset = Dataset()
        # create dataset model dict
        dataset = Dataset()
        dataset['source_url'] = res.url

        dataset['title'] = str(soup_parser.head.\
                                find(name='title').string).strip()

        # replace all non-word characters (e.g. ?/) with '-'
        dataset['name'] = slugify(dataset['title'])

        dataset['resource_url'] = resource['href']

        yield dataset

    


