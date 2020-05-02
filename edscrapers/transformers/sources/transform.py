""" module transforms the raw dataset files (i.e. the results/output from scraping)
into a different json data structure referred to as Sources.
Each scraping output directory will have its own
sources file upon completion of the transformation. Files are titled
'{name}.sources.json' .
All transformation output is written into 'sources' subdirectory of the
'transformers' directory on 'ED_OUTPUT_PATH' """

import os
import json
from pathlib import Path
from collections import Counter
import re

from edscrapers.cli import logger
from edscrapers.transformers.base import helpers as h


OUTPUT_DIR = os.getenv('ED_OUTPUT_PATH') # get the output directory

# get this transformer's output directory
CURRENT_TRANSFORMER_OUTPUT_DIR = h.get_output_path('sources')


def transform(name=None, input_file=None):
    """
    function is responsible for transofrming raw datasets into Sources
    """

    if input_file is None: # no input file specified
        file_list = h.traverse_output(name) # run through all the files in 'name' directory
    else:
        try:
            with open(input_file, 'r') as fp:
                file_list = [line.rstrip() for line in fp]
        except:
            logger.warn(f'Cannot read from list of output files at {input_file}, falling back to all collected data!')
            file_list = h.traverse_output(name)
    
    sources_list = [] # holds the list of sources acquired from 'name' scraper directory
    # loop through filepath in file list
    for file_path in file_list:
        # read the json data in each filepath
        data = h.read_file(file_path)
        if not data: # if data is None
            continue

        # retrieve source from dataset
        source = extract_source_from(dataset=data, use_key='collection')
        if not source: # source could not be retrieved
            continue
        # add source to list
        sources_list.append(source)

    # get a list of non-duplicate Sources
    sources_list = get_distinct_sources_from(sources_list, min_occurence_counter=2)
    # get the path were the gotten Sources will be saved to on local disk
    file_output_path = f'{CURRENT_TRANSFORMER_OUTPUT_DIR}/{(name or "all")}.sources.json'
    # write to file the Sources gotten from 'name' scraped output
    h.write_file(file_output_path, sources_list)
    # write file the Sources gotten from 'name' scraped out to S3 bucket
    h.upload_to_s3_if_configured(file_output_path, 
                                 f'{(name or "all")}.sources.json')


def extract_source_from(dataset: dict, use_key: str='collection') -> dict:
    """
    function is used to extract a Source from the provided dataset.
    NOTE:
    In the current sttructure for the raw dataset, a Source object is housed
    within a Collection object, it is necessary for this function to retrieve/interact
    with Collection object prior to retrieving the Source object. This implementation
    may changed in the future if the raw dataset structure changes
    
    - use_key: the key within the dataset that houses the COLLECTION
    """

    if not dataset.get(use_key, None): # if there is no collection present
        return None
    
    if len(dataset[use_key]) == 0: # empty key (no collection content)
        return None
    
    if not dataset[use_key].get('source', None): # no Source specified for this Collection
        return None
    
    if len(dataset[use_key]['source']) == 0: # empty key (no Source content)
        return None

    return dataset[use_key]['source'] # return extracted Source


def get_distinct_sources_from(source_list,
                                  min_occurence_counter: int=1) -> list:
    """ function returns a list of distinct/unique (non-duplicate) Sources
    extracted from the provided sources list
    
    PARAMETERS
    - sources_list: a list containing the Sources to extract distinct
    Sources from

    - min_occurence_counter: the operations used to identify a distinct Source can 
    be instructed on how to identify a Source for consideration. The
    'min_occurence_counter' instructs the algorithm to
    ignore/remove a Source from the list of distinct Sources if it does not
    occur/appear within the provided 'sources_list' at least that number of times.
    The default value is 1. Setting 'min_occurence_counter to < 1 will disable this
    check when creating a distinct/unique (non-duplicate) Source list
    """

    if (not source_list) or len(source_list) == 0: # parameter not provided
        return None
    
    # get a 'mapped' source_list for easy operation
    mapped_sources = map(lambda source: source.get('source_id', 
                                                        source['source_title']),
                                   source_list)
    
    # find out if minimum occurence checks should be performed
    min_occurence_counter = int(min_occurence_counter)
    if min_occurence_counter > 0: # perform minimum occcurence check
        sources_counter = Counter(mapped_sources) # Counter for how many times a Source occurs
        count_keys = list(sources_counter.keys()) # create a list from the counter key/source id
        for key in count_keys: # loop through each counter key/source id
            if sources_counter[key] < min_occurence_counter: # if counter key/source id < min_occurence counter
                # remove this key as it represents a Source that occurs less than requested
                del sources_counter[key]
        # end of minimum occurence checks,
        # so, generate the 'mapped' source list from the results of this check
        mapped_sources = sources_counter.elements()

    # get distinct (non-duplicate) 'mapped' source_list
    mapped_sources = set(mapped_sources)

    distinct_source_list = [] # holds the list of distinct source objects
    # iterate through 'mapped_source'
    for mapped_source in mapped_sources:
        # iterate through 'source_list'  parameter
        for source in source_list:
            # the source has the same id or title as mapped_source
            if source.get('source_id', source['source_title']) == mapped_source:
                # add this source to the list of distinct source objects
                distinct_source_list.append(source)
                break # leave the inner loop
    
    return distinct_source_list # return the distinct source
