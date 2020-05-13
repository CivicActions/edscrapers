""" parser for ocr state/national estimates 2009/10,
2006,2004,2002 """

import json

import requests

import bs4 # pip install beautifulsoup4
from slugify import slugify

import edscrapers.scrapers.base.helpers as h
import edscrapers.scrapers.base.parser as base_parser
from edscrapers.scrapers.base.models import Dataset, Resource, Collection, Source



def parse(res) -> dict:
    """ function parses content to create a dataset model """

    # create parser object
    soup_parser = bs4.BeautifulSoup(res.text, 'html5lib')

    dataset_containers = soup_parser.body.find_all(id='maincontent',
                                                   recursive=True)
    
    # check if this page is a collection (i.e. collection of datasets)
    if len(dataset_containers) > 0: # this is a collection
        # create the collection (with a source)
        collection = h.extract_dataset_collection_from_url(collection_url=res.url,
                                        namespace="all",
                                        source_url=\
                                        str(res.request.headers.get(str(b'Referer',
                                                                    encoding='utf-8'), b''), 
                                            encoding='utf-8'))

    for container in dataset_containers:
        # create dataset model dict
        dataset = Dataset()
        dataset['source_url'] = res.url
        if dict(enumerate(container.find('div').find_all('div'))).get(0) is None:
            # get the first available div element
            dataset['title'] = str(container.find(name='div').\
                                string).strip()
        else:
            # get the 1st div element from the first avaialble div
            dataset['title'] = str(container.find('div').find_all('div')[0].\
                                    string).strip()
                                    
        if dataset['title'] is None or dataset['title'] == '':
            dataset['title'] = str(soup_parser.head.\
                                find(name='title').string).strip()
        # replace all non-word characters (e.g. ?/) with '-'
        dataset['name'] = slugify(dataset['title'])
        # get publisher from parent package name
        dataset['publisher'] = __package__.split('.')[-2]
        if container.select_one('p') is not None:
            # get the first available p element
            dataset['notes'] = str(container.select_one('p').string).\
                                  strip()
        elif dict(enumerate(container.find_all('div'))).get(1) is not None:
            # get the 2nd div element
            dataset['notes'] = str(container.find_all('div')[1].\
                                    string).strip()
        else:
            # get the 2nd div element from the 1st avialble div element
            dataset['notes'] = str(container.\
                                    find('div').find_all('div')[1].\
                                    string).strip()
        # if no notes/description still not available (after best efforts),
        # default to dataset title
        if dataset['notes'] is None or dataset['notes'] == '':
            dataset['notes'] = dataset['title']

        dataset['tags'] = ''
        dataset['date'] = ''
        dataset['contact_person_name'] = ""
        dataset['contact_person_email'] = ""

        # specify the collection which the dataset belongs to
        if collection: # if collection exist
            dataset['collection'] = collection
            
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
