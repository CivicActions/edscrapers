# -*- coding: utf-8 -*-
import os
import datetime
import pandas as pd
from glob import glob

import dash
import dash_daq as daq
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output

import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format, Scheme, Sign, Symbol
from edscrapers.transformers.base import helpers as h

from edscrapers.tools.dashboard.utils import buttonsToRemove

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

OUTPUT_PATH = os.getenv('ED_OUTPUT_PATH')

def get_df_series(name=None):
    out_dir = h.get_output_path('rag')
    dfs_list = glob(out_dir + f'/*/*_{name or "all"}.csv')

    dfs = []
    for df_csv in dfs_list:
        df = pd.read_csv(df_csv)
        df_date = df_csv.split('/')[-2]
        df['date'] = df_date
        df['office'] = name
        dfs.append(df)
    return dfs

def get_series(name=None):

    out_dir = h.get_output_path('rag')
    dfs_list = glob(out_dir + f'/*/*_{name or "all"}.csv')

    if len(dfs_list) == 0:
        return None

    dfs = []
    for df_csv in dfs_list:

        df = pd.read_csv(df_csv)
        df = df.groupby('publisher', as_index=False)['weighted score ratio'].mean()
        df = df.round({'weighted score ratio': 2})
        df['weighted score ratio'] = df['weighted score ratio'].apply(lambda x: x*100)

        df_date = df_csv.split('/')[-2]  
        df['date'] = datetime.datetime.strptime(df_date, '%Y-%m-%d')

        dfs.append(df)

    return dfs

def domain_quality_series(name=None):
    dfs = get_df_series(name)

    df = pd.concat(dfs)
    df = df.sort_values(by='date')

    figure = px.line(df,
                     x="date",
                     y="weighted score",
                     # line_group='domain',
                     title=f'{name or "Overall"} Data Quality Trend')

    return dcc.Graph(
        figure=figure
    )


def all_domain_quality_series():

    concat_lst = []

    dfs_edgov = get_series('edgov')
    if dfs_edgov:
        dfs_edgov = pd.concat(dfs_edgov, ignore_index=True)
        concat_lst.append(dfs_edgov)

    dfs_ocr = get_series('ocr')
    if dfs_ocr: 
        dfs_ocr = pd.concat(dfs_ocr, ignore_index=True)
        concat_lst.append(dfs_ocr)

    dfs_octae = get_series('octae')
    if dfs_octae:    
        dfs_octae = pd.concat(dfs_octae, ignore_index=True)
        concat_lst.append(dfs_octae)

    dfs_oela = get_series('oela')
    if dfs_oela:
        dfs_oela = pd.concat(dfs_oela, ignore_index=True)
        concat_lst.append(dfs_oela)

    df = pd.concat(concat_lst, ignore_index=True)
    df = df.sort_values(by='date')

    figure = px.line(df,
                     x="date",
                     y="weighted score ratio",
                     color='publisher',
                     # line_group='domain',
                     #title='Overall Data Quality Trend'
                     )

    # Edit the layout
    figure.update_layout(xaxis_title='Date',
                   yaxis_title='Weighted Score',
                   yaxis_range=['0','100'],
                   plot_bgcolor='#F8F9FA')

    figure.update_traces(mode='markers+lines')
    #figure.layout.paper_bgcolor = '#F8F9FA'

    return dcc.Graph(
        figure=figure,
        config={ 
                'modeBarButtonsToRemove': buttonsToRemove 
            }
    )

def generate_layout():
    return html.Div(children=[
        # domain_quality_series(),
        #domain_quality_series('ocr'),
        #domain_quality_series('edgov'),
        html.Hr(),
        html.Div([
            html.H4('Overall Data Quality Trend',
            style={'text-align': 'center'}),
        ]), 
        html.Hr(),
        all_domain_quality_series()
    ])


app.layout = generate_layout

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_hot_reload=True, host='0.0.0.0')
