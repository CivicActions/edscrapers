""" module handles the sanitising of datajson output """

import os
import json
from pathlib import Path
import re

from edscrapers.cli import logger
from edscrapers.transformers.base import helpers as h


OUTPUT_DIR = os.getenv('ED_OUTPUT_PATH') # get the output directory

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
        # mark private datasets that have certain keywords in their data
        data = _mark_private(data, search_words=['conference', 'awards',
                                                'user guide', 'applications'])
        # write modified dataset back to file
        h.write_file(file_path, data)



def _mark_private(dataset: dict, search_words=[], add_word_tag=True,
                  mark_as_private=True) -> dict:
    """ private helper function.
    FUNCTION ONLY adds/modifies the '_clean_data' key of 'dataset' during operations.

    searches the dataset title for provided search_words.
    if any search_words are found, will OPTIONALLY marks the datasets as private and
    adds the search word as a tag to the list of keywords"""

    if dataset.get('title') is None:
        return
    
    dataset['title'] = dataset['title'].strip()

    # get the '_clean_data' key of dataset
    clean_data = dataset.setdefault('_clean_data', {})
    # get the tags key from clean_data or use those from dataset
    tags = clean_data.get('tags', dataset['tags'].strip())


    for word in search_words:
        # check if word is in dataset title
        if re.search('\\b'+ word + '\\b', dataset['title'], re.IGNORECASE):
            # word is in title
            if add_word_tag and word.lower().replace(' ', '-')\
                not in h.transform_keywords(tags):
                # word needs to be added to tag
                tags = h.transform_keywords(tags)
                tags.append(word.lower().replace(' ', '-'))
                tags = ';'.join(tags)
                clean_data['tags'] = tags
            # mark dataset as 'private;
            if mark_as_private:
                clean_data['accessLevel'] = 'non-public'

    if len(clean_data.keys()) > 0: # if '_clean_data' has keys
        dataset['_clean_data'] = clean_data # update dataset
    else: # else no keys
        del dataset['_clean_data'] # delete '_clean_data' key from dataset

    return dataset