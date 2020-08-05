# -*- coding: utf-8 -*-
import os
import datetime
import textwrap
import pandas as pd
from glob import glob

import dash
import dash_daq as daq
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Input, Output

import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format, Scheme, Sign, Symbol
from edscrapers.transformers.base import helpers as h
from edscrapers.tools.dashboard.pages import helpers as dashboard_helpers
from edscrapers.tools.dashboard.pages.tooltips import TRENDS_OVERALL_DATA_QUALITY_TOOLTIP

from edscrapers.tools.dashboard.utils import buttonsToRemove

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

OUTPUT_PATH = os.getenv('ED_OUTPUT_PATH')

TOOLTIP_STYLE = {
    'font-size': '0.8em',
    'text-align': 'center',
    'cursor': 'pointer',
    'height': '20px',
    'width': '20px',
    'color': '#1F77B4',
    'background-color': '#E6E6E6',
    'border-radius': '50%',
    'display': 'inline-block',
}

def tooltip(children, alignment):
    return html.Div([
        html.Span(
            "?",
            id="tooltip-target",
            style=TOOLTIP_STYLE,
        ),

        dbc.Tooltip(
            children,
            target="tooltip-target",
            placement="center",
        )
    ], style={
        'display': 'inline-block',
        'vertical-align': alignment,
        }
    )

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
        df = dashboard_helpers.mapped_publisher_name(df)
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

    #dfs_all = get_series()
    #if dfs_all:
    #    dfs_all = pd.concat(dfs_all, ignore_index=True)
    #    concat_lst.append(dfs_all)

    for office in ['edgov', 'fsa', 'ies', 'nces', 'ocr', 'rems',
                    'octae', 'oela', 'oese', 'ope', 'opepd', 'osers']:
        dfs = get_series(office)
        if dfs:
            dfs = pd.concat(dfs, ignore_index=True)
            concat_lst.append(dfs)

    df = pd.concat(concat_lst, ignore_index=True)
    df = df.sort_values(by='date')

    df_labels = df
    rows = df_labels['publisher']
    updated_rows = []
    for row in rows:
        legend_str = '<br>'.join(textwrap.wrap(row, width=40))
        updated_rows.append(legend_str)
    df_labels['publisher'] = updated_rows

    figure = px.line(df,
                     x="date",
                     y="weighted score ratio",
                     color='publisher',
                     labels={'date' : 'Date',
                             'weighted score ratio': 'Weighted Score Ratio',
                             'publisher': 'Publisher'},
                     text=updated_rows,
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
        
        html.Div([
            html.H5('Data Quality Trend',
                style={
                    'display':'inline-block',
                    'margin-bottom': '0',
                    'margin-right': '10px',
                    'margin-top':'0px',
                    }), 
            tooltip(TRENDS_OVERALL_DATA_QUALITY_TOOLTIP, alignment='text-bottom'),
        ], style={
            'width': '100%', 
            'vertical-align': 'middle',
            'display':'inline-block', 
        }),
        html.Hr(),

        all_domain_quality_series()
    ])


app.layout = generate_layout

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_hot_reload=True, host='0.0.0.0')
