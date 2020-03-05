from os import system, name
import sys
import pandas as pd
from terminaltables import GithubFlavoredMarkdownTable as ght

from .summary import Summary


def cli(argv):
    try:
        air_csv = argv[1]
    except IndexError:
        air_csv = './tools/data/AIR.csv'

    summary = Summary()

    try:
        print("Generating AIR data frame... ", end = '', flush=True)
        summary.air_df = pd.read_csv(air_csv)
        print('done.')
        print("Generating Datopian data frame... ", end = '', flush=True)
        try:
            summary.out_df = summary.generate_output_df(use_dump=True)
        except:
            summary.out_df = summary.generate_output_df(use_dump=False)
        print('done.')
    except Exception as e:
        print(e)

    summary.calculate_totals()

    # if name == 'nt':
    #     _ = system('cls')
    # else:
    #     _ = system('clear')

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
        f"{summary.total}"
    )



if __name__ == '__main__':
    cli(sys.argv)
