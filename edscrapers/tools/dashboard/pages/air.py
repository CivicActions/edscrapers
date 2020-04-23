# -*- coding: utf-8 -*-
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html

from edscrapers.tools.dashboard.venn_diagram import venn_figure
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


def generate_layout():
    return html.Div(children=[
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
        id='bar-graph-pages',
        figure={
            'data': get_pages_by_office_bar_data(),
            'layout': {
                'title': 'Total number of Pages by Office'
            }
        }
    ),

    dcc.Graph(
        id='pie-graph-pages-datopian',
        figure={
            'data': get_pages_by_office_pie_data('datopian'),
            'layout': {
                'title': 'Total number of Pages by Office - Datopian'
            }
        }
    ),

    dcc.Graph(
        id='pie-graph-pages-air',
        figure={
            'data': get_pages_by_office_pie_data('air'),
            'layout': {
                'title': 'Total number of Pages by Office - Air'
            }
        }
    ),

    dcc.Graph(
        id='venn-graph',
        figure=venn_figure(
            'Datopian only: ' + str(get_intersection_data()['datopian_only']['resources']),
            'AIR only: ' + str(get_intersection_data()['air_only']['resources']),
            get_total_resources_data()['datopian'] - get_intersection_data()['datopian_only']['resources'],
        ),
    )
])


def generate_split_layout():
    return html.Div(children=[
    #     html.Img(src='https://www.datopian.com/img/datopian-logo.svg', style={'width': 200, 'float': 'right', 'margin': 20}),
    #     html.Img(src='https://i.stack.imgur.com/wSpIb.png', style={'width': 200, 'float': 'right', 'margin': 20}),
    # html.H1(children='Scraping Dashboard'),

    # html.Hr(),
    
    html.Div([
        dcc.Graph(figure={'data': get_datasets_bars_data(),
                'layout': {'title': 'Datasets by scraper'}}),
    ], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Div([
        html.H1(children=get_total_datasets_number(), style={'text-align': 'center', 'font-weight': 'bold'}),
        html.H4(children='TOTAL DATASETS', style={'text-align': 'center'}),
    ], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}),


    html.Hr(),

    html.Div([
        html.H4(children='TOTAL NUMBER OF RESOURCES', style={'text-align': 'center'}),
    ]),
    html.Div([
        html.H1(children=get_stats()['total']['air']['resources'], style={'text-align': 'center', 'font-weight': 'bold'}),
        html.H4(children='AIR', style={'text-align': 'center'}),
    ], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Div([
        html.H1(children=get_stats()['total']['datopian']['resources'], style={'text-align': 'center', 'font-weight': 'bold'}),
        html.H4(children='DATOPIAN', style={'text-align': 'center'}),
    ], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}),

    html.Hr(),

    dcc.Graph(
        figure={'data': get_resources_by_office_bar_data(),
            'layout': {'title': 'Total number of Resources by Office'}},
        style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}
    ),
    html.Div([],
        style={'width': '9%', 'display': 'inline-block', 'vertical-align': 'middle'}
    ),
    html.Div([
        dash_table.DataTable(
            columns=[{'name': '', 'id': 's'}, {'name': 'AIR', 'id': 'air'}, {'name': 'Datopian', 'id': 'datopian'}],
            data=get_table_rows_by_office('resources_by_office'),
            sort_action='native',
            style_cell={'textAlign': 'left'},
        )],
        style={'width': '39%', 'display': 'inline-block', 'vertical-align': 'middle'}
    ),

    html.Hr(),

    dcc.Graph(
        figure={'data': get_pages_by_office_bar_data(),
            'layout': {'title': 'Total number of pages by office'}},
        style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}
    ),
    html.Div([],
        style={'width': '9%', 'display': 'inline-block', 'vertical-align': 'middle'}
    ),
    html.Div([
        dash_table.DataTable(
            columns=[{'name': '', 'id': 's'}, {'name': 'AIR', 'id': 'air'}, {'name': 'Datopian', 'id': 'datopian'}],
            data=get_table_rows_by_office('pages'),
            sort_action='native',
            style_cell={'textAlign': 'left'},
        )],
        style={'width': '39%', 'display': 'inline-block', 'vertical-align': 'middle'}
    ),

    html.Hr(),

])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = generate_split_layout

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_hot_reload=True, host='0.0.0.0')
