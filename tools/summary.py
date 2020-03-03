import sys
import pathlib
import json
import pandas as pd
from terminaltables import GithubFlavoredMarkdownTable as ght

from edscrapers.scrapers.base import helpers


class Summary():

    air_df = None
    out_df = None

    scrapers = ['edgov', 'edoctae', 'edoela', 'edope', 'edopepd', 'edosers', 'ocr', 'oese']
    scrapers_domains = {
        'edgov': r'www2.ed.gov',
        'edoctae': r'ovae|OVAE|octae|OCTAE',
        'edoela': r'oela|ncela',
        'edope': r'ope/',
        'edopepd': r'opepd',
        'edosers': r'osers|osep|idea',
        'ocr': r'ocrdata.ed.gov',
        'oese': r'oese.ed.gov'
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


    def get_resources_table(self, name=''):
        if len(name) > 0:
            data = [['AIR', 'Datasets']]
            table = ght(data)
            table.inner_heading_row_border = False
        else:
            data = [['', 'AIR', 'Datopian', ]]
            for s in self.scrapers:
                data.append([
                    s.upper(),# self.out_df.drop_duplicates(subset='url')[self.out_df.scraper.eq(s)].count()['url']
                    self.air_df[self.air_df.source_url.str.contains(self.scrapers_domains[s])].count()['source_url'],
                    self.out_df[self.out_df.source_url.str.contains(self.scrapers_domains[s])].count()['source_url']
                    # self.out_df[self.out_df.url.str.contains(f"({'|'.join(helpers.get_data_extensions().keys())})$", regex=True, na=False)][self.out_df.scraper.eq(s)].count()['url']
                ])
            table = ght(data)
        return table.table



    def calculate_totals(self):

        self.out_resources_df = self.out_df.url.str.contains(f"({'|'.join(helpers.get_data_extensions().keys())})$", regex=True, na=False)

        self.total['datasets'] = self._get_total_datasets()
        self.total['resources'] = self.out_df[self.out_resources_df].count()['url']
        self.total['resources_and_docs'] = self.out_df.count()['url']
        self.total['air_resources'] = self.air_df.count()['url']
        self.total['urls'] = self.out_df.drop_duplicates(subset='source_url').count()['source_url']
        self.total['air_urls'] = self.air_df.drop_duplicates(subset='source_url').count()['source_url']


    def _get_total_datasets(self, name=''):
        results = pathlib.Path(f'./output/{name}').glob('**/*.json')
        files = [f for f in results]
        return len(files)


    def generate_output_df(self, use_dump=False):
        results = pathlib.Path(f'./output/').glob('**/*.json')
        df_dump = str(pathlib.Path(f'./output/out_df.csv'))
        files = [f for f in results]

        if use_dump:
            df = pd.read_csv(df_dump)
        else:
            dfs = []
            for fp in files:
                with open(fp, 'r') as json_file:
                    j = json.load(json_file)
                    j = [{'url': r['url'], 'source_url': r['source_url'], 'scraper': fp.parent.name} for r in j['resources']]
                    dfs.append(pd.read_json(json.dumps(j)))
            df = pd.concat(dfs, ignore_index=True)
            df.to_csv(df_dump, index=False)

        return df


    def _compare_df(static_df, output_df, key):
        result = static_df.merge(output_df,
                                indicator=True,
                                on=key,
                                how='inner')
        result.drop_duplicates(subset=key,
                            keep=False,
                            inplace=True)
        return result
