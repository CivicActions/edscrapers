""" main parser for edoctae. parser
handlers branching and delication to
other parsers in the 'parsers' subpackage"""

# -*- coding: utf-8 -*-
import re
import json

import bs4

from edscrapers.scrapers import base
import edscrapers.scrapers.base.parser as base_parser
from edscrapers.scrapers.edoctae import parsers

# contains list of data resources to exclude from dataset
deny_list = []

def parse(res):
    """ function parses content to create a dataset model
    or return None if no resource in content"""

    soup_parser = bs4.BeautifulSoup(res.text, 'html5lib')
    # check if the content contains any of the extensions
    if soup_parser.body.find(name='a', href=base_parser.resource_checker,
                             recursive=True) is None:
        # no resource on this page, so return None
        print('URL', 'NONE', res.url)
        return None

    # if code gets here, at least one resource was found
    
    # check if the parser is working on OCTAE web page
    if soup_parser.body.find(name='div', id='maincontent', recursive=True) is not None:
        # parse the page with the parser and return result
        print('URL', 'PARSER1', res.url)
        return parsers.parser1.parse(res)
    # check if the parser is working on OCR State & National Estimations (variant 2)
    if soup_parser.body.select_one('#container2 #maincontent') is not None:
        # parse the page with the parser and return result
        print('URL', 'PARSER2', res.url)
        return parsers.parser2.parse(res)
    else:
        print('URL', 'NONE2', res.url)
        return None


    


