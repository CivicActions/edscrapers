import urllib.parse
import os
import pandas as pd
from datetime import datetime as dt
from pathlib import Path

import edscrapers.transformers.base.helpers as h
from edscrapers.cli import logger

# get the output directory
OUTPUT_DIR = h.get_output_path('excel')

def _add_to_spreadsheet(file_path, sheet_name, result):
    # write the result (dataframe) to an excel sheet
    if os.path.exists(file_path): # check if excel sheet exist
        writer_mode = 'a' # set write mode to append
    else:
        writer_mode = 'w' # set write mode to write
    with pd.ExcelWriter(file_path, engine="openpyxl",
                        mode=writer_mode) as writer:
        result.to_excel(writer,
                        sheet_name=sheet_name,
                        index=False,
                        engine='openpyxl')
    pass


def transform(name=None, input_file=None):

    print(name)
    file_list = [] # holds the list of files which contain datajson/dataset
    datasets_list = [] # holds the data jsons gotten from files

    if name: # name of processed datajson is provided so get the file path
        file_list.append(Path(h.get_output_path('datajson'), f'{name}.data.json'))
    else: # name of processed datajson not provided
        file_list.extend(Path(h.get_output_path('datajson')).glob('*.json'))

    # read the contents in the file_list
    for file_path in file_list:

        df = pd.DataFrame(columns=[
            'title',
            'description',
            'tags',
            'modified'
            'publisher',
            'source_url',
            'data_steward_email',
            'name',
            'access_level',
            'bureauCode',
            'programCode',
            'license',
            'spatial',
            'categories',
            'level_of_data'
        ])

        if name:
            sheet_name = name
        else:
            sheet_name = file_path.name.split('.')[0].upper()

        # read json from file using helper function
        data = h.read_file(file_path)
        for dd in data.get('dataset', []): # loop through the datasets contained in data

            dfd = {
                'name': dd.get('identifier', None),
                'title': dd.get('title', None),
                'description': dd.get('description', None),
                'tags': ', '.join(dd['keyword']),
                'modified': dd.get('modified', None),
                'publisher': dd['publisher']['name'],
                'source_url': dd['scraped_from'],
                'data_steward_email': dd['contactPoint']['hasEmail'],
                'access_level': dd.get('accessLevel', None),
                'bureauCode': ', '.join(dd.get('bureauCode', [])),
                'programCode': ', '.join(dd.get('programCode', [])),
                'license': dd.get('license', None),
                'spatial': dd.get('spatial', None),
                'categories': ', '.join(dd.get('theme', [])),
                'level_of_data': ', '.join(dd.get('levelOfData', [])),
            }


            # if df is None:
            #     # On first run, initialize the datframe with the datajson structure
            #     # TODO: Remove this hack, maybe, sometimes
            #     df = pd.DataFrame(columns=dataset_dict.keys())

            # datasets_list.append(dataset_dict)
            # print(dataset_dict['title'])
            df2 = pd.DataFrame([dfd.values()], columns=dfd.keys())
            # print(df2)
            logger.debug(f"Dumping data for [{sheet_name}] {dd['identifier']}")
            df = df.append(df2, ignore_index=True)

        logger.debug(f"Dumping data for {file_path}")
        _add_to_spreadsheet(os.path.join(OUTPUT_DIR, 'datasets.xlsx'), sheet_name, df)
