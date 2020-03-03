import sys
import pathlib
import json
import pandas as pd


def cli(argv):
    try:
        name = argv[1]
    except IndexError:
        name = ''

    try:
        air_csv = argv[2]
    except IndexError:
        air_csv = './tools/data/AIR.csv'

    try:
        air_df = pd.read_csv(air_csv)
        out_df = _generate_output_df(name)
    except Exception as e:
        print(e)

    c1 = _compare_df(air_df, out_df, 'source_url')
    c2 = _compare_df(air_df, out_df, 'url')

    # print(f"source_url: {c1.count()['url']}")
    print(f"url: {c2.count()['url']}")

def _generate_output_df(name):
    results = pathlib.Path(f'./output/{name}').glob('**/*.json')
    files = [f for f in results]

    dfs = []
    for fp in files:
        with open(fp, 'r') as json_file:
            j = json.load(json_file)
            j = [{'url': r['url'], 'source_url': r['source_url']} for r in j['resources']]
            dfs.append(pd.read_json(json.dumps(j)))

    return pd.concat(dfs, ignore_index=True)


def _compare_df(static_df, output_df, key):
    result = static_df.merge(output_df,
                             indicator=True,
                             on=key,
                             how='inner')
    result.drop_duplicates(subset=key,
                           keep=False,
                           inplace=True)
    return result


if __name__ == '__main__':
    cli(sys.argv)
