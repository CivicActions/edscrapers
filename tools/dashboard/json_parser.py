import json
import os

file_path =  '../../output/statistics.json'
dirname = os.path.dirname(__file__)
file_path = os.path.join(dirname, file_path)

def read_json_file():

    with open(file_path) as json_file:
        data = json.load(json_file)

    return data

def get_total_resources_data():

    data = read_json_file()

    datopian_res_number = data['total']['datopian']['resources']
    air_res_number = data['total']['air']['resources']

    return {
        'Datopian' : datopian_res_number,
        'Air' : air_res_number
    }

def get_total_resources_by_office(source):

    data = read_json_file()
    return data['total'][source]['resources_by_office']

def get_total_pages_by_office(source):

    data = read_json_file()
    return data['total'][source]['pages']
    
