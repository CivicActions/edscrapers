""" main parser for edgov. parser
handles branching and delication to
other parsers in the 'parsers' subpackage"""

# -*- coding: utf-8 -*-
import re
import json
import importlib

import bs4

from edscrapers.scrapers import base
import edscrapers.scrapers.base.parser as base_parser
from edscrapers.scrapers.edgov import parsers, offices_map
from edscrapers.scrapers.base.models import Publisher

edgov_parsers = ['octae', 'oela', 'oese', 'ope', 'opepd', 'osers']

def parse(res):
    """ function parses content to create a dataset model
    or return None if no resource in content"""

    soup_parser = bs4.BeautifulSoup(res.text, 'html5lib')

    try:
        office = soup_parser.head.find(name='meta', attrs={'name': 'DC.office'})['content']
    except:
        office = None

    publisher = Publisher()
    publisher['name'] = 'edgov'
    publisher['subOrganizationOf'] = None

    if office:
        if office in offices_map.keys():
            publisher['name'] = offices_map[office]['name']
            publisher['subOrganizationOf'] = offices_map[office]['subOrganizationOf']
        if publisher['name'] in edgov_parsers:
            name = office
            parser = importlib.import_module(f'edscrapers.scrapers.edgov.{office}').parser
            return parser.parse(res, publisher)

    # check if the content contains any of the extensions
    if soup_parser.body.find(name='a', href=base_parser.resource_checker,
                             recursive=True) is None:
        # no resource on this page, so return None
        return None
    # if code gets here, at least one resource was found
    
    # check if the parser is working on EDGOV web page
    if soup_parser.body.find(name='div', recursive=True) is not None:
        # parse the page with the parser and return result
        return parsers.parser1.parse(res, publisher)
    else:
        return None


    


