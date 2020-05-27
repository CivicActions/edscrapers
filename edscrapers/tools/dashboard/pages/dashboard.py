import dash
import dash_table
import pandas as pd
import dash_daq as daq
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from edscrapers.tools.dashboard.ckan_api import CkanApi
from edscrapers.tools.dashboard.utils import buttonsToRemove
from edscrapers.tools.dashboard.pages.components import header, led_display

def datasets_in_portal_pie(ckan_api):
    """" function is used to created a pie chart showing
    the number of datasets in the Portal """

    labels=["Scraped Datasets", "Datasets Amended", "Datasets Manually Added"]
    values=[ckan_api.total_scraped_datasets(),
            ckan_api.total_amended_datasets(),
            ckan_api.total_manual_datasets()]

    pie_figure = go.Figure(data=[go.Pie(labels=labels,
                                        values=values,
                                        title={
                                            'font': {'size': 16}, 
                                            'position': 'top right'}
                                        )])
    pie_figure.update_traces(textposition='inside', textinfo='value+label')

    # return the pie chart
    return dcc.Graph(id='resources_by_domain_pie',
                    figure=pie_figure,
                    config={ 
                        'modeBarButtonsToRemove': buttonsToRemove 
                    }
    )

def generate_layout():

    ckan_api = CkanApi()
    
    return html.Div(children=[
    
    # Datasets By Domain
    header('Portal Totals', 
            'portal-totals',html.Div(id='portal-totals-tooltip-div', children=[
    html.Span("Datasets In Portal", style={'font-weight':'bold'}),
    html.Span(" - Total number of datasets in portal."),
    html.Br(),
    html.Br(), 
    html.Span("Scraped Datasets", style={'font-weight':'bold'}),
    html.Span(" - Total number of scraped datasets."),
    html.Br(),
    html.Br(),
    html.Span("Datasets Amended", style={'font-weight':'bold'}), 
    html.Span(" - Total number of scraped datasets which have been amended by a user."),
    html.Br(),
    html.Br(),
    html.Span("Datasets Manually Added", style={'font-weight':'bold'}), 
    html.Span(" - Total number of datasets manually added by a user.")
    ])),   
    html.Hr(),

    # LED displays
    led_display(ckan_api.total_datasets(), 
        "Datasets In Portal"),
    led_display(ckan_api.total_scraped_datasets(), 
        "Scraped Datasets"),
    led_display(ckan_api.total_amended_datasets(),
        "Datasets Amended By User"),
    led_display(ckan_api.total_manual_datasets(), 
        "Datasets Manually Added"),


    # Total dataset in the portal pie chart
    html.Div([
            datasets_in_portal_pie(ckan_api=ckan_api),
        ], style={'vertical-align': 'middle'}
    ),
    
    ])
    


external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = generate_layout

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_hot_reload=True, host='0.0.0.0')