"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location. There are two callbacks,
one uses the current location to render the appropriate page content, the other
uses the current location to toggle the "active" properties of the navigation
links.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from .pages import dashboard, rag, trends, insights

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,'https://codepen.io/tanvirchahal/pen/WNQWvjE.css'])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#007bff",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "min-height": "100vh",
}

FOOTER_STYLE = {
    "background-color": "#f8f9fa",
    #"position": "absolute",
    "bottom": 0,
    "width": "100%",
    "height": "40px",
}

IMAGE_FOOTER_STYLE1 = {
    "width": 80, 
    "margin-right": 10,
}

IMAGE_FOOTER_STYLE2 = {
    "width": 100, 
    "margin-right": 10,
}

sidebar = html.Div(
    [
        html.H4("Scraping Dashboard", 
            className="display-6 text-center",
        ),
        html.Span(
            "Statistics on data extracted from ED sites",
            className='text-muted text-center',
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Dashboard", href="/dashboard", id="page-1-link"),
                dbc.NavLink("Scraping Insights", href="/insights", id="page-2-link"),
                dbc.NavLink("Data Quality", href="/quality", id="page-3-link"),
                dbc.NavLink("Trends", href="/trends", id="page-4-link")
            ],
            vertical=True,
            pills=True,
            
        ),
    ],
    style=SIDEBAR_STYLE,
    id='sidebar',
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

footer = html.Footer(
    className='page-footer',
    style=FOOTER_STYLE,
    children=html.Div(
        id='footer',
        className='container-fluid text-center',
        children=[
            html.Span(
                className='text-muted align-middle',
                style={'float': 'right', 'margin-bottom': 10},
                children=[
                    html.Span(
                        'Made by',
                        className='text-muted',
                        style={
                            'margin-right': 10,
                            'font-size':'12px',
                        }
                    ),
                    html.Img(src='https://i.stack.imgur.com/wSpIb.png', style=IMAGE_FOOTER_STYLE1),
                    html.Img(src='https://www.datopian.com/img/datopian-logo.png', style=IMAGE_FOOTER_STYLE2),
                ],
            ),
            html.H5()
        ]
    )
)

def generate_layout():
    return html.Div(
            children=[
                dcc.Location(id="url"),
                sidebar, 
                content, 
                footer
            ]
    )

app.layout = generate_layout

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 5)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False, False
    return [pathname == f"/{i}" for i in ['dashboard','insights', 'quality', 'trends']]

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/dashboard"]:
        return dashboard.generate_layout()
    elif pathname == "/insights":
        return insights.generate_split_layout()
    elif pathname in ["/rag", "/quality"]:
        return rag.generate_layout()
    elif pathname == "/trends":
        return trends.generate_layout()
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_hot_reload=True, host='0.0.0.0')
