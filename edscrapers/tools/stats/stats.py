import json
import sys
import os
import re
import urllib.parse
import functools
import pathlib
import edscrapers
import pandas as pd
import requests

from json.decoder import JSONDecodeError

from edscrapers.cli import logger


SCRAPERS =  {
    'edgov': r'www2.ed.gov',
    'fsa': r'studentaid.gov',
    'octae': r'ovae|OVAE|octae|OCTAE',
    'oela': r'oela|ncela',
    'ope': r'/ope/',
    'opepd': r'\bopepd\b',
    'osers': r'osers|osep|idea',
    'ocr': r'ocrdata.ed.gov',
    'oese': r'oese.ed.gov',
    'nces': r'\bnces\b',
}

class Statistics():

    METRICS_OUTPUT_PATH = os.path.join(os.getenv('ED_OUTPUT_PATH'), 'tools', 'stats')
    METRICS_OUTPUT_XLSX = os.path.join(os.getenv('ED_OUTPUT_PATH'), 'tools', 'stats', 'metrics.xlsx')


    def __init__(self, delete_all_stats=False):

        logger.debug("Creating statistics...")
        if delete_all_stats is True:
            if os.path.exists(self.METRICS_OUTPUT_XLSX): # check if excel sheet exist
                os.remove(self.METRICS_OUTPUT_XLSX) # remove the excel sheet

        if os.path.exists(os.getenv('ED_OUTPUT_PATH') +\
            '/transformers/deduplicate/deduplicated_all.lst'):

            self.deduplicated_list_path = os.getenv('ED_OUTPUT_PATH') +\
            '/transformers/deduplicate/deduplicated_all.lst'
        else:
            self.deduplicated_list_path = None

        self.datopian_out_df = self._generate_datopian_df(use_dump=False)
        # self.resource_count_per_page = self.list_resource_count_per_page()
        self.resource_count_per_domain = self.list_resource_count_per_domain()
        self.page_count_per_domain = self.list_page_count_per_domain()

    def generate_statistics(self):
        statistics = {
            'total': {
                'datopian': {
                    'datasets': self._get_total_datasets(),
                    'resources': int(self.resource_count_per_domain['resource count'].sum()),
                    'pages': self.format_dataframe_results(self.page_count_per_domain),
                    'resources_by_office': self.format_dataframe_results(self.resource_count_per_domain),
                    'datasets_by_office': self.get_datasets_dict(),
                }
            }
        }

        print(
            f"Total number of raw datasets: {statistics['total']['datopian']['datasets']}\n",
            f"\n---\n\n",
            f"Total number of pages: {statistics['total']['datopian']['pages']}\n",
            f"\n---\n\n",
            f"Total number of resources: {statistics['total']['datopian']['resources']}\n",
            f"\n---\n\n",
            f"Total number of resources by domain: \n{self.resource_count_per_domain}\n",
            f"\n---\n\n",
            f"Total number of pages by domain: \n{self.page_count_per_domain}\n",
            f"\n---\n\n",
        )

        with open(f"{os.getenv('ED_OUTPUT_PATH')}/statistics.json", 'w') as stats_file:
            json.dump(statistics, stats_file)

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

    def format_dataframe_results(self, df):
        results = {}

        for row in df.to_dict('records'):
            matching = { key: value for key, value in SCRAPERS.items() if re.match(value, row['domain']) }
            if matching.keys():
                matching_domain = list(matching.keys())[0].upper()
                results[matching_domain] = list(row.values())[1]
            else:
                continue
        return results

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

    # TODO: Imported from the Summary module, needs refactoring to fit in
    def _generate_datopian_df(self, use_dump=False):

        def get_files_list():
            results = pathlib.Path(os.path.join(os.getenv('ED_OUTPUT_PATH'), 'scrapers')).glob('**/*.json')
            return [f for f in results]

        def abs_url(url, source_url):
            if url.startswith(('../', './', '/')) or not urllib.parse.urlparse(url).scheme:
                full_url = urllib.parse.urljoin(source_url, url)
                return full_url
            else:
                return url

        if self.deduplicated_list_path is None:
            files = get_files_list()
        else:
            try:
                with open(self.deduplicated_list_path, 'r') as fp:
                    files = [pathlib.Path(line.rstrip()) for line in fp]
            except:
                files = get_files_list()

        df_dump = str(pathlib.Path(os.path.join(os.getenv('ED_OUTPUT_PATH'), 'out_df.csv')))
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

        return df


    # TODO: Imported from the Summary module, needs refactoring to fit in
    def _get_total_datasets(self, name=''):
        files = list()
        try:
            with open(self.deduplicated_list_path, 'r') as fp:
                if name:
                    files = [line.rstrip() for line in fp if line.rstrip().split('/')[-2] == name]
                else:
                    files = [line.rstrip() for line in fp]
        except:
            # TODO ENABLE print('Warning! Cannot read deduplication results!')
            results = pathlib.Path(os.path.join(os.getenv('ED_OUTPUT_PATH'), 'scrapers', name)).glob('**/*.json')
            files = [f.name for f in results]

        return len(files)

    # TODO: Imported from the Summary module, needs refactoring to fit in
    def get_datasets_dict(self):
        data = dict()
        for scraper in SCRAPERS:
            data[scraper.upper()] = int(self._get_total_datasets(scraper))
        return data

    def list_page_count_per_domain(self, ordered=True):
        """Generate page count per domain

        PARAMETERS
        - ordered: whether the resulting DataFrame or
        Excel sheet result be sorted/ordered. If True, order by 'page count'
        """

        # create a dataframe with duplicate source_urls removed
        df = self.datopian_out_df.\
            drop_duplicates(subset='source_url', inplace=False)

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

            self._add_to_spreadsheet(sheet_name='PAGE COUNT',
                                     result=df_subset)
        return df_subset


    def list_resource_count_per_domain(self, ordered=True):
        """Generate resource count per domain

        PARAMETERS
        - ordered: whether the resulting DataFrame or
        Excel sheet result be sorted/ordered. If True, order by 'resource per domain'
        """

        # create a dataframe with duplicate url and source_urls removed
        df_deduplicated_df = self.datopian_out_df.\
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

        if ordered:
            df_subset.sort_values(by='resource count', axis='index',
                                        ascending=False, inplace=True,
                                        ignore_index=True)

        self._add_to_spreadsheet(sheet_name='RESOURCE COUNT PER DOMAIN',
                                    result=df_subset)
        return df_subset

    def list_resource_count_per_page(self, ordered=True):
        """Determine resources produced/generated from each page

        PARAMETERS
        - ordered: whether the resulting DataFrame or
        Excel sheet result be sorted/ordered. If True, order by 'resource per page'
        """

        # create a dataframe with duplicate url and source_urls removed
        deduplicated_df = self.datopian_out_df.drop_duplicates(subset=['url', 'source_url'],
                                             inplace=False)
        # create subset of the dataframe (subset will house domain info)
        df_subset = pd.DataFrame(columns=['domain'])
        # create the domain column from the source_url info available
        df_subset['domain'] = self.datopian_out_df.apply(lambda row: urllib.parse.\
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

        self._add_to_spreadsheet(sheet_name='RESOURCE COUNT PER PAGE',
                                 result=result)

        return result
