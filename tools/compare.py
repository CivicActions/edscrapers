from os import system, name, path
import sys
import json
import pandas as pd
from terminaltables import GithubFlavoredMarkdownTable as ght

from .summary import Summary


def compare():
    air_csv = './tools/data/AIR.csv'

    summary = Summary()

    if path.exists('./output/deduplicated_all.lst'):
        output_list_file = './output/deduplicated_all.lst'
    else:
        output_list_file = None

    try:
        print("Generating AIR data frame... ", end = '', flush=True)
        summary.air_df = pd.read_csv(air_csv)
        print('done.')
        print("Generating Datopian data frame... ", end = '', flush=True)
        try:
            summary.out_df = summary.generate_output_df(use_dump=True, output_list_file=output_list_file)
        except:
            summary.out_df = summary.generate_output_df(use_dump=False, output_list_file=output_list_file)
        print('done.')
    except Exception as e:
        print(e)

    summary.calculate_totals()

    # if name == 'nt':
    #     _ = system('cls')
    # else:
    #     _ = system('clear')

    statistics = {
        'total': {
            'datopian': {
                'datasets': int(summary.total['out_datasets']),
                'resources': int(summary.total['out_resources']),
                'pages': summary.get_resources_dict('out', 'source_url'),
                'datasets_by_office': summary.get_datasets_dict(),
                'resources_by_office': summary.get_resources_dict('out', 'url')
            },
            'air': {
                'datasets': 0,
                'resources': int(summary.total['air_resources']),
                'pages': summary.get_resources_dict('air', 'source_url'),
                'resources_by_office': summary.get_resources_dict('air', 'url')
            }
        },
        'intersections': {
            'datopian_only': {
                'pages': int(summary.get_values_only_in('out', 'source_url')),
                'resources': int(summary.get_values_only_in('out', 'url'))
            },
            'air_only': {
                'pages': int(summary.get_values_only_in('air', 'source_url')),
                'resources': int(summary.get_values_only_in('air', 'url'))
            }
        }
    }

    print(
        f"Total number of raw datasets: {summary.total['out_datasets']}\n"
        f"\n---\n\n"
        f"Total number of raw datasets per scraper: \n\n{summary.get_datasets_table()}\n"
        f"\n---\n\n"
        f"Total number of resources:\n"
        f"     AIR: {summary.total['air_resources']}\n"
        f"Datopian: {summary.total['out_resources']}\n"
        f"\n---\n\n"
        f"Total number of resources by office: \n{summary.get_resources_table(column='url')}\n"
        f"\n---\n\n"
        f"Total number of pages by office: \n{summary.get_resources_table(column='source_url')}\n"
        f"\n---\n\n"
        f"Pages scraped by AIR only: {summary.get_values_only_in('air', 'source_url')}\n"
        f"Pages scraped by Datopian only: {summary.get_values_only_in('out', 'source_url')}\n"
        f"\n---\n"
        f"Resources collected by AIR only: {summary.get_values_only_in('air', 'url')}\n"
        f"Resources collected by Datopian only: {summary.get_values_only_in('out', 'url')}\n"
        f"\n---\n\n"
        f"CSV file with all the resources was dumped in {summary.dump('./output/datopian.csv')}"
    )

    with open('./output/statistics.json', 'w') as stats_file:
        json.dump(statistics, stats_file)


if __name__ == '__main__':
    cli(sys.argv)
