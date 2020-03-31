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
    page_resource_links = container.find_all(name='a',
                                                href=base_parser.resource_checker,
                                                recursive=True)
    for resource_link in page_resource_links:
        resource = Resource(source_url=res.url, url=resource_link['href'])
        # get the resource name iteratively
        for child in resource_link.parent.children:
            if resource_link.parent.name == 'td':
                resource['name'] = str(resource_link.find_parent(name='tr').contents[1]).strip()
            else:
                resource['name'] = str(child).strip()
            if re.sub(r'(<.+>)', '',
            re.sub(r'(</.+>)', '', resource['name'])) != "":
                break
        resource['name'] = re.sub(r'(</.+>)', '', resource['name'])
        resource['name'] = re.sub(r'(<.+>)', '', resource['name'])

        if resource_link.parent.parent.find(name=True):

            # concatenate the text content of parents with 
            # class 'headersLevel1' & 'headersLevel2'
            resource['description'] = str(resource_link.parent.parent.find(name=True)).strip() +\
                                        " - " + str(resource['name']).strip()
            resource['description'] = re.sub(r'(</.+>)', '', resource['description'])
            resource['description'] = re.sub(r'(<.+>)', '', resource['description'])
        else:
            # concatenate the text content of parents with
            # class 'headersLevel1' & 'contentText'
            resource['description'] = str(resource['name']).strip()
            resource['description'] = re.sub(r'(</.+>)', '', resource['description'])
            resource['description'] = re.sub(r'(<.+>)', '', resource['description'])

        # get the format of the resource from the file extension of the link
        resource_format = resource_link['href']\
                        [resource_link['href'].rfind('.') + 1:]
        resource['format'] = resource_format

        # Add header information to resource object
        resource['headers'] = h.get_resource_headers(res.url, resource_link['href'])

        # add the resource to collection of resources
        dataset['resources'].append(resource)

    yield dataset
