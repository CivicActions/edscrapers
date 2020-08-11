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

from  edscrapers.transformers.base.helpers import traverse_output
from edscrapers.cli import logger


def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

class Statistics():

    METRICS_OUTPUT_PATH = os.path.join(os.getenv('ED_OUTPUT_PATH'), 'tools', 'stats')
    METRICS_OUTPUT_XLSX = os.path.join(os.getenv('ED_OUTPUT_PATH'), 'tools', 'stats', 'metrics.xlsx')


    def __init__(self, delete_all_stats=False):

        if delete_all_stats is True:
            if os.path.exists(self.METRICS_OUTPUT_XLSX): # check if excel sheet exist
                os.remove(self.METRICS_OUTPUT_XLSX) # remove the excel sheet

        if os.path.exists(os.getenv('ED_OUTPUT_PATH') +\
            '/transformers/deduplicate/deduplicated_all.lst'):
            self.deduplicated_list_path = os.getenv('ED_OUTPUT_PATH') +\
            '/transformers/deduplicate/deduplicated_all.lst'
        else:
            self.deduplicated_list_path = None

        self.resource_count_per_page = []
        self.resource_count_per_domain = []
        self.page_count_per_domain = []

    def generate_statistics(self):
        logger.debug("Creating statistics...")
        scraper_outputs_df = self._generate_scraper_outputs_df(use_dump=False)
        self.resource_count_per_page = self.list_resource_count_per_page(scraper_outputs_df)
        self.resource_count_per_domain = self.list_resource_count_per_domain(scraper_outputs_df)
        self.page_count_per_domain = self.list_page_count_per_domain(scraper_outputs_df)
        self.datasets_per_scraper = self.list_datasets_per_scraper()

        print(
            f"Total number of raw datasets: \n {self.datasets_per_scraper}\n",
            f"\n---\n\n",
            f"Total number of pages: {self.page_count_per_domain['page count'].sum()}\n",
            f"\n---\n\n",
            f"Total number of resources: {self.resource_count_per_domain['resource count'].sum()}\n",
            f"\n---\n\n",
            f"Total number of pages by domain: \n{self.page_count_per_domain}\n",
            f"\n---\n\n",
            f"Total number of resources by domain: \n{self.resource_count_per_domain}\n",
            f"\n---\n\n",
        )

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

    # TODO: Imported from the Summary module, needs refactoring to fit in
    def _generate_scraper_outputs_df(self, use_dump=False):

        def abs_url(url, source_url):
            if url.startswith(('../', './', '/')) or not urllib.parse.urlparse(url).scheme:
                full_url = urllib.parse.urljoin(source_url, url)
                return full_url
            else:
                return url

        if self.deduplicated_list_path is None:
            files = traverse_output()
        else:
            try:
                with open(self.deduplicated_list_path, 'r') as fp:
                    files = [pathlib.Path(line.rstrip()) for line in fp]
            except:
                files = traverse_output()

        df_dump = str(pathlib.Path(os.path.join(os.getenv('ED_OUTPUT_PATH'), 'out_df.csv')))
        if use_dump:
            df = pd.read_csv(df_dump)
        else:
            dfs = []
            for fp in files:
                with open(fp, 'r') as json_file:
                    try:
                        j = json.load(json_file)

                        # if it's marked for removal by the sanitizer, skip it
                        if j.get('_clean_data', dict()).get('_remove_dataset'):
                            logger.debug(f"Ignoring {j.get('source_url')}")
                            continue

                        j = [{
                            'url': abs_url(r['url'], r['source_url']),
                            'source_url': r['source_url'],
                            'publisher': str(j['publisher']),
                            'size': r.get('headers', dict()).get('content-length', 0),
                            'scraper': fp.parent.name
                        } for r in j['resources'] if r['source_url'].find('/print/') == -1]

                        dfs.append(pd.read_json(json.dumps(j)))

                    except Exception as e:
                        logger.warning(f'Could not parse file {json_file} as JSON! {e}')
            df = pd.concat(dfs, ignore_index=True)
            df.to_csv(df_dump, index=False)

        return df

    def list_datasets_per_scraper(self, ordered=True):
        """Generate page count per domain

        PARAMETERS
        - ordered: whether the resulting DataFrame or
        Excel sheet result be sorted/ordered. If True, order by 'page count'
        """

        filenames = []
        try:
            with open(self.deduplicated_list_path, 'r') as fp:
                filenames = fp.readlines()
        except:
            logger.warning('Warning! Cannot read deduplication results. Please run deduplicate transformer first')
            filenames = traverse_output()

        scraper_counts = {}
        for filename in filenames:
            scraper_name = str(filename).rstrip().split('/')[-2]
            scraper_counts[scraper_name] = (scraper_counts.get(scraper_name, 0) + 1)

        df = pd.DataFrame(columns=['scraper', 'dataset count'])
        df['scraper'] = list(scraper_counts.keys())
        df['dataset count'] = list(scraper_counts.values())

        if ordered:
            df.sort_values(by='dataset count', axis='index',
                                    ascending=False, inplace=True,
                                    ignore_index=True)

        self._add_to_spreadsheet(sheet_name='DATASET COUNT PER SCRAPER',
                                    result=df)
        return df
    

    def list_page_count_per_domain(self, scraper_outputs_df, ordered=True):
        """Generate page count per domain

        PARAMETERS
        - scraper_outputs_df: dataframe containing scraper outputs,
           generated with the method with the same name
        - ordered: whether the resulting DataFrame or
        Excel sheet result be sorted/ordered. If True, order by 'page count'
        """

        # create a dataframe with duplicate source_urls removed
        df = scraper_outputs_df.\
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

        self._add_to_spreadsheet(sheet_name='PAGE COUNT PER DOMAIN',
                                    result=df_subset)
        return df_subset


    def list_resource_count_per_domain(self, scraper_outputs_df, ordered=True):
        """Generate resource count per domain

        PARAMETERS
        - scraper_outputs_df: dataframe containing scraper outputs,
           generated with the method with the same name
        - ordered: whether the resulting DataFrame or
        Excel sheet result be sorted/ordered. If True, order by 'resource per domain'
        """

        # create a dataframe with duplicate url and source_urls removed
        df_deduplicated_df = scraper_outputs_df.\
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

    def list_resource_count_per_page(self, scraper_outputs_df, ordered=True,):
        """Determine resources produced/generated from each page

        PARAMETERS
        - scraper_outputs_df: dataframe containing scraper outputs,
           generated with the method with the same name
        - ordered: whether the resulting DataFrame or
        Excel sheet result be sorted/ordered. If True, order by 'resource per page'
        """

        # create a dataframe with duplicate url and source_urls removed
        deduplicated_df = scraper_outputs_df.drop_duplicates(subset=['url', 'source_url'],
                                             inplace=False)
        # create subset of the dataframe (subset will house domain info)
        df_subset = pd.DataFrame(columns=['domain'])
        # create the domain column from the source_url info available
        df_subset['domain'] = deduplicated_df.apply(lambda row: urllib.parse.\
                                       urlparse(row['source_url']).hostname.\
                                       replace('www2.', 'www.').replace('www.', ''), axis=1)

        # get the 'source_url' renamed as 'page'
        df_subset['page'] = deduplicated_df['source_url']

        from edscrapers.scrapers.edgov.offices_map import offices_map
        def _munge_publisher(value):
            try:
                result = eval(value)['name']
                return result.upper()
            except:
                if isinstance(value, dict):
                    result = value['name']
                    return result.upper()
                result = value
                for office_full_name in offices_map.keys():
                    import re
                    regex = re.compile(r'\b' + value + r'\b')
                    if regex.search(office_full_name):
                        result = offices_map[office_full_name]['name']
                return result.upper()

        df_subset['publisher'] = deduplicated_df['publisher']
        # to get the number of resources retrieved from each page, perform groupby
        grouped = df_subset.groupby(['domain', 'page', 'publisher'])
        # create dataframe to store aggreated resource info
        result = pd.DataFrame(columns=['domain', 'page', 'publisher'])
        result['domain'] = [domain for domain, page, publisher in grouped.indices.keys()]
        result['page'] = [page for domain, page, publisher in grouped.indices.keys()]
        result['publisher'] = [_munge_publisher(publisher) for domain, page, publisher in grouped.indices.keys()]
        # get the size of each group
        # this value represents the number of resources gotten per page
        result['resources per page'] = list(grouped.size().values)

        # if 'ordered' is True, sorted the df by 'resource count' in descending order
        if ordered:
            result.sort_values(by='resources per page',
                                axis='index',
                                ascending=False,
                                inplace=True,
                                ignore_index=True)

        self._add_to_spreadsheet(sheet_name='RESOURCE COUNT PER PAGE',
                                result=result)

        return result



    def list_resource_size_per_office(self, scraper_outputs_df):
        """Determine amount of data produced/generated for each publishing office

        PARAMETERS
        - scraper_outputs_df: dataframe containing scraper outputs,
           generated with the method with the same name
        """

        # create a dataframe with duplicate url and source_urls removed
        deduplicated_df = scraper_outputs_df.drop_duplicates(subset=['url', 'source_url'],
                                             inplace=False)
        # create subset of the dataframe (subset will house domain info)
        df_subset = pd.DataFrame(columns=['domain'])
        # create the domain column from the source_url info available
        df_subset['domain'] = deduplicated_df.apply(lambda row: urllib.parse.\
                                       urlparse(row['source_url']).hostname.\
                                       replace('www2.', 'www.').replace('www.', ''), axis=1)

        # get the 'source_url' renamed as 'page'
        df_subset['page'] = deduplicated_df['source_url']

        from edscrapers.scrapers.edgov.offices_map import offices_map
        acronyms_map = {v['name']: {} for v in offices_map.values()}

        for full_name, data_dict in offices_map.items():
            acronyms_map[data_dict['name']] = full_name

        def _munge_publisher(value):
            result = value
            try:
                office_name = eval(value)['name']
            except:
                office_name = value
                if isinstance(value, dict):
                    office_name = value.get('name', 'XXX')
            result = acronyms_map.get(office_name, None)
            if not result:
                for full_name in acronyms_map.values():
                    if str(value).lower() in str(full_name).lower():
                        result = full_name
            return result

        df_subset['publisher'] = deduplicated_df['publisher']
        df_subset['size'] = deduplicated_df['size']
        deduplicated_df['publisher'][deduplicated_df['scraper'] == 'dashboard'] = 'os'
        deduplicated_df['publisher'][deduplicated_df['scraper'] == 'rems'] = 'osss'
        df_subset['publisher'] = deduplicated_df['publisher'].apply(lambda x: _munge_publisher(str(x)))

        # to get the number of resources retrieved from each page, perform groupby
        grouped = df_subset.groupby(['publisher'])
        # create dataframe to store aggreated resource info
        result = pd.DataFrame(columns=['publisher'])
        # result['domain'] = [domain for publisher, domain in grouped.indices.keys()]
        # result['publisher'] = [_munge_publisher(publisher) for publisher in grouped.indices.keys()]
        result['publisher'] = [publisher for publisher in grouped.indices.keys()]

        # import ipdb; ipdb.set_trace()

        result['count per office'] = list(grouped['size'].count().values)
        result['raw size per office'] = list(grouped['size'].sum().values)
        result['size per office'] = result['raw size per office'].apply(lambda x: sizeof_fmt(x))

        # import ipdb; ipdb.set_trace()

        result.sort_values(by='size per office',
                            axis='index',
                            ascending=False,
                            inplace=True,
                            ignore_index=True)

        self._add_to_spreadsheet(sheet_name='RESOURCE SIZE PER OFFICE',
                                result=result)
        # self._add_to_spreadsheet(sheet_name='RAW RESOURCE SIZE PER OFFICE',
        #                          result=df_subset)

        return result
