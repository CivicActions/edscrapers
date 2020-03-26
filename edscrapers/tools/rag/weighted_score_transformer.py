""" module computes the weighted scores of data.json files and 
transforms the resources into a csv file 
with name 'datasets_weighted_scores_{yyyy_mm_dd}.csv' """

import urllib.parse
import os
import datetime

import pandas as pd

import edscrapers.transformers.base.helpers as transformers_helpers
from edscrapers.cli import logger

from . import DATASET_WEIGHTING_SYS, TOTAL_WEIGHT # import weighting system & total weight

# get the output directory
OUTPUT_DIR = os.getenv('ED_OUTPUT_PATH')


def transform(name=None, input_file=None) -> pd.DataFrame:
    """ function transforms the data.json into a dataframe/csv 
    PARAMETERS
    name: if provided must correspond to the name of a scraper.
    the data.json files contained in the 'name' scraper subdirectory of the 
    'ED_OUTPUT_PATH/scraper' will be read
    
    input_file: if provided mut be a file with list of data.json
    to read.

    If no parameters are provided, which is the default behaviour;
    then all data.json files contained in 'ED_OUTPUT_PATH/scraper' will be read.

    function returns the DataFrame contained the transformed data.json files
    """
    
    file_list = [] # holds the list of files which contain dataset json
    datasets_list = [] # holds the datasets jsons gotten from files

    if not input_file: # no input file provided
        # loop over directory structure
        if name:
            # loop over <name> scraper output e.g nces
            file_list = transformers_helpers.traverse_output(name)
            # datasets = list of all <name> files
        else:
            # loop over everything
            file_list = transformers_helpers.traverse_output(None)
            # datasets = list of all JSON files
    else: # input file provided
        # read input_file, which is a list of files
        with open(input_file, 'r') as fp:
            try:
                file_list = [line.rstrip() for line in fp]
            except Exception:
                # logger.warn(f'Cannot read from list of output files at {input_file}, falling back to all collected data!')
                file_list = transformers_helpers.traverse_output(None)

    # read the contents in file_list
    for file_path in file_list:
        # read json from the file using helper
        data = transformers_helpers.read_file(file_path)
        # compute the weight score of the dataset
        compute_score(data)
        datasets_list.append(data)

    # map the datasets to pandas format
    dataset_rows_list = map(lambda dataset: [dataset['publisher'],\
                                             dataset['source_url'], \
                                            dataset['_weighted_score'], \
                                            dataset['_weighted_score_ratio']], 
                            datasets_list)
    # create the pandas df
    weighted_datasets_scores_df = pd.DataFrame(dataset_rows_list,
                                                columns=['publisher',
                                                         'source url',
                                                         'weighted score',
                                                         'weighted score ratio'])
    
    # create a df that incorporates domain info
    weighted_datasets_scores_df2 = pd.DataFrame(columns=['domain'])
    weighted_datasets_scores_df2['domain'] = weighted_datasets_scores_df.\
            apply(lambda row: urllib.parse.\
                    urlparse(row['source url']).hostname.\
                        replace('www2.', 'www.').replace('www.', ''), axis=1)
    
    weighted_datasets_scores_df2['publisher'] = weighted_datasets_scores_df['publisher']
    weighted_datasets_scores_df2['source url'] = weighted_datasets_scores_df['source url']
    weighted_datasets_scores_df2['weighted score'] = weighted_datasets_scores_df['weighted score']
    weighted_datasets_scores_df2['weighted score ratio'] = weighted_datasets_scores_df['weighted score ratio']

    # create the output csv file name
    output_filename = "datasets_weighted_scores_{}_{:02d}_{:02d}.csv".\
        format(datetime.datetime.now().year, 
                                      datetime.datetime.now().month,
                                      datetime.datetime.today().day)
    # create the fullpath weer file will be written
    fullpath = os.path.join(OUTPUT_DIR, output_filename)
    # write the dataframe to csv
    weighted_datasets_scores_df2.to_csv(fullpath, index=False)
    # write the csv to S3 bucket
    transformers_helpers.upload_to_s3_if_configured(OUTPUT_DIR, output_filename)
    
    return weighted_datasets_scores_df2



def compute_score(dataset: dict, append_score=True) -> dict:
    """ function computed the weighted score for the provided dataset.
    It uses the WEIGHTING SYSTEM provided in this package/module.
    
    If 'append_score' is True (the default), then the weighted score and 
    the weighted score ratio are added to the dataset as additional keys.
    The keys are '_weighted_score' and '_weighted_score_ratio'.
    
    Function returns a dict with these two keys
    """
    
    score = 0 # used to tally weighted score for the dataset
    
    # loop through all the keys in the weighted system
    for weighted_value_dict in DATASET_WEIGHTING_SYS.values():
        # check if the current dataset json schema has the attribute/key/metadata required
        if weighted_value_dict['dataset_key'] == '': # the key is not present
            score += 0 # that is a 'no score'
        else: # key is present in schema
            # check if the dataset provided for scoring has the metadata
            metadata_value = dataset.get(weighted_value_dict['dataset_key'], None)
            # check if the dataset has useful value
            if metadata_value is None or str(metadata_value).strip() == "":
                score += 0 # no useful value
            else: # there is useful value
                # score the dataset metadata based on the agreed weight
                score += weighted_value_dict['score']

    # check if score should be appended
    if append_score:
        dataset['_weighted_score'] = score
        dataset['_weighted_score_ratio'] = score / TOTAL_WEIGHT  
    
    return {'_weighted_score': score, '_weight_score_ratio': score / TOTAL_WEIGHT}


# TODO REMOVE THIS. THIS IS JUST FOR CONVENIENT TESTING
if __name__ == "__main__":
    transform(name='ocr')
    