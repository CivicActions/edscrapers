# -*- coding: utf-8 -*-
import re
import logging
import datetime
import hashlib
import requests
import bs4

from urllib.parse import urlparse
from urllib.parse import urljoin
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from edscrapers.scrapers.base.models import Resource, Collection, Source

import pathlib
import importlib

logger = logging.getLogger(__name__)


def get_data_extensions():
    return {
        '.xls': 'Excel data file',
        '.csv': 'Comma delimited text file',
        '.sas': 'SAS syntax file',
        '.dat': 'Generic data file',
        '.spss': 'SPSS syntax',  # This may be an incorrect extension, but we will continue to search for it
        '.db.': 'Generic data base',
        '.sql': 'Structured query language file',
        '.xml': 'Extensible Markup language',
        '.zip': 'File containing compressed files',
        '.txt': 'Text files',

        '.xlsx': 'Excel data file',
        '.sps': 'SPSS syntax',
        '.sav': 'SPSS data',
        '.dat': 'Stata data',
        '.do': 'Stata syntax',
        '.r': 'R script',
        '.rdata': 'R data',
        '.rda': 'R data',
        '.sd2': 'SAS data',
        '.sd7': 'SAS data',
        '.sas7bdat': 'SAS data'
    }

def get_document_extensions():
    return {
        '.docx': 'Word document',
        '.doc': 'Word document',
        '.pdf': 'PDF file'
    }

def get_all_resources(res, dataset, extensions, deny_list=[]):
    for link in LxmlLinkExtractor(deny_extensions=[], deny=deny_list).extract_links(res):
        for extension in extensions.keys():
            if link.url.endswith(extension):
                resource = Resource(
                    source_url = res.url,
                    url = link.url,
                    name = link.text,
                )
                dataset['resources'].append(resource)

def get_variables(object, filter=None):
    """Extract variables from object to dict using name filter.
    """
    variables = {}
    for name, value in vars(object).items():
        if filter is not None:
            if not filter(name):
                continue
        variables[name] = value
    return variables

def get_meta_value(soup, meta_name):
    meta_tag = soup.head.find(name='meta',attrs={'name': meta_name})
    if meta_tag is None:
        meta_tag = soup.head.find(name='meta',attrs={'property': meta_name})
        if meta_tag is None:
            return None
    return meta_tag['content']

def get_resource_headers(source_url, url):
    headers = dict()
    if urlparse(url).scheme:
        raw_headers = requests.get(url).headers
    else:
        raw_headers = requests.get(urljoin(source_url, url)).headers

    headers['content-type'] = raw_headers['Content-Type']
    headers['last-modified'] = raw_headers['Last-Modified']
    headers['content-length'] = raw_headers['Content-Length']

    return headers

def retrieve_crawlers_allowed_domains(except_crawlers=[]) -> list:
    """ function retireves all 'allowed_domains'
    (domains which are allowed to be scraped) from the available
    crawlers in the 'scrapers' package EXCEPT for the 'allowed_domains'
    for crawlers listed in 'except_crawlers'.
    
    function returns a list containing domain names ('allowed_domains')
    retrieved from all crawlers EXCEPT crawlers listed in 'except_crawlers'

    PARMAETERS:
    - except_crawlers : contains a list of crawler names whose
    'allowed_domains' should NOT be retrieved'. The default
    value is an empty list (which means no crawler is excluded) """

    # get the path to the scrapers package
    scrapers_path = pathlib.Path('./edscrapers/scrapers')
    allowed_domains = set() # collection of allowed domains
    except_allowed_domains = set() # domains to be exempted from collection

    # iterate over all subpackages in the scrapers package
    for subpath in scrapers_path.iterdir():
        if subpath.is_dir(): # check if subpath is a directory
            try:
                # import the crawler module from the subpackage
                crawler = importlib.import_module('.' + subpath.name + '.crawler', 
                                                  'edscrapers.scrapers')
                # check if the subpath is in included in exempted crawlers
                if subpath.name not in except_crawlers: # subpath not exempted
                    # retrieve the 'allowed_domains' from the imported crawler
                    # and add it the set of 'allowed domains'
                    allowed_domains.update(crawler.Crawler.allowed_domains)
                else: # subpath is exempted
                    # add the 'allowed_domains' from this subpackage to
                    # set of exempted domains
                    except_allowed_domains.update(crawler.Crawler.allowed_domains)
            except:
                continue
            # remove all exempted domains which may also be present in
            # 'allowed domains'
            allowed_domains.difference_update(except_allowed_domains)
    return list(allowed_domains) # return allowed_domains

    def extract_dataset_collection_from_url(collection_url, source_url=None):
        """ function is used to generate/extract a dataset 'Collection' from
        the provided collection_url.
        A collection is created based on the Collection model in
        edscrapers.scrapers.base.models
        """
        # make a request for html page contained in the provided url
        res = requests.get(collection_url, verify=False)

        # ensure that the response text gotten is a string
        if not isinstance(getattr(res, 'text', None), str):
            return None

        try:
            soup_parser = bs4.BeautifulSoup(res.text, 'html5lib')
        except:
            return None
        
        collection = Collection()
        collection['collection_url'] = res.url
        collection['collection_title'] = str(soup_parser.head.\
                                find(name='title').string).strip()
        collection['collection_id'] =\
            f'{hashlib.md5(collection["collection_url"].encode("utf-8")).hexdigest()}-{hashlib.md5(__package__.split(".")[-2].encode("utf-8")).hexdigest()}'

        if source_url:
            pass
