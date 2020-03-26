# -*- coding: utf-8 -*-
import os
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_daq as daq
import plotly.graph_objs as go
import plotly.express as px


from edscrapers.tools.dashboard.pages.air import get_datasets_bars_data, get_table_rows_by_office

from edscrapers.tools.stats.stats import Statistics

stats = Statistics()

compare_dict = stats.get_compare_dict()
domains_df = stats.list_domain()

resources_domain_fig = px.pie(domains_df, values='page count', names='domain',
                              title='Resources per domain',)
resources_domain_fig.update_traces(textposition='inside', textinfo='value+label')



def generate_split_layout():
    return html.Div(children=[
    html.Div([
        daq.LEDDisplay(value=compare_dict['total']['datopian']['datasets'], color="#353", label="DATASETS"),
    ], style={'width': '24%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Div([
        daq.LEDDisplay(value=compare_dict['total']['datopian']['resources'], color="#353", label="RESOURCES"),
    ], style={'width': '24%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Div([
        daq.LEDDisplay(value=sum(s for s in compare_dict['total']['datopian']['pages'].values()),
                       color="#353", label="PAGES"),
    ], style={'width': '24%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Div([
        daq.LEDDisplay(value=domains_df.count()['domain'], color="#353", label="DOMAINS"),
    ], style={'width': '24%', 'display': 'inline-block', 'vertical-align': 'middle'}),


    html.Hr(),

    html.Div([
        dcc.Graph(figure={'data': get_datasets_bars_data(),
                'layout': {'title': 'Datasets by scraper'}}),
    ], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}),

    html.Div([
        dcc.Graph(figure=resources_domain_fig),
    ], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}),

    html.Div([
        dash_table.DataTable(
            columns=[{'name': 'Scraper', 'id': 's'}, {'name': 'Count', 'id': 'datopian'}],
            data=get_table_rows_by_office('resources_by_office'),
            sort_action='native',
            style_cell={'textAlign': 'left'},
        ),
    ], style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'top'}),

    html.Div([
        html.H4(children='RAW DATA',
                style={'text-orientation': 'upright', 'writing-mode': 'vertical-lr',
                       'text-transform': 'uppercase', 'margin': '0 auto',
                       'color': '#AAA', 'text-align': 'center'}),
    ], style={'width': '5%', 'display': 'inline-block', 'vertical-align': 'top', 'text-align': 'center'}),

    html.Div([
        dash_table.DataTable(
                data=domains_df.to_dict('records'),
                columns=[
                    {'id': i, 'name': i} for i in domains_df.columns
                ],
                fixed_rows={ 'headers': True, 'data': 0 },
                sort_action='native',
                style_cell={'textAlign': 'left'},
                virtualization=True,
                page_action='none'
        ),
    ], style={'width': '55%', 'display': 'inline-block', 'vertical-align': 'top'}),
    html.Hr(),
    html.Hr(),

])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = generate_split_layout
