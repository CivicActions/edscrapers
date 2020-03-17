""" module provides functions for obtaining
various metrics above the Dept Ed scraping exercise"""

import urllib.parse
import os

import pandas as pd # pip install pandas

from tools.dataset_metrics import datopian_out_df, air_out_df, METRICS_OUTPUT_PATH


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

    # check which scraper domain listing is for
    if scraper.upper() == "DATOPIAN":
        # get all domains visited by datopian but NOT AIR
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
                                        sheet_name='RESOURCE COUNT (DATOPIAN ONLY)',
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
                                        sheet_name='RESOURCE COUNT (AIR ONLY)',
                                        index=False, engine='openpyxl')
                                        
        return air_df_subset