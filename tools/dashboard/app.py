# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

from venn_diagram import venn_figure
from json_parser import (get_total_resources_data, 
                        get_total_resources_by_office)

def get_resources_bars_data():

    data_list = list()
    total_res_dict = get_total_resources_data()
    for key, value in total_res_dict.items():
        data_list.append({
            'x': ['Resources'], 'y': [value], 
            'type': 'bar', 'name': key
        })
    return data_list

def get_resources_by_office_pie_data(source):

    res_dict = get_total_resources_by_office(source)
    
    return [{
        'labels': list(res_dict.keys()),
        'values': list(res_dict.values()),
        'type': 'pie',
    }]

def get_resources_by_office_bar_data():

    data_list = list()

    res_datopian_dict = get_total_resources_by_office('datopian')
    res_air_dict = get_total_resources_by_office('air')

    data_list.append({
        'x': list(res_datopian_dict.keys()), 
        'y': list(res_datopian_dict.values()), 
        'type': 'bar', 'name': 'Datopian'})

    data_list.append({
        'x': list(res_air_dict.keys()), 
        'y': list(res_air_dict.values()), 
        'type': 'bar', 'name': 'Air'})

    return data_list

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Scraping Dashboard'),

    html.Div(children='''
        Department of Education
    '''),

    dcc.Graph(
        id='bar-graph',
        figure={
            'data': get_resources_bars_data(),
            'layout': {
                'title': 'Total number of Resources'
            }
        }
    ),

    dcc.Graph(
        id='bar-graph-resources',
        figure={
            'data': get_resources_by_office_bar_data(),
            'layout': {
                'title': 'Total number of Resources by Office'
            }
        }
    ),

    dcc.Graph(
        id='pie-graph-datopian',
        figure={
            'data': get_resources_by_office_pie_data('datopian'),
            'layout': {
                'title': 'Total number of Resources by Office - Datopian'
            }
        }
    ),

    dcc.Graph(
        id='pie-graph-air',
        figure={
            'data': get_resources_by_office_pie_data('air'),
            'layout': {
                'title': 'Total number of Resources by Office - Air'
            }
        }
    ),

    dcc.Graph(
        id='venn-graph',
        figure=venn_figure("Datopian: 185", "8326", "Air: 31682")
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)