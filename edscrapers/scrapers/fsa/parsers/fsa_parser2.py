""" parser for fsa pages """

import re

import bs4 # pip install beautifulsoup4
from slugify import slugify

import edscrapers.scrapers.base.helpers as h
import edscrapers.scrapers.base.parser as base_parser
from edscrapers.scrapers.base.models import Dataset, Resource


def parse(res, container, dataset) -> dict:
    """ function parses content to create a dataset model """

    # add  resources from the 'container' to the dataset
    page_resource_links = container.find_all(name='option',
                                                recursive=True)
    for resource_link in page_resource_links:
        resource = Resource(source_url=res.url,
                            url=resource_link['value'])
        # get the resource name
        resource['name'] = str(resource_link.text).strip()

        # get the format of the resource from the file extension of the link
        resource_format = resource_link['value']\
                        [resource_link['value'].rfind('.') + 1:]
        resource['format'] = resource_format

        # Add header information to resource object
        resource['headers'] = h.get_resource_headers(res.url, resource_link['value'])

        # add the resource to collection of resources
        dataset['resources'].append(resource)

    yield dataset
