# -*- coding: utf-8 -*-
import re
import logging
import datetime
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from edscrapers.scrapers.base.models import Resource

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
        '.sas7bdat': 'SAS data',
    }

def get_document_extensions():
    return {
        '.docx': 'Word document',
        '.doc': 'Word document',
        '.pdf': 'PDF file',
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
                dataset.resources.append(resource)

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

