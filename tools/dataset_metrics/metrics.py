""" module provides functions for obtaining
various metrics about the Dept Ed scraping exercise"""

import urllib.parse
import os
import json
import functools

import pandas as pd # pip install pandas
import requests # pip install requests

from tools.dataset_metrics import datopian_out_df, air_out_df, METRICS_OUTPUT_PATH
import tools.dataset_metrics.helpers as h


def list_domain(scraper='datopian', ordered=True):
    """function is used to list the domains scraped by
    'scraper'. Optionally order these domains
    by number of pages parsed if 'ordered' is True """

    # check which scraper domain listing is for
    if scraper.upper() == "DATOPIAN":
        # create a dataframe with duplicate source_urls removed
        datopian_out_deduplicated_df = datopian_out_df.\
            drop_duplicates(subset='source_url', inplace=False)
        # create subset of the datopian dataframe (subset will house domain info)
        datopian_df_subset = pd.DataFrame(columns=['domain'])
        # create the domain column from the source_url info available
        datopian_df_subset['domain'] = datopian_out_deduplicated_df.\
            apply(lambda row: urllib.parse.\
                 urlparse(row['source_url']).hostname.\
                     replace('www2.', 'www.').replace('www.', ''), axis=1)
        # to get the number of pages visited from each domain, perform groupby
        grouped = datopian_df_subset.groupby(['domain'])
        # recreate the datopian dataframe subset to store aggreated domain info
        datopian_df_subset = pd.DataFrame(columns=['domain'])
        # get the keys/names for grouped domains
        datopian_df_subset['domain'] = list(grouped.indices.keys())
        # get the size of each group
        # i.e. the number of times each domain appeared in the non-grouped dataframe
        # this value represents the number of pages visited
        datopian_df_subset['page count'] = list(grouped.size().values)

        # if 'ordered' is True, sorted the df by 'page count' in descending order
        if ordered:
            datopian_df_subset.sort_values(by='page count', axis='index',
                                           ascending=False, inplace=True,
                                           ignore_index=True)
            # write the dataframe to an excel sheet
            if os.path.exists(METRICS_OUTPUT_PATH): # check if excel sheet exist
                writer_mode = 'a' # set write mode to append
            else:
                writer_mode = 'w' # set write mode to write
            with pd.ExcelWriter(METRICS_OUTPUT_PATH, engine="openpyxl",
                                mode=writer_mode) as writer:
                datopian_df_subset.to_excel(writer,
                                           sheet_name='PAGE COUNT (DATOPIAN)',
                                           index=False, engine='openpyxl')
        return datopian_df_subset

    elif scraper.upper() == "AIR":
        # create a dataframe with duplicate source_urls removed
        air_out_deduplicated_df = air_out_df.\
            drop_duplicates(subset='source_url', inplace=False)
        # create subset of the AIR dataframe (subset will house domain info)
        air_df_subset = pd.DataFrame(columns=['domain'])
        # create the domain column from the source_url info available
        air_df_subset['domain'] = air_out_deduplicated_df.\
            apply(lambda row: urllib.parse.\
                 urlparse(row['source_url']).hostname.\
                     replace('www2.', 'www.').replace('www.', ''), axis=1)
        # to get the number of pages visited from each domain, perform groupby
        grouped = air_df_subset.groupby(['domain'])
        # recreate the AIR dataframe subset to store aggreated domain info
        air_df_subset = pd.DataFrame(columns=['domain'])
        # get the keys/names for grouped domains
        air_df_subset['domain'] = list(grouped.indices.keys())
        # get the size of each group
        # i.e. the number of times each domain appeared in the non-grouped dataframe
        # this value represents the number of pages visited
        air_df_subset['page count'] = list(grouped.size().values)

        # if 'ordered' is True, sorted the df by 'page count' in descending order
        if ordered:
            air_df_subset.sort_values(by='page count', axis='index',
                                           ascending=False, inplace=True,
                                           ignore_index=True)
        # write the dataframe to an excel sheet
        if os.path.exists(METRICS_OUTPUT_PATH): # check if excel sheet exist
                writer_mode = 'a' # set write mode to append
        else:
                writer_mode = 'w' # set write mode to write
        with pd.ExcelWriter(METRICS_OUTPUT_PATH, engine="openpyxl",
                            mode=writer_mode) as writer:
            air_df_subset.to_excel(writer,
                                        sheet_name='PAGE COUNT (AIR)',
                                        index=False, engine='openpyxl')
        return air_df_subset
    else:
        raise ValueError('invalid "scraper" provided')


def list_exclusive_domain(scraper='datopian',
                          compare_scraper='air', ordered=True):
    """ function is used to determine what domains were
    EXCLUSIVELY visited by 'scraper' and NOT by 'compare_scraper' .
    If 'ordered' is True, dataframe is sorted by 'resource count' """

    # create a datopian dataframe with duplicate url and source_urls removed
    datopian_out_deduplicated_df = datopian_out_df.\
        drop_duplicates(subset=['url', 'source_url'], inplace=False)
    # create subset of the datopian dataframe (subset will house domain info)
    datopian_df_subset = pd.DataFrame(columns=['domain'])
    # create the domain column from the source_url info available
    datopian_df_subset['domain'] = datopian_out_deduplicated_df.\
        apply(lambda row: urllib.parse.\
                urlparse(row['source_url']).hostname.\
                    replace('www2.', 'www.').replace('www.', ''), axis=1)
    # to get the number of pages visited from each domain, perform groupby
    grouped = datopian_df_subset.groupby(['domain'])
    # recreate the datopian dataframe subset to store aggreated domain info
    datopian_df_subset = pd.DataFrame(columns=['domain'])
    # get the keys/names for grouped domains
    datopian_df_subset['domain'] = list(grouped.indices.keys())
    # get the size of each group
    # i.e. the number of times each domain appeared in the non-grouped dataframe
    # this value represents the number of resources visited
    datopian_df_subset['resource count'] = list(grouped.size().values)

    # create a air dataframe with duplicate url and source_urls removed
    air_out_deduplicated_df = air_out_df.\
        drop_duplicates(subset=['url', 'source_url'], inplace=False)
    # create subset of the air dataframe (subset will house domain info)
    air_df_subset = pd.DataFrame(columns=['domain'])
    # create the domain column from the source_url info available
    air_df_subset['domain'] = air_out_deduplicated_df.\
        apply(lambda row: urllib.parse.\
                urlparse(row['source_url']).hostname.\
                    replace('www2.', 'www.').replace('www.', ''), axis=1)
    # to get the number of pages visited from each domain, perform groupby
    grouped = air_df_subset.groupby(['domain'])
    # recreate the air dataframe subset to store aggreated domain info
    air_df_subset = pd.DataFrame(columns=['domain'])
    # get the keys/names for grouped domains
    air_df_subset['domain'] = list(grouped.indices.keys())
    # get the size of each group
    # i.e. the number of times each domain appeared in the non-grouped dataframe
    # this value represents the number of resources visited
    air_df_subset['resource count'] = list(grouped.size().values)

    # check which scraper is requested
    if scraper.upper() == "DATOPIAN":
        # get all domains visited by datopian but NOT AIR.
        # We use the trick of concatenating 'air_df_subset' twice.
        # This is to ensure that when remove duplicates
        # in later step all rows from 'air_df_subset' will
        # ALWAYS be removed.
        datopian_df_subset = pd.concat([datopian_df_subset,
        air_df_subset, air_df_subset], axis='index', ignore_index=True)
        # remove duplicate rows
        datopian_df_subset.drop_duplicates(subset=['domain'], keep=False,
                                           inplace=True)

        # if 'ordered' is True, sorted the df by 'resource count' in descending order
        if ordered:
            datopian_df_subset.sort_values(by='resource count', axis='index',
                                           ascending=False, inplace=True,
                                           ignore_index=True)

        # write the dataframe to an excel sheet
        if os.path.exists(METRICS_OUTPUT_PATH): # check if excel sheet exist
            writer_mode = 'a' # set write mode to append
        else:
            writer_mode = 'w' # set write mode to write
        with pd.ExcelWriter(METRICS_OUTPUT_PATH, engine="openpyxl",
                            mode=writer_mode) as writer:
            datopian_df_subset.to_excel(writer,
                                        sheet_name='RESOURCE COUNT PER DOMAIN (DATOPIAN ONLY)',
                                        index=False, engine='openpyxl')
        return datopian_df_subset

        # check which scraper domain listing is for
    elif scraper.upper() == "AIR":
        # get all domains visited by AIR but NOT datopian
        air_df_subset = pd.concat([air_df_subset,
        datopian_df_subset, datopian_df_subset], axis='index', ignore_index=True)
        # remove duplicate rows
        air_df_subset.drop_duplicates(subset=['domain'], keep=False,
                                           inplace=True)

        # if 'ordered' is True, sorted the df by 'resource count' in descending order
        if ordered:
            air_df_subset.sort_values(by='resource count', axis='index',
                                           ascending=False, inplace=True,
                                           ignore_index=True)

        # write the dataframe to an excel sheet
        if os.path.exists(METRICS_OUTPUT_PATH): # check if excel sheet exist
            writer_mode = 'a' # set write mode to append
        else:
            writer_mode = 'w' # set write mode to write
        with pd.ExcelWriter(METRICS_OUTPUT_PATH, engine="openpyxl",
                            mode=writer_mode) as writer:
            air_df_subset.to_excel(writer,
                                        sheet_name='RESOURCE COUNT PER DOMAIN (AIR ONLY)',
                                        index=False, engine='openpyxl')
                                        
        return air_df_subset
    else:
        raise ValueError('invalid "scraper" provided')


def list_intersection_domain(scraper='datopian',
                          compare_scraper='air', ordered=True):
    """ function is used to determine what domains were
    BOTH visited by 'scraper' AND 'compare_scraper' .
    If 'ordered' is True, dataframe is sorted by 'resource count' """

    if (scraper.upper() != "DATOPIAN" and compare_scraper.upper() != "AIR")\
        and (scraper.upper() != "AIR" and compare_scraper.upper() != "DATOPIAN"):
        raise ValueError('invalid "scraper" or "compare_scraper" provided')

    # create a datopian dataframe with duplicate url and source_urls removed
    datopian_out_deduplicated_df = datopian_out_df.\
        drop_duplicates(subset=['url', 'source_url'], inplace=False)
    # create subset of the datopian dataframe (subset will house domain info)
    datopian_df_subset = pd.DataFrame(columns=['domain'])
    # create the domain column from the source_url info available
    datopian_df_subset['domain'] = datopian_out_deduplicated_df.\
        apply(lambda row: urllib.parse.\
                urlparse(row['source_url']).hostname.\
                    replace('www2.', 'www.').replace('www.', ''), axis=1)
    # to get the number of pages visited from each domain, perform groupby
    grouped = datopian_df_subset.groupby(['domain'])
    # recreate the datopian dataframe subset to store aggreated domain info
    datopian_df_subset = pd.DataFrame(columns=['domain'])
    # get the keys/names for grouped domains
    datopian_df_subset['domain'] = list(grouped.indices.keys())
    # get the size of each group
    # i.e. the number of times each domain appeared in the non-grouped dataframe
    # this value represents the number of resources visited
    datopian_df_subset['resource count'] = list(grouped.size().values)

    # create a air dataframe with duplicate url and source_urls removed
    air_out_deduplicated_df = air_out_df.\
        drop_duplicates(subset=['url', 'source_url'], inplace=False)
    # create subset of the air dataframe (subset will house domain info)
    air_df_subset = pd.DataFrame(columns=['domain'])
    # create the domain column from the source_url info available
    air_df_subset['domain'] = air_out_deduplicated_df.\
        apply(lambda row: urllib.parse.\
                urlparse(row['source_url']).hostname.\
                    replace('www2.', 'www.').replace('www.', ''), axis=1)
    # to get the number of pages visited from each domain, perform groupby
    grouped = air_df_subset.groupby(['domain'])
    # recreate the air dataframe subset to store aggreated domain info
    air_df_subset = pd.DataFrame(columns=['domain'])
    # get the keys/names for grouped domains
    air_df_subset['domain'] = list(grouped.indices.keys())
    # get the size of each group
    # i.e. the number of times each domain appeared in the non-grouped dataframe
    # this value represents the number of resources visited
    air_df_subset['resource count'] = list(grouped.size().values)

    # intersect the dataframes
    merged_df = datopian_df_subset.merge(right=air_df_subset,
                                         how='inner', on=['domain'],
                                         suffixes=('_datopian', '_air'))
    # if 'ordered' is True, sorted the df by 'resource count' in descending order
    if ordered:
        merged_df.sort_values(by=['resource count_datopian',
                                 'resource count_air'],
                              axis='index',
                              ascending=False, inplace=True,
                              ignore_index=True)
    
    # write the dataframe to an excel sheet
    if os.path.exists(METRICS_OUTPUT_PATH): # check if excel sheet exist
        writer_mode = 'a' # set write mode to append
    else:
        writer_mode = 'w' # set write mode to write
    with pd.ExcelWriter(METRICS_OUTPUT_PATH, engine="openpyxl",
                        mode=writer_mode) as writer:
        merged_df.to_excel(writer,
                                    sheet_name='RESOURCE COUNT PER DOMAIN (DATOPIAN-AIR INTERSECTION)',
                                    index=False, engine='openpyxl')
    return merged_df
        

def list_highest_resources_from_pages(scraper='datopian',
                          ordered=True):
    """ function is used to determine what pages from a particular
    scraper produced/generated the highest number of resources.
    
    PARAMETERS
    - scraper: the scraper that was run on the domains to generate the 
    datasets e.g. DATOPIAN or AIR
    
    - ordered: whether the resulting DataFrame or 
    Excel sheet result be sorted/ordered. If True, order by 'resource per page'
     """

    # check which scraper is requested
    if scraper.upper() == "DATOPIAN":
        # create a datopian dataframe with duplicate url and source_urls removed
        datopian_out_deduplicated_df = datopian_out_df.\
            drop_duplicates(subset=['url', 'source_url'], inplace=False)
        # create subset of the datopian dataframe (subset will house domain info)
        datopian_df_subset = pd.DataFrame(columns=['domain'])
        # create the domain column from the source_url info available
        datopian_df_subset['domain'] = datopian_out_deduplicated_df.\
            apply(lambda row: urllib.parse.\
                    urlparse(row['source_url']).hostname.\
                        replace('www2.', 'www.').replace('www.', ''), axis=1)
        # get the 'source_url' renamed as 'page'
        datopian_df_subset['page'] = datopian_out_deduplicated_df['source_url']
        # to get the number of resources retrieved from each page, perform groupby
        grouped = datopian_df_subset.groupby(['domain', 'page'])
        # create dataframe to store aggreated resource info
        dataframe = pd.DataFrame(columns=['domain', 'page'])
        dataframe['domain'] = [domain for domain, page in grouped.indices.keys()]
        dataframe['page'] = [page for domain, page in grouped.indices.keys()]
        # get the size of each group
        # this value represents the number of resources gotten per page
        dataframe['resource per page'] = list(grouped.size().values)

        # if 'ordered' is True, sorted the df by 'resource count' in descending order
        if ordered:
            dataframe.sort_values(by='resource per page', axis='index',
                                           ascending=False, inplace=True,
                                           ignore_index=True)

        # write the dataframe to an excel sheet
        if os.path.exists(METRICS_OUTPUT_PATH): # check if excel sheet exist
            writer_mode = 'a' # set write mode to append
        else:
            writer_mode = 'w' # set write mode to write
        with pd.ExcelWriter(METRICS_OUTPUT_PATH, engine="openpyxl",
                            mode=writer_mode) as writer:
            dataframe.to_excel(writer,
                                        sheet_name='RESOURCE COUNT PER PAGE (DATOPIAN)',
                                        index=False, engine='openpyxl')
        return dataframe
        
    elif scraper.upper() == "AIR":
        # create a AIR dataframe with duplicate url and source_urls removed
        air_out_deduplicated_df = air_out_df.\
            drop_duplicates(subset=['url', 'source_url'], inplace=False)
        # create subset of the air dataframe (subset will house domain info)
        air_df_subset = pd.DataFrame(columns=['domain'])
        # create the domain column from the source_url info available
        air_df_subset['domain'] = air_out_deduplicated_df.\
            apply(lambda row: urllib.parse.\
                    urlparse(row['source_url']).hostname.\
                        replace('www2.', 'www.').replace('www.', ''), axis=1)
        # get the 'source_url' renamed as 'page'
        air_df_subset['page'] = air_out_deduplicated_df['source_url']
        # to get the number of resources retrieved from each page, perform groupby
        grouped = air_df_subset.groupby(['domain', 'page'])
        # create dataframe to store aggreated resource info
        dataframe = pd.DataFrame(columns=['domain', 'page'])
        dataframe['domain'] = [domain for domain, page in grouped.indices.keys()]
        dataframe['page'] = [page for domain, page in grouped.indices.keys()]
        # get the size of each group
        # this value represents the number of resources gotten per page
        dataframe['resource per page'] = list(grouped.size().values)

        # if 'ordered' is True, sorted the df by 'resource count' in descending order
        if ordered:
            dataframe.sort_values(by='resource per page', axis='index',
                                           ascending=False, inplace=True,
                                           ignore_index=True)

        # write the dataframe to an excel sheet
        if os.path.exists(METRICS_OUTPUT_PATH): # check if excel sheet exist
            writer_mode = 'a' # set write mode to append
        else:
            writer_mode = 'w' # set write mode to write
        with pd.ExcelWriter(METRICS_OUTPUT_PATH, engine="openpyxl",
                            mode=writer_mode) as writer:
            dataframe.to_excel(writer,
                                        sheet_name='RESOURCE COUNT PER PAGE (AIR)',
                                        index=False, engine='openpyxl')
        return dataframe
        
    else:
        raise ValueError('invalid "scraper" provided')


def data_json_compare(scraper='datopian', 
                      compare_with_path='https://www2.ed.gov/data.json'):
    """ function compares/measures the differences between data resources
    collected by 'datopian' scraper and resources listen in a data.json file.
    
    function uses the json schema provided by ed.gov/data.json to construct
    a dataframe to be used for comparison"""
    
    # check that scraper provided is 'datopian'
    if scraper.upper() != "DATOPIAN":
        raise ValueError('invalid "scraper" provided')

    # check if an appropriate path is provided
    if urllib.parse.urlparse(compare_with_path).scheme == "" and\
        os.path.isfile(compare_with_path) == False:
        raise ValueError('invalid "compare_with_path" provided')

    # load the data.json for comparison
    if urllib.parse.urlparse(compare_with_path).scheme != "": # remote file
        # use requests to load json
        data_json = requests.get(compare_with_path, verify=False).json()
    elif os.path.isfile(compare_with_path) == True: # local file
        # json module to load json
        data_json = json.load(open(compare_with_path, mode='r'))

    # normalise the json for pd dataframe
    # filter out non-useful datasets i.e. datasets that don't contain resources
    data_json = filter(h.filter_data_json_datasets, data_json['dataset'])

    # map the iteratable contained in data_json to
    # a list of lists (2-dimensional) which can be used by pd dataframe
    # the list of lists contain the url of every resource from each dataset
    data_json = map(h.map_data_json_resources_to_lists, data_json)
    data_json = functools.reduce(lambda index1, index2:\
                    (index1.extend(index2) or index1), data_json, [])
    data_json = functools.reduce(lambda index1, index2:\
                    (index1.append([index2]) or index1), data_json, [])
    # crate a dataframe from the dataset resources of data.json
    data_json_df = pd.DataFrame(data_json, columns=['url'])
    
    # get the resources EXCLUSIVE to edgov/data.json
    dataframe = pd.DataFrame(columns=['url'])
    dataframe['url'] = datopian_out_df['url']

    dataframe = pd.concat([data_json_df,
        dataframe, dataframe], axis='index', ignore_index=True)
    # remove duplicate rows
    dataframe.drop_duplicates(subset=['url'], keep=False,
                                        inplace=True)
    
    # write the dataframes to an excel sheet
    if os.path.exists(METRICS_OUTPUT_PATH): # check if excel sheet exist
        writer_mode = 'a' # set write mode to append
    else:
        writer_mode = 'w' # set write mode to write
    with pd.ExcelWriter(METRICS_OUTPUT_PATH, engine="openpyxl",
                        mode=writer_mode) as writer:
        data_json_df.to_excel(writer,
                                    sheet_name='ALL EDGOV RESOURCES',
                                    index=False, engine='openpyxl')
        dataframe.to_excel(writer,
                                    sheet_name='EXCLUSIVE EDGOV RESOURCES',
                                    index=False, engine='openpyxl')
    
    return dataframe # return dataframe with resources EXCLUSIVE to edgov/data.json

