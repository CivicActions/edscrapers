# -*- coding: utf-8 -*-
import sys
import logging
from edscrapers.transformer.transform import to_data_json

logger = logging.getLogger(__name__)

def cli(argv):

    to_data_json(argv[1])

if __name__ == '__main__':
    cli(sys.argv)