""" main parser for fsa. parser
handles branching and delication to
other parsers in the 'parsers' subpackage"""

# -*- coding: utf-8 -*-
import re
import json

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

    soup_parser = bs4.BeautifulSoup(res.text, 'html5lib')
    # check if the content contains any of the extensions
    if soup_parser.body.find(name='a', href=base_parser.resource_checker,
                             recursive=True):
        pass
    elif soup_parser.body.find(name='select', href=base_parser.resource_checker,
                               recursive=True):
        pass
    else:
        # no resource on this page, so return None
        return None
    # if code gets here, at least one resource was found

    # create parser object
    soup_parser = bs4.BeautifulSoup(res.text, 'html5lib')

    dataset_containers = soup_parser.find_all(name='body')
    # soup_parser.body.find_all(name='div', id='maincontent', recursive=True)
    for container in dataset_containers:
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

        # run both parsers, return whichever has results
        return parsers.parser1.parse(res, container, dataset) or \
            parsers.parser2.parse(res, container, dataset)


