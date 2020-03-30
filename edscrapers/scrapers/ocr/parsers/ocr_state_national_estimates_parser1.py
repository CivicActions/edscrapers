""" parser for ocr state/national estimates 2011/12, 2013/14"""

import json
import requests

import bs4 # pip install beautifulsoup4
from slugify import slugify

import edscrapers.scrapers.base.helpers as h
import edscrapers.scrapers.base.parser as base_parser
from edscrapers.scrapers.base.models import Dataset, Resource


def parse(res) -> dict:
    """ function parses content to create a dataset model """

    # create parser object
    soup_parser = bs4.BeautifulSoup(res.text, 'html5lib')

    dataset_containers = soup_parser.body.find_all(class_='accordiontitle', recursive=True)
    for container in dataset_containers:
        # create dataset model dict
        dataset = Dataset()
        dataset['source_url'] = res.url

        dataset['title'] = str(container.find(class_='accordionheader').\
                            string).strip()
        # replace all non-word characters (e.g. ?/) with '-'
        dataset['name'] = slugify(dataset['title'])
        dataset['publisher'] = ''
        dataset['notes'] = str(container.find(name='p').string).\
                                  strip()
        dataset['tags'] = ''
        dataset['date'] = ''
        dataset['contact_person_name'] = ""
        dataset['contact_person_email'] = ""
        dataset['resources'] = list()

        # add  resources from the 'container' to the dataset
        page_resource_links = container.find_all(name='a',
                                                 href=base_parser.resource_checker,
                                                 recursive=True)
        for resource_link in page_resource_links:
            resource = Resource(source_url = res.url,
                                url = resource_link['href'],
                                name = str(resource_link.string).strip())

            # get the format of the resource from the file extension of the link
            resource_format = resource_link['href']\
                            [resource_link['href'].rfind('.') + 1:]
            resource['format'] = resource_format

            # Add header information to resource object
            resource['headers'] = h.get_resource_headers(res.url, resource_link['href'])

            # add the resource to collection of resources
            dataset['resources'].append(resource)

        # if this dataset alread has data resource files look for
        # document resource files
        if len(dataset['resources']) > 0:
            yield dataset
