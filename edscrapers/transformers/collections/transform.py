""" module transforms the raw dataset files (i.e. the results/output from scraping)
into a different json data structure referred to as Collections.
Each scraping output directory will have its own
collections file upon completion of the transformation. Files are titled
'{name}_collections.json' """

import os
import json
from pathlib import Path
import re

from edscrapers.cli import logger
from edscrapers.transformers.base import helpers as h


OUTPUT_DIR = os.getenv('ED_OUTPUT_PATH') # get the output directory

# get this transformer's output directory
CURRENT_TRANSFORMER_OUTPUT_DIR = h.get_output_path('collections')

def transform(name=None, input_file=None):

    if input_file is None:
        file_list = h.traverse_output(name)
    else:
        try:
            with open(input_file, 'r') as fp:
                file_list = [line.rstrip() for line in fp]
        except:
            logger.warn(f'Cannot read from list of output files at {input_file}, falling back to all collected data!')
            file_list = h.traverse_output(name)
    
    # loop through filepath in file list
    for file_path in file_list:
        # read the json data in each filepath
        data = h.read_file(file_path)
        if not data: # if data is None
            continue
        # mark as private datasets that have certain keywords in their data
        data = _mark_private(data, search_words=['conference', 'awards',
                                                'user guide', 'applications'])

        # mark of removal datasets that have certain keywords
        data = _remove_dataset(data, search_words=['photo'])

        # REMOVE UNWANTED STRING FROM THE VALUE OF A DATASET'S KEY
        # 1. remove 'table [0-9].' from beginning of dataset title
        data = _strip_unwanted_string(data, r'^table [0-9a-z]+(-?[a-z])?\.', 
                                      dict_key='title')
        
        # set the 'level of data' for the dataset
        data = _set_dataset_level_of_data(data)

        # write modified dataset back to file
        h.write_file(file_path, data)

