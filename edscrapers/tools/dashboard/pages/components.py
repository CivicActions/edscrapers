import dash_daq as daq
import dash_html_components as html
import dash_bootstrap_components as dbc

LED_DISPLAY_STYLE = {
    'width': '25%', 
    'display': 'inline-block', 
    'vertical-align': 'middle',
    'margin-top':'20px',
}

TOOLTIP_STYLE = {
    'font-size': '0.7em',
    'text-align': 'center',
    'cursor': 'pointer',
    'height': '16px',
    'width': '16px',
    'font-weight':'bold',
    'color': '#1F77B4',
    'background-color': '#E6E6E6',
    'border-radius': '50%',
    'display': 'inline-block',
}

HEADER_STYLE = {
    'display':'inline-block',
    'margin-bottom': '12px',
    'margin-right': '10px',
    'margin-top':'0px',
}

def tooltip(id, children, alignment):
    # returns a html component for tooltip
    return html.Div([
        html.Span(
            "?",
            id="tooltip-target-" + id,
            style=TOOLTIP_STYLE,
        ),

        dbc.Tooltip(
            children,
            target="tooltip-target-" + id,
            placement="center",
        )
    ], style={
            'display': 'inline-block',
            'vertical-align': alignment,
            'margin-right': '20px',
            }
    )

def header(title, tooltip_id, tooltip_text):
    # returns a Header html component with a tooltip at the right side
    return html.Div([
        html.H5(title, style=HEADER_STYLE), 
        tooltip(tooltip_id, tooltip_text, alignment='text-bottom'),
    ], style={
        'width': '100%', 
        'vertical-align': 'middle',
        'display':'inline-block',
    })

def led_display(value, label):
    # returns a component with a Led Display
    return html.Div([
        daq.LEDDisplay(
            value=value, 
            color="#1F77B4", label=label,
            backgroundColor="#F8F9FA"
        ),
    ], style=LED_DISPLAY_STYLE)