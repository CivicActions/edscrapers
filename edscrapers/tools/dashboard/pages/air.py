# -*- coding: utf-8 -*-
from edscrapers.tools.dashboard.json_parser import (get_stats,
                         get_total_resources_data,
                         get_total_pages_data,
                         get_total_datasets_number,
                         get_total_datasets_data,
                         get_total_resources_by_office,
                         get_total_pages_by_office,
                         get_table_rows_by_office,
                         get_intersection_data)

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

def get_resources_bars_data():

    data_list = list()
    total_res_dict = get_total_resources_data()
    for key, value in total_res_dict.items():
        data_list.append({
            'x': ['Resources'], 'y': [value],
            'type': 'bar', 'name': key
        })
    return data_list

def get_datasets_by_office_pie_data():

    res_dict = get_total_datasets_data()

    return [{
        'labels': list(res_dict.keys()),
        'values': list(res_dict.values()),
        'type': 'pie',
    }]

def get_resources_by_office_pie_data(source):

    res_dict = get_total_resources_by_office(source)

    return [{
        'labels': list(res_dict.keys()),
        'values': list(res_dict.values()),
        'type': 'pie',
    }]

def get_pages_by_office_pie_data(source):

    res_dict = get_total_pages_by_office(source)
    # del res_dict['others']
    # del res_dict['NCES']

    return [{
        'labels': list(res_dict.keys()),
        'values': list(res_dict.values()),
        'type': 'pie',
    }]

def get_resources_by_office_bar_data():

    data_list = list()

    res_datopian_dict = get_total_resources_by_office('datopian')
    res_air_dict = get_total_resources_by_office('air', is_sorted=False)

    # del res_datopian_dict['others']
    # del res_datopian_dict['NCES']
    # del res_air_dict['others']
    # del res_air_dict['NCES']

    data_list.append({
        'x': list(res_datopian_dict.keys()), 
        'y': list(res_datopian_dict.values()), 
        'type': 'bar', 'name': 'Datopian'})

    data_list.append({
        'x': list(res_air_dict.keys()), 
        'y': list(res_air_dict.values()), 
        'type': 'bar', 'name': 'Air'})

    return data_list

def get_pages_by_office_bar_data():

    data_list = list()

    res_datopian_dict = get_total_pages_by_office('datopian')
    res_air_dict = get_total_pages_by_office('air', is_sorted=False)

    # del res_datopian_dict['others']
    # del res_datopian_dict['NCES']
    # del res_air_dict['others']
    # del res_air_dict['NCES']

    data_list.append({
        'x': list(res_datopian_dict.keys()), 
        'y': list(res_datopian_dict.values()), 
        'type': 'bar', 'name': 'Datopian'})

    data_list.append({
        'x': list(res_air_dict.keys()), 
        'y': list(res_air_dict.values()), 
        'type': 'bar', 'name': 'Air'})

    return data_list