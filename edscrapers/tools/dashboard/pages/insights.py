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

from edscrapers.tools.dashboard.utils import buttonsToRemove


LED_DISPLAY_STYLE = {
    'width': '24%', 
    'display': 'inline-block', 
    'vertical-align': 'middle'
}

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

        # add a total of page count at the end of the df
        total_page_count = df['page count'].sum()   

        df_total = pd.DataFrame([['Total', total_page_count]], 
                            columns=['domain','page count'])
        df = df.append(df_total, ignore_index=True)

        # create the DataTable
        return dash_table.DataTable(
                id='dataset_by_domain_table',
                #columns=[{"name": i, "id": i} \
                #    if i != "page count" else \
                #        {"name": "Dataset Count", "id": i} \
                #            for i in df.columns],
                columns=[{"id": "domain", "name": "Domain"}, 
                        {"id": "page count", "name": "Dataset Count"}],
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
                            'width': '30%'},
                            {'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'}],
                style_table={
                            'maxHeight': '300px',
                            'maxWidth': '100%',
                            'overflowY': 'auto',
                            'overflowX': 'hidden',
                            'margin': 0,
                            'padding': 0,
                            },
                style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold',
                            'textAlign': 'center',
                            }
        )


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
                    #'title': 'Datasets by Domain'
                }
            },
            config={ 
                'modeBarButtonsToRemove': buttonsToRemove 
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
        
        # sort values
        working_df1.sort_values(by='resource count', axis='index',
                                    ascending=False, inplace=True,
                                    ignore_index=True)

        # add a total of resource count at the end of the df
        total_resource_count = working_df1['resource count'].sum()   

        df_total = pd.DataFrame([['Total', total_resource_count]], 
                            columns=['domain','resource count'])
        working_df1 = working_df1.append(df_total, ignore_index=True)
        
        # return the created DataTable
        return dash_table.DataTable(
                    id='resource_by_domain_table',
                    #columns=[{"name": i, "id": i} for i in working_df1.columns],
                    columns=[{"id": "domain", "name": "Domain"},
                            {"id": "resource count", "name": "Resource Count"}],
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
                        'width': '30%'},
                        {'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'}],
                    style_table={
                        'maxHeight': '300px',
                        'maxWidth': '100%',
                        'overflowY': 'scroll',
                        'overflowX': 'hidden',
                        'margin': 0,
                        'padding': 0
                    },
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold',
                        'textAlign': 'center',
                    }
        )


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
                                            title={
                                                #'text': 'Resources By Domain', 
                                                'font': {'size': 16}, 
                                                'position': 'bottom right'})])
        pie_figure.update_traces(textposition='inside', textinfo='value+label')

        # return the pie chart
        return dcc.Graph(id='resources_by_domain_pie',
                         figure=pie_figure,
                         config={ 
                            'modeBarButtonsToRemove': buttonsToRemove 
                         }
                        )



def generate_split_layout():
    """" function generates the latyout for this page """

    p = InsightsPage()

    return html.Div(children=[
   
    # Totals
    html.Div([
        daq.LEDDisplay(
            value=p.get_compare_dict()['total']['datopian']['datasets'], 
            color="#1F77B4", label="DATASETS",
            backgroundColor="#F8F9FA"
        ),
    ], 
    style=LED_DISPLAY_STYLE),

    html.Div([
        daq.LEDDisplay(
            value=p.get_compare_dict()['total']['datopian']['resources'], 
            color="#1F77B4", label="RESOURCES",
            backgroundColor="#F8F9FA"
        ),
    ], 
    style=LED_DISPLAY_STYLE),

    html.Div([
        daq.LEDDisplay(
            value=sum(s for s in p.get_compare_dict()['total']['datopian']['pages'].values()),
            color="#1F77B4", label="PAGES",
            backgroundColor="#F8F9FA"
        ),
    ], 
    style=LED_DISPLAY_STYLE),

    html.Div([
        daq.LEDDisplay(
            value=p.resources_by_domain_df().count()['domain'], 
            color="#1F77B4", label="DOMAINS",
            backgroundColor="#F8F9FA"
        ),
    ], 
    style=LED_DISPLAY_STYLE),

    html.Hr(),

    # Datasets By Domain
    html.Div([
        html.H4('Datasets by Domain',
        style={'text-align': 'center'}),
        ], 
    style={
        'width': '100%', 
        'vertical-align': 'middle'}
    ),

    html.Hr(),

    html.Div([
        p.dataset_by_domain_table()
    ],
    style={
        'width': '50%', 
        'display': 'inline-block',
        'vertical-align': 'middle', 
        'overflow-x': 'auto'}
    ),

    html.Div([
        p.dataset_by_domain_bar()],
        style={
            'width': '50%', 
            'display': 'inline-block', 
            'vertical-align': 'middle'
        }
    ),

    html.Hr(),

    # Datasets By Office
    html.Div([
        html.H4('Datasets by Office',
        style={'text-align': 'center'}),
        ], 
    style={
        'width': '100%', 
        'vertical-align': 'middle'}
    ),

    html.Hr(),
    
    html.Div([
        dash_table.DataTable(
            columns=[{'name': 'Office', 'id': 's'}, 
                    {'name': 'Count', 'id': 'datopian'}],
            data=get_table_rows_by_office('datasets_by_office'),
            sort_action='native',
            style_cell={'textAlign': 'left'},
            style_cell_conditional=[
                    {'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'}],
            style_table={
                'maxHeight': '300px',
            },
            style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                    }

        ),
    ], style={
            'width': '50%', 
            'display': 'inline-block', 
            'vertical-align': 'middle'}
    ),

    html.Div([
        dcc.Graph(
            figure={
                'data': get_datasets_bars_data(),
                'layout': {
                    #'title': 'Datasets by Office'
                }
            },
            config={ 
                'modeBarButtonsToRemove': buttonsToRemove 
            }
            ),
        ], 
        style={
            'width': '50%', 
            'display': 'inline-block', 
            'vertical-align': 'middle'
            }
    ),

    html.Hr(),

    # Resources by Domain
    html.Div([
        html.H4('Resources by Domain',
        style={'text-align': 'center'}),
        ], 
    style={
        'width': '100%', 
        'vertical-align': 'middle'}
    ),

    html.Hr(),

    html.Div([
        p.resources_by_domain_table()
    ], style={
        'width': '50%', 
        'display': 'inline-block', 
        'vertical-align': 'middle'}
    ),

    html.Div([
        p.resources_by_domain_pie(),
    ], style={
        'width': '50%', 
        'display': 'inline-block', 
        'vertical-align': 'middle'}
    ),

    html.Hr(),

])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = generate_split_layout

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_hot_reload=True, host='0.0.0.0')
