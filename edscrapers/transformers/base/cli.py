# -*- coding: utf-8 -*-
import sys
import importlib

from edscrapers.transformers.base import logger

def cli(argv):

    logger.debug("Starting transform for: {}".format(argv[1]))
    
    transformer = importlib.import_module(f"edscrapers.transformers.{argv[1]}.transform")
    transformer.transform(*argv[2:])
    
    logger.debug("Transform finished.")

if __name__ == '__main__':
    cli(sys.argv)
