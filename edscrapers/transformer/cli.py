# -*- coding: utf-8 -*-
import sys
from edscrapers.transformer.transform import to_data_json
from edscrapers.transformer import logger

def cli(argv):

    logger.debug('Starting transform for: {}'.format(argv[1]))
    to_data_json(argv[1])
    logger.debug('Transform finished.')

if __name__ == '__main__':
    cli(sys.argv)