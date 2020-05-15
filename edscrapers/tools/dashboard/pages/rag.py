# -*- coding: utf-8 -*-
import os
import pandas as pd

import dash
import dash_daq as daq
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format, Scheme, Sign, Symbol


from edscrapers.tools.dashboard.pages.air import get_datasets_bars_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


class RAGSummary():

    def __init__(self):
        self.df = pd.read_csv(os.path.join(os.getenv('ED_OUTPUT_PATH'),
                                           'transformers',
                                           'rag',
                                           'datasets_weighted_scores_all.csv'))

    def domains_table(self):
        return dash_table.DataTable(
            id='dataset_by_domain_table',
            columns=[
                #{'name': '', 'id': 'index'},
                {'name': 'Domain', 'id': 'domain'},
                #{'name': 'Score', 'id': 'weighted score', 'format': Format(precision=2, scheme=Scheme.decimal)},
                {'name': 'Percent', 'id': 'weighted score ratio', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
            ],
            data=self.df.groupby('domain', as_index=False).mean().round({'weighted score': 2}).to_dict('records'),
            sort_action='native',
            style_cell={'textAlign': 'left', 'whiteSpace': 'normal'},
            # virtualization=True,
            style_cell_conditional=[
                {'if': {'column_id': 'weighted score ratio'}, 'fontWeight': 'bold', 'textAlign': 'center'},
                {'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'},
            ],
            style_data_conditional=[
                {'if': {'column_id': 'weighted score ratio', 'filter_query': '{weighted score ratio} > 0.5'},
                'backgroundColor': '#238823'},
                {'if': {'column_id': 'weighted score ratio', 'filter_query': '{weighted score ratio} > 0.2'},
                'backgroundColor': '#FFBF00'},
                {'if': {'column_id': 'weighted score ratio', 'filter_query': '{weighted score ratio} < 0.2'},
                'backgroundColor': '#D2222D', 'color': 'white'},
            ],
            style_as_list_view=True,
            style_table={
                # 'overflowY': 'scroll', 'overflowX': 'hidden',
                'margin': 0, 
                'padding': 0},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
            }
        )

    def pages_table(self):
        return dash_table.DataTable(
            id='dataset_by_page_table',
            columns=[
                #{'name': '', 'id': 'index'},
                # {'name': 'Publisher', 'id': 'publisher'},
                {'name': 'URL', 'id': 'source url'},
                #{'name': 'Score', 'id': 'weighted score', 'format': Format(precision=2, scheme=Scheme.decimal)},
                {'name': 'Percent', 'id': 'weighted score ratio', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
            ],
            data=self.df.to_dict('records'),
            sort_action='native',
            style_cell={'textAlign': 'left',
                        'whiteSpace': 'normal'},
            # virtualization=True,
            style_cell_conditional=[
               # {'if': {'column_id': 'index'}, 'width': '2%', 'textAlign': 'right'},
                {'if': {'column_id': 'source url'}, 'width': '30%'},
                {'if': {'column_id': 'weighted score'}, 'width': '5%'},
                {'if': {'column_id': 'weighted score ratio'}, 'width': '5%'},
                {'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'},
            ],
            style_data_conditional=[
                {'if': {'column_id': 'weighted score ratio', 'filter_query': '{weighted score ratio} > 0.5'},
                # 'backgroundColor': '#238823'},
                'backgroundColor': '#7cd992'},
                {'if': {'column_id': 'weighted score ratio', 'filter_query': '{weighted score ratio} > 0.2'},
                'backgroundColor': '#f7e463'},
                {'if': {'column_id': 'weighted score ratio', 'filter_query': '{weighted score ratio} < 0.2'},
                'backgroundColor': '#eb6060', 'color': 'white'},
            ],
            style_as_list_view=True,
            sort_by=[{'column_id': 'weighted score ratio', 'direction': 'desc'}],
            style_table={
                # 'maxHeight': '300px',
                # 'maxWidth': '100%',
                # 'overflowY': 'scroll',
                # 'overflowX': 'hidden',
                'margin': 0,
                'padding': 0},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
            }
        )

    def publishers_table(self):
        return dash_table.DataTable(
            id='dataset_by_publisher_table',
            columns=[
                #{'name': '', 'id': 'index'},
                {'name': 'Publisher', 'id': 'publisher'},
                #{'name': 'Score', 'id': 'weighted score', 'format': Format(precision=2, scheme=Scheme.decimal)},
                {'name': 'Percent', 'id': 'weighted score ratio', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
            ],
            data=self.df.groupby('publisher', as_index=False).mean().round({'weighted score': 2}).to_dict('records'),
            sort_action='native',
            style_cell={'textAlign': 'left', 'whiteSpace': 'normal'},
            # virtualization=True,
            style_cell_conditional=[
                {'if': {'column_id': 'weighted score ratio'}, 'fontWeight': 'bold', 'textAlign': 'center'},
                {'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'},
            ],
            style_data_conditional=[
                {'if': {'column_id': 'weighted score ratio', 'filter_query': '{weighted score ratio} > 0.5'},
                'backgroundColor': '#238823'},
                {'if': {'column_id': 'weighted score ratio', 'filter_query': '{weighted score ratio} > 0.2'},
                'backgroundColor': '#FFBF00'},
                {'if': {'column_id': 'weighted score ratio', 'filter_query': '{weighted score ratio} < 0.2'},
                'backgroundColor': '#D2222D', 'color': 'white'},
            ],
            style_as_list_view=True,
            style_table={
                'margin': 0, 'padding': 0,},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
            }
        )


def generate_layout():
    rag = RAGSummary()
    return html.Div(children=[
        dcc.Tabs(id="rag-tabs", value='tab-publishers-table', children=[
            dcc.Tab(label='Publishers', value='tab-publishers-table',
                    children=[rag.publishers_table()]
            ),
            dcc.Tab(label='Domains', value='tab-domains-table',
                    children=[rag.domains_table()]
            ),
            dcc.Tab(label='Pages', value='tab-pages-table',
                    children=[rag.pages_table()]
            ),
        ]),
        html.Div(id='tabs-content')
    ],
    style={'display': 'inline-block',
            'width': '100%'}
    )


app.layout = generate_layout


