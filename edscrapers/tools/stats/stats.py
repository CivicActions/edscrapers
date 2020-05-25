import json
import sys
import os
import urllib.parse
import functools
import pathlib
import edscrapers
import pandas as pd
import requests

from json.decoder import JSONDecodeError

from edscrapers.cli import logger
from edscrapers.tools.stats import helpers as h
from .air import compare


class Statistics():

    METRICS_OUTPUT_PATH = os.path.join(os.getenv('ED_OUTPUT_PATH'), 'tools', 'stats')
    METRICS_OUTPUT_XLSX = os.path.join(os.getenv('ED_OUTPUT_PATH'), 'tools', 'stats', 'metrics.xlsx')


    def __init__(self, delete_all_stats=False):

        logger.debug("Creating statistics...")
        if delete_all_stats is True:
            if os.path.exists(self.METRICS_OUTPUT_XLSX): # check if excel sheet exist
                os.remove(self.METRICS_OUTPUT_XLSX) # remove the excel sheet
        
        try:
            air_df_path = pathlib.Path(os.getenv('ED_OUTPUT_PATH'),
                                                 'tools', "stats", 'data', 'air_df.csv')
            if not air_df_path.exists(): # if this filepath does not already exist
                air_csv_url = 'https://storage.googleapis.com/storage/v1/b/us-ed-scraping/o/AIR.csv?alt=media'
                req = requests.get(air_csv_url)
                # make the required path/directories
                pathlib.Path.resolve(air_df_path).parent.mkdir(parents=True, exist_ok=True)     
                # write the downloded file to disk       
                with open(air_df_path, 'wb') as air_df_file:
                    air_df_file.write(req.content)

            self.air_out_df = pd.read_csv(
                air_df_path,
                header=0)
        except Exception as e:
            logger.error('Could not load the AIR CSV.')

        try:
            if os.path.exists(os.path.join(os.getenv('ED_OUTPUT_PATH'), 'out_df.csv')):
                self.datopian_out_df = pd.read_csv(
                    os.path.join(os.getenv('ED_OUTPUT_PATH'), 'out_df.csv'),
                    header=0)
            else:
                # create the Datopian CSV
                compare.compare()
                self.datopian_out_df = pd.read_csv(
                    os.path.join(os.getenv('ED_OUTPUT_PATH'), 'out_df.csv'),
                    header=0)
        except Exception as e:
            logger.error('Could not load the Datopian CSV, please generate it first.')
            # read the AIR csv into a dataframe

        


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
