import os
import sys
import json

from edscrapers.cli import logger

OUTPUT_PATH = os.getenv('ED_OUTPUT_PATH')
try:
    file_path = os.path.join(OUTPUT_PATH, 'statistics.json')
except TypeError:
    logger.error('ED_OUTPUT_PATH env var not set!')
    sys.exit(1)

def read_json_file():

    try:
        with open(file_path) as json_file:
            data = json.load(json_file)
    except:
        logger.error('Cannot read statistics.json file!')

    return data

def get_stats():
    return read_json_file()

def get_total_datasets_number():
    data = read_json_file()
    return data['total']['datopian']['datasets']

def get_total_datasets_data():

    data = read_json_file()

    datasets = data['total']['datopian']['datasets_by_office']

    return datasets

def get_total_pages_data(source):
    data = read_json_file()
    return sum(data['total'][source]['pages'].values())


def get_total_resources_data():

    data = read_json_file()

    datopian_res_number = data['total']['datopian']['resources']

    return {
        'datopian' : datopian_res_number,
    }

def get_total_resources_by_office(source, is_sorted=True):

    data = read_json_file()
    if is_sorted is False:
        return data['total'][source]['resources_by_office']
    else:
        data = data['total'][source]['resources_by_office'].items()
        return dict(sorted(data, key=lambda item: item[1], reverse=True))

def get_total_pages_by_office(source, is_sorted=True):
    # @FIXME Is this really used anywhere? Seems dead to me...

    data = read_json_file()
    if is_sorted is False:
        return data['total'][source]['pages']
    else:
        data = data['total'][source]['pages'].items()
        return dict(sorted(data, key=lambda item: item[1], reverse=True))

def get_table_rows_by_office(key, is_sorted=True):
    data = read_json_file()
    scrapers = data['total']['datopian']['datasets_by_office'].keys()
    rows = []
    for s in scrapers:
        rows.append({
            's': s,
            'datopian': data['total']['datopian'][key][s]
        })
    if is_sorted is True:
        rows.sort(key=lambda item: item['datopian'], reverse=True)
    return rows

def get_intersection_data():
    data = read_json_file()
    return data['intersections']

def get_datasets_bars_data(is_sorted=True):

    data_list = list()
    total_res_dict = get_total_datasets_data()
    for key, value in total_res_dict.items():
        data_list.append({
            'x': ['Datasets'], 'y': [value],
            'type': 'bar', 'name': key
        })
    if is_sorted is True:
        data_list.sort(key=lambda item: item['y'][0], reverse=True)
    return data_list
