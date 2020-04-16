""" main parser for fsa. parser
handles branching and delication to
other parsers in the 'parsers' subpackage"""

# -*- coding: utf-8 -*-
import re
import json
from urllib.parse import urlparse
from urllib.parse import urljoin

import bs4
from dateutil import parser
from slugify import slugify

from edscrapers.cli import logger
import edscrapers.scrapers.base.helpers as h
from edscrapers.scrapers import base
import edscrapers.scrapers.base.parser as base_parser
from edscrapers.scrapers.fsa import parsers
from edscrapers.scrapers.base.models import Dataset


def parse(res):
    """ function parses content to create a dataset model
    or return None if no resource in content"""

    # ensure that the response text gotten is a string
    if not isinstance(getattr(res, 'text', None), str):
        return None

    try:
        soup_parser = bs4.BeautifulSoup(res.text, 'html5lib')
    except:
        return None

    # check if the content contains any of the extensions
    if soup_parser.body.find(name='a', href=base_parser.resource_checker,
                             recursive=True):
        pass
    elif soup_parser.body.find(name='select', recursive=True):
        pass
    else:
        # no resource on this page, so return None
        return None
    # if code gets here, at least one resource was found

    # create parser object
    soup_parser = bs4.BeautifulSoup(res.text, 'html5lib')

    # create dataset model dict
    dataset = Dataset()
    dataset['source_url'] = res.url

    dataset['title'] = h.get_meta_value(soup_parser, 'og:title') or \
        str(soup_parser.head.find(name='title').string).strip()

    # replace all non-word characters (e.g. ?/) with '-'
    # also remove site title from the page title
    dataset['name'] = slugify(dataset['title'].split('|')[0])

    dataset['publisher'] = h.get_meta_value(soup_parser, 'og:site_name') or \
        __package__.split('.')[-1]

    dataset['notes'] = h.get_meta_value(soup_parser, 'og:description') or \
        h.get_meta_value(soup_parser, 'description') or ''

    dataset['date'] = h.get_meta_value(soup_parser, 'article:published_time') or \
        h.get_meta_value(soup_parser, 'article:modified_time') or \
        h.get_meta_value(soup_parser, 'og:updated_time') or ''
    if dataset['date']:
        dataset['date'] = parser.parse(dataset['date']).strftime('%Y-%m-%d')

    dataset['contact_person_name'] = ''
    dataset['contact_person_email'] = ''

    dataset['resources'] = list()

    # get option tags that have 'value' attribute linking to a resource file
    option_tags = soup_parser.find_all(name='option',
                                       value=base_parser.resource_checker,
                                       recursive=True)

    for option_tag in option_tags:

        option_value = option_tag['value']
        # if it has options with URLs as values, then engage parser2
        if option_value.startswith(('http', '../', './', '/')):
            return parsers.parser2.parse(res, soup_parser, dataset)

    # run parser1, since parser2 was not activated until this point
    return parsers.parser1.parse(res, soup_parser, dataset)

