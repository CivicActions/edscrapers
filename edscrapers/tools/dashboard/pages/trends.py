# -*- coding: utf-8 -*-
import os
import pandas as pd
from glob import glob

import dash
import dash_daq as daq
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px


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

    dfs = []
    for df_csv in dfs_list:

        df = pd.read_csv(df_csv)
        df = df.groupby('publisher', as_index=False)['weighted score ratio'].mean()
        df = df.round({'weighted score ratio': 2})
        df['weighted score ratio'] = df['weighted score ratio'].apply(lambda x: x*100)

        df_date = df_csv.split('/')[-2]  
        df['date'] = df_date

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

    dfs_edgov = get_series('edgov')
    dfs_edgov = pd.concat(dfs_edgov, ignore_index=True)

    dfs_ocr = get_series('ocr')
    dfs_ocr = pd.concat(dfs_ocr, ignore_index=True)

    dfs_octae = get_series('octae')
    dfs_octae = pd.concat(dfs_octae, ignore_index=True)

    #dfs_oela = get_series('oela')
    #dfs_oela = pd.concat(dfs_oela, ignore_index=True)

    df = pd.concat([dfs_edgov,
       dfs_ocr, dfs_octae], ignore_index=True)

    df = df.sort_values(by='date')

    figure = px.line(df,
                     x="date",
                     y="weighted score ratio",
                     color='publisher',
                     # line_group='domain',
                     title=f'{"Overall"} Data Quality Trend')

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
        all_domain_quality_series()
    ])


app.layout = generate_layout

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_hot_reload=True, host='0.0.0.0')
