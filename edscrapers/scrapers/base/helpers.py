# -*- coding: utf-8 -*-
import re
import logging
import datetime
logger = logging.getLogger(__name__)


# Module API


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

def make_slug(url):
    return '-'.join(url.split('/')[3:]).replace('.html', '').replace('.', '-')
