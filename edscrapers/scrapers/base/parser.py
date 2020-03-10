""" file containers utility functions to be used by BeautifulSoup parser"""

import edscrapers.scrapers.base.helpers as h

# contains list of data resources to exclude from dataset
deny_list = ['site-list.xls']

def resource_checker(tag_attr: str):
    """ function is used as a filter for BeautifulSoup to
    locate resource (i.e. DATA_EXTENSIONS) files"""

    if tag_attr != '' and tag_attr is not None:
        for extension in h.get_data_extensions().keys():
            if tag_attr.endswith(f'{extension}') and\
                (tag_attr[tag_attr.rfind('/')+1:] not in deny_list):
                return True
        # if code gets here, no resources found
        return False
    # tag_attr does not match resource required, so return False
    return False

def document_checker(tag_attr: str):
    """ function is used as a filter for BeautifulSoup to
    locate document files (i.e. DOCUMENT_EXTENSIONS) files"""

    if tag_attr != '' and tag_attr is not None:
        for extension in h.get_document_extensions().keys():
            if tag_attr.endswith(f'.{extension}'):
                return True
        # if code gets here, no resources found
        return False
    # tag_attr does not match resource required, so return False
    return False
