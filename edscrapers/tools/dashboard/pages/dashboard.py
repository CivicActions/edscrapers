import dash
import dash_table
import pandas as pd
import dash_daq as daq
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from edscrapers.tools.dashboard.utils import buttonsToRemove
from edscrapers.tools.dashboard.pages.components import header, led_display

def datasets_in_portal_pie():
    """" function is used to created a pie chart showing
    the number of datasets in the Portal """

    labels=["Scraped Datasets", "Datasets Amended", "Datasets Manually Added"]
    values=[223,15,34]

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
    
    return html.Div(children=[
    
    # Datasets By Domain
    html.Hr(),
    header('Portal Totals', 
            'portal-totals','Some text'),   
    html.Hr(),

    # LED displays
    led_display(272, 
        "Datasets in Portal"),
    led_display(223, 
        "Scraped Datasets"),
    led_display(15,
        "Datasets Amended"),
    led_display(34, 
        "Datasets Manually Added"),

    html.Hr(),

    # Total dataset in the portal pie chart
    html.Div([
            datasets_in_portal_pie(),
        ], style={'vertical-align': 'middle'}
    ),
    
    ])
    


external_stylesheets = [dbc.themes.BOOTSTRAP, 'https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = generate_layout()

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_hot_reload=True, host='0.0.0.0')