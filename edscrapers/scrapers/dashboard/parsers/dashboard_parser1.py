""" parser for dashboard tables """

import re
import requests

import bs4 # pip install beautifulsoup4
from slugify import slugify

import edscrapers.scrapers.base.helpers as h
import edscrapers.scrapers.base.parser as base_parser
from edscrapers.scrapers.base.models import Dataset, Resource


def parse(res, publisher) -> dict:
    """ function parses content to create a dataset model """

    # create parser object
    soup_parser = bs4.BeautifulSoup(res.text, 'html5lib')

    dataset_containers = soup_parser.find_all(name='body')
    
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

        dataset['title'] = soup_parser.select(
            'div.MainContent > div.IndicatorList > h4 > a'
        )[0].string


        # replace all non-word characters (e.g. ?/) with '-'
        dataset['name'] = slugify(dataset['title'])
        dataset['publisher'] = publisher
        
        dataset['notes'] = dataset['title']

        if soup_parser.find(name='div', attrs={'class': 'ReportSource'}):
            report_source = soup_parser.find(name='div', attrs={'class': 'ReportSource'})
            dataset['notes'] = f"{dataset['notes']}<br>\n{report_source.string}"

        if 'statedetail.aspx' in res.url:
            dataset['notes'] = f"{dataset['notes']}<br>\n<a href='{res.url.replace('statedetail', 'moreinfo')}'>More Info</a>"

        if soup_parser.head.find(name='meta', attrs={'name': 'keywords'}) is None:
            dataset['tags'] = ''
        else:
            dataset['tags'] = soup_parser.head.\
                                find(name='meta', attrs={'name': 'keywords'})['content']
    
        if soup_parser.head.find(name='meta', attrs={'name': 'DC.date.valid'}) is None:
            dataset['date'] = ''
        else:
            dataset['date'] = soup_parser.head.\
                                    find(name='meta', attrs={'name': 'DC.date.valid'})['content']
        
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
            resource = Resource(source_url=res.url,
                                url=resource_link['href'])
            file_name = resource_link['href'].split('.')[-2]
            resource['name'] = h.unslugify(file_name.split('/')[-1].strip())

            try:
                resource['description'] = report_source.string
            except:
                resource['description'] = dataset['title']

            # get the format of the resource from the file extension of the link
            resource_format = resource_link['href']\
                            [resource_link['href'].rfind('.') + 1:]
            resource['format'] = resource_format

            # Add header information to resource object
            resource['headers'] = h.get_resource_headers(res.url, resource_link['href'])

            # add the resource to collection of resources
            dataset['resources'].append(resource)
        if len(dataset['resources']) == 0:
            continue

        yield dataset
