import json
import sys
import os
import urllib.parse
import functools
import edscrapers
import pandas as pd
import requests

from json.decoder import JSONDecodeError

from edscrapers.cli import logger
from edscrapers.tools.stats import helpers as h


class Statistics():

    METRICS_OUTPUT_PATH = os.path.join(os.getenv('ED_OUTPUT_PATH'), 'tools', 'stats')
    METRICS_OUTPUT_XLSX = os.path.join(os.getenv('ED_OUTPUT_PATH'), 'tools', 'stats', 'metrics.xlsx')


    def __init__(self):

        logger.debug("Creating statistics...")

        if os.path.exists(self.METRICS_OUTPUT_XLSX): # check if excel sheet exist
            os.remove(self.METRICS_OUTPUT_XLSX) # remove the excel sheet

        try:
            self.datopian_out_df = pd.read_csv(
                os.path.join(os.getenv('ED_OUTPUT_PATH'), 'out_df.csv'),
                header=0)
        except Exception as e:
            logger.error('Cold not load the Datopian CSV, please generate it first.')
            # read the AIR csv into a dataframe

        try:
            air_csv_url = 'https://storage.googleapis.com/storage/v1/b/us-ed-scraping/o/AIR.csv?alt=media'
            req = requests.get(air_csv_url)
            with open(os.path.join(
                    os.getenv('ED_OUTPUT_PATH'), 'tools', 'stats', 'data', 'air_df.csv'
            ), 'wb') as air_df_file:
                air_df_file.write(req.content)

            self.air_out_df = pd.read_csv(
                os.path.join(os.getenv('ED_OUTPUT_PATH'), 'tools', 'stats', 'data', 'air_df.csv'),
                header=0)
        except Exception as e:
            logger.error('Cold not load the AIR CSV.')


    def _add_to_spreadsheet(self, sheet_name, result):
        # write the result (dataframe) to an excel sheet
        if os.path.exists(self.METRICS_OUTPUT_XLSX): # check if excel sheet exist
            writer_mode = 'a' # set write mode to append
        else:
            writer_mode = 'w' # set write mode to write
        with pd.ExcelWriter(self.METRICS_OUTPUT_XLSX, engine="openpyxl",
                            mode=writer_mode) as writer:
            result.to_excel(writer,
                            sheet_name=sheet_name,
                            index=False,
                            engine='openpyxl')
        pass

    def to_json(self, stats_dict):
        """Create a JSON output from the provided stats dictionary
        """
        pass

    def to_xlsx(self):
        pass
    def to_ascii(self, stats_dict):
        """Create an ASCII output from the provided stats dictionary
        """
        pass


    def get_compare_dict(self):
        json_url = 'https://storage.googleapis.com/storage/v1/b/us-ed-scraping/o/compare-statistics.json?alt=media'
        json_s3_file = os.path.join(os.getenv('ED_OUTPUT_PATH'),
                                    'tools', 'stats', 's3_compare-statistics.json')
        json_local_file = os.path.join(os.getenv('ED_OUTPUT_PATH'), 'statistics.json')

        try:
            req = requests.get(json_url)
            req.raise_for_status()
            with open(json_s3_file, 'wb') as json_file:
                json_file.write(req.content)
        except:
            pass

        try:
            result = json.loads(json_s3_file)
        except JSONDecodeError:
            try:
                with open(json_local_file) as json_file:
                    result = json.load(json_file)
            except FileNotFoundError:
                logger.error('Comparison statistics JSON not found!')
                raise

        return result


    def generate_datopian_df(self, use_dump=False, output_list_file=None):

        def get_files_list():
            results = pathlib.Path(os.path.join(self.output_path, 'scrapers')).glob('**/*.json')
            return [f for f in results]

        def abs_url(url, source_url):
            if url.startswith(('../', './', '/')) or not urllib.parse.urlparse(url).scheme:
                full_url = urllib.parse.urljoin(source_url, url)
                return full_url
            else:
                return url

        if output_list_file is None:
            files = get_files_list()
        else:
            try:
                with open(output_list_file, 'r') as fp:
                    files = [pathlib.Path(line.rstrip()) for line in fp]
            except:
                files = get_files_list()

        df_dump = str(pathlib.Path(os.path.join(self.output_path, 'out_df.csv')))
        if use_dump:
            df = pd.read_csv(df_dump)
        else:
            dfs = []
            for fp in files:
                # TODO refactor these rules or the files structure
                if 'data.json' in str(fp):
                    continue
                if 'statistics.json' in str(fp):
                    continue

                with open(fp, 'r') as json_file:
                    j = json.load(json_file)
                    j = [{
                        'url': abs_url(r['url'], r['source_url']),
                        'source_url': r['source_url'],
                        'scraper': fp.parent.name
                    } for r in j['resources'] if r['source_url'].find('/print/') == -1]
                    dfs.append(pd.read_json(json.dumps(j)))
            df = pd.concat(dfs, ignore_index=True)
            df.to_csv(df_dump, index=False)

        # import ipdb; ipdb.set_trace()
        return df


    def list_domain(self, provider='datopian', ordered=True):
        """function is used to list the domains scraped by
        'provider'. Optionally order these domains
        by number of pages parsed if 'ordered' is True """

        if provider.upper() == "DATOPIAN":
            # create a dataframe with duplicate source_urls removed
            df = self.datopian_out_df.\
                drop_duplicates(subset='source_url', inplace=False)
        elif provider.upper() == "AIR":
            df = self.air_out_df.\
                drop_duplicates(subset='source_url', inplace=False)
        else:
            raise ValueError('invalid "provider" provided')

        # create subset of the datopian dataframe (subset will house domain info)
        df_subset = pd.DataFrame(columns=['domain'])
        # create the domain column from the source_url info available
        df_subset['domain'] = df.\
            apply(lambda row: urllib.parse.\
                    urlparse(row['source_url']).hostname.\
                        replace('www2.', 'www.').replace('www.', ''), axis=1)
        # to get the number of pages visited from each domain, perform groupby
        grouped = df_subset.groupby(['domain'])
        # recreate the datopian dataframe subset to store aggreated domain info
        df_subset = pd.DataFrame(columns=['domain'])
        # get the keys/names for grouped domains
        df_subset['domain'] = list(grouped.indices.keys())
        # get the size of each group
        # i.e. the number of times each domain appeared in the non-grouped dataframe
        # this value represents the number of pages visited
        df_subset['page count'] = list(grouped.size().values)

        # if 'ordered' is True, sorted the df by 'page count' in descending order
        if ordered:
            df_subset.sort_values(by='page count', axis='index',
                                    ascending=False, inplace=True,
                                    ignore_index=True)

            self._add_to_spreadsheet(sheet_name='PAGE COUNT (DATOPIAN)',
                                     result=df_subset)
        return df_subset


    def list_exclusive_domain(self, provider='datopian', compare_provider='air', ordered=True):
        """ function is used to determine what domains were
        EXCLUSIVELY visited by 'provider' and NOT by 'compare_provider' .
        If 'ordered' is True, dataframe is sorted by 'resource count' """

        def create_df_subset(df):
            # create a datopian dataframe with duplicate url and source_urls removed
            df_deduplicated_df = df.\
                drop_duplicates(subset=['url', 'source_url'], inplace=False)
            # create subset of the df dataframe (subset will house domain info)
            df_subset = pd.DataFrame(columns=['domain'])
            # create the domain column from the source_url info available
            df_subset['domain'] = df_deduplicated_df.\
                apply(lambda row: urllib.parse.\
                        urlparse(row['source_url']).hostname.\
                            replace('www2.', 'www.').replace('www.', ''), axis=1)
            # to get the number of pages visited from each domain, perform groupby
            grouped = df_subset.groupby(['domain'])
            # recreate the datopian dataframe subset to store aggreated domain info
            df_subset = pd.DataFrame(columns=['domain'])
            # get the keys/names for grouped domains
            df_subset['domain'] = list(grouped.indices.keys())
            # get the size of each group
            # i.e. the number of times each domain appeared in the non-grouped dataframe
            # this value represents the number of resources visited
            df_subset['resource count'] = list(grouped.size().values)
            return df_subset

        datopian_df_subset = create_df_subset(self.datopian_out_df)
        air_df_subset = create_df_subset(self.air_out_df)

        df_subset_map = {
            'datopian': datopian_df_subset,
            'air': air_df_subset
        }

        if provider.lower() in df_subset_map.keys():
            # Get the requested df (i.e. datopian_df_subset
            df1_subset = df_subset_map.pop(provider.lower())
            # Now get the other one
            df2_subset = next(iter(df_subset_map.values()))

            # get all domains visited by df1 but NOT df2.
            # We use the trick of concatenating 'df2_subset' twice.
            # This is to ensure that when remove duplicates
            # in later step all rows from 'df2_subset' will
            # ALWAYS be removed.
            df1_subset = pd.concat([df1_subset,
            df2_subset, df2_subset], axis='index', ignore_index=True)
            # remove duplicate rows
            df1_subset.drop_duplicates(subset=['domain'], keep=False,
                                            inplace=True)

            # if 'ordered' is True, sorted the df by 'resource count' in descending order
            if ordered:
                df1_subset.sort_values(by='resource count', axis='index',
                                            ascending=False, inplace=True,
                                            ignore_index=True)

            self._add_to_spreadsheet(sheet_name='RESOURCE COUNT PER DOMAIN (DATOPIAN ONLY)',
                                     result=df1_subset)
            return df1_subset

        else:
            raise ValueError('invalid "provider" provided')


    def list_intersection_domain(self, provider='datopian', compare_provider='air', ordered=True):
        """ function is used to determine what domains were
        BOTH visited by 'provider' AND 'compare_provider' .
        If 'ordered' is True, dataframe is sorted by 'resource count' """

        if (provider.upper() != "DATOPIAN" and compare_provider.upper() != "AIR")\
            and (provider.upper() != "AIR" and compare_provider.upper() != "DATOPIAN"):
            raise ValueError('invalid "provider" or "compare_provider" provided')

        # create a datopian dataframe with duplicate url and source_urls removed
        datopian_out_deduplicated_df = self.datopian_out_df.\
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
        air_out_deduplicated_df = self.air_out_df.\
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

        self._add_to_spreadsheet(sheet_name='RESOURCE COUNT PER DOMAIN (DATOPIAN-AIR INTERSECTION)',
                                 result=merged_df)
        return merged_df


    def list_highest_resources_from_pages(self, provider='datopian', ordered=True):
        """ function is used to determine what pages from a particular
        provider produced/generated the highest number of resources.

        PARAMETERS
        - provider: the provider that was run on the domains to generate the 
        datasets e.g. DATOPIAN or AIR

        - ordered: whether the resulting DataFrame or 
        Excel sheet result be sorted/ordered. If True, order by 'resource per page'
        """

        df_map = {
            'datopian': self.datopian_out_df,
            'air': self.air_out_df
        }

        try:
            df = df_map[str(provider.lower())]
        except:
            raise ValueError('invalid "provider" value')

        # create a dataframe with duplicate url and source_urls removed
        deduplicated_df = df.drop_duplicates(subset=['url', 'source_url'],
                                             inplace=False)
        # create subset of the dataframe (subset will house domain info)
        df_subset = pd.DataFrame(columns=['domain'])
        # create the domain column from the source_url info available
        df_subset['domain'] = df.apply(lambda row: urllib.parse.\
                                       urlparse(row['source_url']).hostname.\
                                       replace('www2.', 'www.').replace('www.', ''), axis=1)


        # get the 'source_url' renamed as 'page'
        df_subset['page'] = deduplicated_df['source_url']
        # to get the number of resources retrieved from each page, perform groupby
        grouped = df_subset.groupby(['domain', 'page'])
        # create dataframe to store aggreated resource info
        result = pd.DataFrame(columns=['domain', 'page'])
        result['domain'] = [domain for domain, page in grouped.indices.keys()]
        result['page'] = [page for domain, page in grouped.indices.keys()]
        # get the size of each group
        # this value represents the number of resources gotten per page
        result['resource per page'] = list(grouped.size().values)

        # if 'ordered' is True, sorted the df by 'resource count' in descending order
        if ordered:
            result.sort_values(by='resource per page',
                                  axis='index',
                                  ascending=False,
                                  inplace=True,
                                  ignore_index=True)

        self._add_to_spreadsheet(sheet_name='RESOURCE COUNT PER PAGE (DATOPIAN)',
                                 result=result)

        return result
