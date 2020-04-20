""" module creates the dashboard '/insights' page """

# -*- coding: utf-8 -*-
import os

import dash
import dash_table
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go

from edscrapers.tools.dashboard.pages.air import get_datasets_bars_data, get_table_rows_by_office
from edscrapers.tools.stats.stats import Statistics


class InsightsPage():

    # path to Excel sheet used for creating stas dataframes
    PATH_TO_EXCEL_SHEET = os.path.join(os.getenv('ED_OUTPUT_PATH'), 'tools', 'stats', 'metrics.xlsx')

    def get_compare_dict(self):
        if not hasattr(self, 'stats'):
            self.stats = Statistics()
        return self.stats.get_compare_dict()


    def _get_df_from_excel_sheet(self, sheet_name):
        """ private helper function used to read excel sheets and 
            create dataframes from the specified sheet"""

        return pd.read_excel(self.PATH_TO_EXCEL_SHEET, sheet_name, engine='openpyxl')


    def dataset_by_domain_table(self):
        """ function used to create the Table component which displays 
        the number of pages/datasets obtained from each domain """

        # get the dataframe from the excel sheet
        df = self._get_df_from_excel_sheet('PAGE COUNT (DATOPIAN)')
        # create the DataTable
        return dash_table.DataTable(id='dataset_by_domain_table',
                                    columns=[{"name": i, "id": i} \
                                        if i != "page count" else \
                                            {"name": "dataset count", "id": i} \
                                                for i in df.columns],
                                    data=df.to_dict('records'),
                                    sort_action='native',
                                    style_cell={'textAlign': 'left', 
                                                'whiteSpace': 'normal'},
                                    #fixed_rows={ 'headers': True, 'data': 0 },
                                    #virtualization=True,
                                    style_cell_conditional=[
                                                            {'if': {'column_id': 'domain'},
                                                            'width': '70%',
                                                            'textAlign': 'right'},
                                                            {'if': {'column_id': 'page count'},
                                                            'width': '30%'}],
                                    style_table={
                                                    'maxHeight': '300px',
                                                    'maxWidth': '100%',
                                                    'overflowY': 'scroll',
                                                    'overflowX': 'hidden',
                                                    'margin': 0,
                                                    'padding': 0
                                                    })


    def dataset_by_domain_bar(self):
        """ function creates a bar chart which displays the 
        number of pages/datasets per domain """
        # the the dataframe from the Excel sheet
        df = self._get_df_from_excel_sheet('PAGE COUNT (DATOPIAN)')
        # create the bar chart using the created dataframe
        return dcc.Graph(
            id='dataset_by_domain_graph',
            figure={
                'data': [
                            {'x': df['domain'], 'y': df['page count'], 'type': 'bar'}
                        ],
                'layout': {
                    'title': 'Datasets By Domain'
                }
            }
        )


    def resources_by_domain_table(self):
        """ function is used to create DataTable containing
        the number of resources/domains """

        # to perform this tasks, we need to collect stas from 2 different sheets
        # and unifiy it into one dataframe

        # get the resources collected from the datopian end of the air-datopian intersect
        df = self._get_df_from_excel_sheet('RESOURCE COUNT PER DOMAIN (DATOPIAN-AIR INTERSECTION)')

        # create a dataframe to hold the necessary info we use for this task
        working_df1 = pd.DataFrame(columns=['domain'])
        working_df1['domain'] = df['domain']
        working_df1['resource count'] = df['resource count_datopian']

        # get the resources from the DAtopian only resource count
        df = self._get_df_from_excel_sheet('RESOURCE COUNT PER DOMAIN (DATOPIAN ONLY)')
        working_df2 = pd.DataFrame(columns=['domain'])
        working_df2['domain'] = df['domain']
        working_df2['resource count'] = df['resource count']

        # concatenate the 2 dataframes
        working_df1 = pd.concat([working_df1,
                                working_df2], axis='index', ignore_index=True)
        # return the created DataTable
        return dash_table.DataTable(id='resource_by_domain_table',
                                    columns=[{"name": i, "id": i} for i in working_df1.columns],
                                    data=working_df1.to_dict('records'),
                                    sort_action='native',
                                    style_cell={'textAlign': 'left', 
                                                'whiteSpace': 'normal'},
                                    #fixed_rows={ 'headers': True, 'data': 0 },
                                    #virtualization=True,
                                    style_cell_conditional=[
                                            {'if': {'column_id': 'domain'},
                                            'width': '70%', 'textAlign': 'right'},
                                            {'if': {'column_id': 'resource count'},
                                            'width': '30%'}],
                                    style_table={
                                                    'maxHeight': '300px',
                                                    'maxWidth': '100%',
                                                    'overflowY': 'scroll',
                                                    'overflowX': 'hidden',
                                                    'margin': 0,
                                                    'padding': 0
                                                    })


    def resources_by_domain_df(self):
        # this function uses a concatenation of 2 different excel sheets and dataframes
        df = self._get_df_from_excel_sheet('RESOURCE COUNT PER DOMAIN (DATOPIAN-AIR INTERSECTION)')
        working_df1 = pd.DataFrame(columns=['domain'])
        working_df1['domain'] = df['domain']
        working_df1['resource count'] = df['resource count_datopian']

        df = self._get_df_from_excel_sheet('RESOURCE COUNT PER DOMAIN (DATOPIAN ONLY)')
        working_df2 = pd.DataFrame(columns=['domain'])
        working_df2['domain'] = df['domain']
        working_df2['resource count'] = df['resource count']

        # concatenate the 2 dataframes
        return pd.concat([working_df1, working_df2], axis='index', ignore_index=True)

    def resources_by_domain_pie(self):
        """" function is used to created a pie chart showing
        the number of resources gotten per domain """

        df = self.resources_by_domain_df()

        pie_figure = go.Figure(data=[go.Pie(labels=df['domain'],
                                            values=df['resource count'],
                                            title={'text': 'Resources By Domain', 'font': {'size': 16}, 'position': 'bottom right'})])
        pie_figure.update_traces(textposition='inside', textinfo='value+label')

        # return the pie chart
        return dcc.Graph(id='resources_by_domain_pie',
                         figure=pie_figure)



def generate_split_layout():
    """" function generates the latyout for this page """

    p = InsightsPage()

    return html.Div(children=[

    html.Div([
        daq.LEDDisplay(value=p.get_compare_dict()['total']['datopian']['datasets'], color="#353", label="DATASETS"),
    ], style={'width': '24%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Div([
        daq.LEDDisplay(value=p.get_compare_dict()['total']['datopian']['resources'], color="#353", label="RESOURCES"),
    ], style={'width': '24%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Div([
        daq.LEDDisplay(value=sum(s for s in p.get_compare_dict()['total']['datopian']['pages'].values()),
                       color="#353", label="PAGES"),
    ], style={'width': '24%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Div([
        daq.LEDDisplay(value=p.resources_by_domain_df().count()['domain'], color="#353", label="DOMAINS"),
    ], style={'width': '24%', 'display': 'inline-block', 'vertical-align': 'middle'}),

    html.Hr(),

    html.Div([
        p.resources_by_domain_pie(),
    ], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}),

    html.Div([
        p.resources_by_domain_table()
    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'middle'}),

    html.Div([
        dcc.Graph(figure={'data': get_datasets_bars_data(),
                'layout': {'title': 'Datasets by scraper'}}),
    ], style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}),

    html.Div([
        dash_table.DataTable(
            columns=[{'name': 'Scraper', 'id': 's'}, {'name': 'Count', 'id': 'datopian'}],
            data=get_table_rows_by_office('resources_by_office'),
            sort_action='native',
            style_cell={'textAlign': 'left'},
        ),
    ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'middle'}),

    html.Hr(),

    html.Div([
        html.H1('Domain Dataset Stats',
        style={'text-align': 'center', 'font-weight': 'bold'}),
    ], style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'middle'}),

    html.Div([
        p.dataset_by_domain_table()
        ],
        style={'width': '45%', 'display': 'inline-block',
            'vertical-align': 'middle', 'overflow-x': 'visible'}),

    html.Div([],
        style={'width': '5%', 'display': 'inline-block', 'vertical-align': 'middle'}),

    html.Div([p.dataset_by_domain_bar()],
        style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'middle'}),

    html.Hr(),

])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = generate_split_layout

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_hot_reload=True, host='0.0.0.0')
