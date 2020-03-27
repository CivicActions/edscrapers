# -*- coding: utf-8 -*-
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_daq as daq

from edscrapers.tools.dashboard.pages.air import get_datasets_bars_data


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/Emissions%20Data.csv').reset_index()
df['Emission'] = df['Emission'].map(lambda x: '{0:.2f}'.format(x))


def generate_layout():
    return html.Div(children=[
    dcc.Tabs(id="rag-tabs", value='RAG Summary', children=[
        dcc.Tab(label='Domains', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [4, 1, 2],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
        dcc.Tab(label='Pages', children=[
            dcc.Graph(
                figure={
                    'data': [
                        {'x': [1, 2, 3], 'y': [1, 4, 1],
                            'type': 'bar', 'name': 'SF'},
                        {'x': [1, 2, 3], 'y': [1, 2, 3],
                         'type': 'bar', 'name': u'Montréal'},
                    ]
                }
            )
        ]),
    ]),
    html.Div(id='tabs-content-example')
    ])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = generate_layout
