# -*- coding: utf-8 -*-
import os
import pandas as pd

import dash
import dash_daq as daq
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output

import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format, Scheme, Sign, Symbol

from edscrapers.tools.dashboard.json_parser import get_datasets_bars_data

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
                {'name': 'Score', 'id': 'weighted score ratio', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
            ],
            data=self.df.groupby('domain', as_index=False).mean().round({'weighted score': 2}).to_dict('records'),
            sort_action='native',
            style_cell={'textAlign': 'left', 'whiteSpace': 'normal'},
            # virtualization=True,
            style_cell_conditional=[
                {'if': {'column_id': 'weighted score ratio'}, 'fontWeight': 'bold', 'textAlign': 'center'},
                #{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'},
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

    def publishers_table(self):
        return dash_table.DataTable(
            id='dataset_by_publisher_table',
            columns=[
                #{'name': '', 'id': 'index'},
                {'name': 'Publisher', 'id': 'publisher'},
                #{'name': 'Score', 'id': 'weighted score', 'format': Format(precision=2, scheme=Scheme.decimal)},
                {'name': 'Score', 'id': 'weighted score ratio', 'type': 'numeric', 'format': FormatTemplate.percentage(1)},
            ],
            data=self.df.groupby('publisher', as_index=False).mean().round({'weighted score': 2}).to_dict('records'),
            sort_action='native',
            style_cell={'textAlign': 'left', 'whiteSpace': 'normal'},
            # virtualization=True,
            style_cell_conditional=[
                {'if': {'column_id': 'weighted score ratio'}, 'fontWeight': 'bold', 'textAlign': 'center'},
                #{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(248, 248, 248)'},
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

    def header_notes(self):
        return html.Div(id="header_notes",children=[
            html.Span(
                "The data quality by ",
                className='text-muted',
            ),
            html.Span(
                "publisher",
                id="tooltip-publisher", className='text-muted',
                style={"textDecoration": "underline", "cursor": "pointer"},
            ),
            dbc.Tooltip(
                id="tooltip-1",
                children="Publishers are the Offices",
                target="tooltip-publisher",
            ),
            html.Span(
                " and ",
                className='text-muted',
            ),
            html.Span(
                "domain",
                id="tooltip-domain", className='text-muted',
                style={"textDecoration": "underline", "cursor": "pointer"},
            ),
            dbc.Tooltip(
                id="tooltip-2",
                children="A domain is the webpages that a Publisher has (can be 1 or more)",
                target="tooltip-domain",
            ),
            html.Span(
                " is shown below.",
                className='text-muted',
            ),
            html.Br(),
            html.Span(
                "An outline of how data quality is calculated provided at the ",
                className='text-muted',
            ),
            dcc.Link("bottom of this page.", href="#foot-table"),
        ], style={'margin-bottom':'30px'})

    def footer_notes(self):
        return html.Div(id="footer-notes", children=[
            html.Span("The Score reflect how complete the metadata " 
                "is in the form. 100% would mean that all the metadata fields " 
                "were present (this does not mean that the metadata is correct, " 
                "as the metadata has either been ingested by a scraper or input by a user. "
                "In other words, the metadata quality has not been assessed, the algorithm "
                "only checks how many metadata fields have been entered).",
                className='text-muted'),
            html.Br(),
            html.Br(),
            html.Span("The score is shown by two dimensions: by Publisher and by Domain.",
                className='text-muted'),
            html.Br(),
            html.Br(),
            html.Span("Data quality is calculated in the following way. "
                    "For each metadata filed that is present in a dataset," 
                    "points are assigned as per the table below",
                className='text-muted'),
            html.Br(),
            html.Br(),
            html.Div([
                html.Table(children=[
                    html.Tr([html.Th('Field'), html.Th('Weight')], style={'border': '1px solid'}),
                    html.Tr([html.Td('Title'), html.Td('10')]),
                    html.Tr([html.Td('Date period - Start'), html.Td('10')]),
                    html.Tr([html.Td('Date period - End'), html.Td('10')]),
                    html.Tr([html.Td('Categories'), html.Td('9.5')]),
                    html.Tr([html.Td('Tags'), html.Td('9.5')]),
                    html.Tr([html.Td('Description'), html.Td('9')]),
                    html.Tr([html.Td('Organization'), html.Td('8.5')]),
                    html.Tr([html.Td('Publisher'), html.Td('8.5')]),
                    html.Tr([html.Td('Data level'), html.Td('7')]),
                    html.Tr([html.Td('Spatial'), html.Td('6')]),
                    html.Tr([html.Td('Created Date'), html.Td('5')]),
                    html.Tr([html.Td('Frequency'), html.Td('5')]),
                    html.Tr([html.Td('Data Steward Name'), html.Td('4')]),
                    html.Tr([html.Td('Data Steward Email'), html.Td('4')]),
                    html.Tr([html.Td('Helpdesk Phone'), html.Td('4')]),
                    html.Tr([html.Td('Helpdesk Email'), html.Td('4')]),
                    html.Tr([html.Td('License'), html.Td('4')]),
                    html.Tr([html.Td('Bureau code'), html.Td('1')]),
                    html.Tr([html.Td('Program code'), html.Td('1')]),
                    html.Tr([html.Td('Access level'), html.Td('1')]),
                    ],style={'border': '1px solid'}, id="foot-table", className='text-muted')
            ],style={'width': '30%', 'margin': 'auto'})
        ])

def generate_layout():
    rag = RAGSummary()
    return html.Div(children=[

        # header notes
        rag.header_notes(),

        # tabs
        dcc.Tabs(id="rag-tabs", value='tab-publishers-table', children=[
            dcc.Tab(label='Publishers', value='tab-publishers-table',
                    children=[rag.publishers_table()]
            ),
            dcc.Tab(label='Domains', value='tab-domains-table',
                    children=[rag.domains_table()]
            ),
        ]),
        html.Div(id='tabs-content',style={"margin-bottom":"30px"}),

        # footer notes
        rag.footer_notes(),
        
    ],
    style={'display': 'inline-block',
            'width': '100%'}
    )


app.layout = generate_layout


