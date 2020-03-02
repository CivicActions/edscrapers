""" parser for ocr state/national estimates 2011/12, 2013/14"""

import json

import bs4 # pip install beautifulsoup4

import edscrapers.scrapers.base.helpers as h
import edscrapers.scrapers.base.parser as base_parser
from edscrapers.scrapers.base.models import Dataset, Resource


def parse(res) -> dict:
    """ function parses content to create a dataset model """

    # create parser object
    soup_parser = bs4.BeautifulSoup(res.text, 'html5lib')
    # define a variable that is the dataset dict
    dataset_dict = None
    dataset_list = list()

    dataset_containers = soup_parser.body.find_all(class_='accordiontitle', recursive=True)
    for container in dataset_containers:
        # create dataset model dict
        dataset_dict = dict()
        dataset_dict['source_url'] = res.url

        dataset_dict['title'] = str(container.find(class_='accordionheader').\
                            string).strip()
        # replace all non-word characters (e.g. ?/) with '-'
        dataset_dict['name'] = h.make_slug(res.url)
        dataset_dict['publisher'] = ''
        dataset_dict['notes'] = str(container.find(name='p').string).\
                                  strip()
        dataset_dict['tags'] = ''
        dataset_dict['date'] = ''
        dataset_dict['contact_person_name'] = ""
        dataset_dict['contact_person_email'] = ""

        # create the dataset model
        dataset = Dataset(**dataset_dict)
        dataset.crawler_name = globals()['__package__'].split('.')[-2]

        # add  resources from the 'container' to the dataset
        page_resource_links = container.find_all(name='a',
                                                 href=base_parser.resource_checker,
                                                 recursive=True)
        for resource_link in page_resource_links:
            resource_obj = {'source_url': res.url,
                            'url': resource_link['href'],
                            'name': str(resource_link.string).strip()
                           }
            # get the format of the resource from the file extension of the link
            resource_format = resource_link['href']\
                            [resource_link['href'].rfind('.') + 1:]
            resource_obj['format'] = resource_format
            # create the Resource model
            resource_obj = Resource(**resource_obj)
            # add the resource_obj to collection of resources
            dataset.resources.append(resource_obj)

        # if this dataset alread has data resource files look for
        # document resource files
        if len(dataset.resources) > 0:
            # add  documents from the 'container' to the dataset
            page_document_links = container.find_all(name='a',
                                                    href=base_parser.document_checker,
                                                    recursive=True)
            for resource_link in page_document_links:
                resource_obj = {'source_url': res.url,
                                'url': resource_link['href'],
                                'name': str(resource_link.string).strip()
                               }
                # get the format of the resource from the file extension of the link
                resource_format = resource_link['href']\
                                [resource_link['href'].rfind('.') + 1:]
                resource_obj['format'] = resource_format
                # add the resource_obj to collection of resources
                resource_obj = Resource(**resource_obj)
                # add the resource_obj to collection of resources
                dataset.resources.append(resource_obj)
        # dump dataset
        dataset.dump()
        # append dataset (converted to dict) to dataset_list
        dataset_list.append(json.loads(dataset.toJSON()))
    

    return dataset_list
