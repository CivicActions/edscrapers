import sys
import pathlib
import json
import time
import urllib
import pandas as pd
from terminaltables import GithubFlavoredMarkdownTable as ght

from edscrapers.scrapers.base import helpers


class Summary():

    air_df = None
    out_df = None
    dedup_file = './output/deduplicated_all.lst'

    scrapers = {
        'edgov': r'www2.ed.gov',
        'edoctae': r'ovae|OVAE|octae|OCTAE',
        'edoela': r'oela|ncela',
        'edope': r'/ope/',
        'edopepd': r'\bopepd\b',
        'edosers': r'osers|osep|idea',
        'ocr': r'ocrdata.ed.gov',
        'oese': r'oese.ed.gov',
        'nces': r'\bnces\b',
    }

    total = dict()


    def get_datasets_table(self):
        data = [['Scraper', 'Datasets']]
        for s in self.scrapers:
            data.append([
                s.upper(), self._get_total_datasets(s)
            ])
        table = ght(data)
        return table.table


    def get_datasets_dict(self):
        data = dict()
        for s in self.scrapers:
            data[s.upper()] = int(self._get_total_datasets(s))
        return data

    def get_resources_table(self, name='', column='url'):
        def df_contains(df, regex, key):
            return df[df[key].str.contains(f".*{regex}.*", regex=True)].drop_duplicates(subset=key).count()[key]

        if len(name) > 0:
            data = [['AIR', 'Datasets']]
            table = ght(data)
            table.inner_heading_row_border = False
        else:
            data = [['', 'AIR', 'Datopian', ]]
            for s in self.scrapers.keys():
                data.append([
                    s.upper(),# self.out_df.drop_duplicates(subset='url')[self.out_df.scraper.eq(s)].count()['url']
                    df_contains(self.air_df, self.scrapers[s], column),
                    df_contains(self.out_df, self.scrapers[s], column),
                ])

            data.append([
                'OTHERS',
                self.air_df.count()['url'] - df_contains(self.air_df, '|'.join(self.scrapers.values()), column),
                self.out_df.count()['url'] - df_contains(self.out_df, '|'.join(self.scrapers.values()), column),
            ])
            table = ght(data)

        return table.table


    def get_resources_dict(self, name, column='url'):
        def df_contains(df, regex, key):
            return df[df[key].str.contains(f".*{regex}.*", regex=True)].drop_duplicates(subset=key).count()[key]

        if name == 'air':
            df = self.air_df
        elif name == 'out':
            df = self.out_df

        data = dict()
        for s in self.scrapers.keys():
            data[s.upper()] = int(df_contains(df, self.scrapers[s], column))
        data['others'] = int(df.count()['url'] - df_contains(df, '|'.join(self.scrapers.values()), column))
        return data



    def sanitize_df(self, df):
        rows_to_drop = []
        all_urls = []

        for idx, row in self.out_df.iterrows():
            if '../' in row['url']:
                row['url'] = f"{row['source_url']}/{row['url']}"
            normalized_url = row['source_url'].replace('/www.', '/').replace('/www2.', '/')
            if normalized_url not in all_urls:
                all_urls.append(normalized_url)
            else:
                rows_to_drop.append(idx)
            # if 'print' in row['source_url']:
            #     rows_to_drop.append(idx)

        df.drop(rows_to_drop, inplace=True)


    def calculate_totals(self):

        # print("Sanitizing Datopian data frame... ", end = '', flush=True)
        # self.sanitize_df(self.out_df)
        # print('done.')

        self.total['out_datasets'] = self._get_total_datasets()

        self.total['out_resources'] = self.out_df.count()['url']
        self.total['air_resources'] = self.air_df.count()['url']

        self.total['out_urls'] = self.out_df.drop_duplicates(subset='source_url').count()['source_url']
        self.total['air_urls'] = self.air_df.drop_duplicates(subset='source_url').count()['source_url']


    def _get_total_datasets(self, name=''):
        files = list()
        try:
            with open(self.dedup_file, 'r') as fp:
                if name:
                    files = [line.rstrip() for line in fp if line.rstrip().split('/')[1] == name]
                else:
                    files = [line.rstrip() for line in fp]
        except:
            print('Warning! Cannot read deduplication results!')
            results = pathlib.Path(f'./output/{name}').glob('**/*.json')
            files = [f.name for f in results]

        return len(files)


    def generate_output_df(self, use_dump=False, output_list_file=None):

        def get_files_list():
            results = pathlib.Path(f'./output/').glob('**/*.json')
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

        df_dump = str(pathlib.Path(f'./output/out_df.csv'))
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


    def get_values_only_in(self, df_name='air', column='source_url'):

        # import ipdb; ipdb.set_trace()

        # if df_name == 'air':
        #     merged = self.air_df.merge(self.out_df, on=column, how='left', indicator=True)
        #     result = merged[merged['_merge'] == 'left_only']
        # if df_name == 'out':
        #     merged = self.air_df.merge(self.out_df, on=column, how='right', indicator=True)
        #     result = merged[merged['_merge'] == 'right_only']
        merged = pd.merge(self.air_df, self.out_df, how='inner', left_on=column, right_on=column).count()[column]
        if column == 'source_url':
            if df_name == 'air':
                return self.total['air_urls'] - merged
            if df_name == 'out':
                return self.total['out_urls'] - merged
        if column == 'url':
            if df_name == 'air':
                return self.total['air_resources'] - merged
            if df_name == 'out':
                return self.total['out_resources'] - merged


    def dump(self, path):
        out_csv = pathlib.Path(f'./output/datopian.csv')
        self.out_df.to_csv(out_csv, index=False)
        return out_csv
