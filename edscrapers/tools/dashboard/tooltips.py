# -*- coding: utf-8 -*-
import dash_html_components as html

INSIGHTS_TOTALS_TOOLTIP = html.Div([
    html.Span("Datasets", style={'font-weight':'bold'}),
    html.Span(" - Amount of scraped Datasets."),
    html.Br(),
    html.Br(), 
    html.Span("Resources", style={'font-weight':'bold'}),
    html.Span(" - Amount of scraped Resources."),
    html.Br(),
    html.Br(),
    html.Span("Pages", style={'font-weight':'bold'}), 
    html.Span(" - Amount of scraped Pages."),
    html.Br(),
    html.Br(),
    html.Span("Domains", style={'font-weight':'bold'}), 
    html.Span(" - Amount of scraped Domains.")
])

INSIGHTS_DATASETS_BY_DOMAIN_TOOOLTIP = html.Div([
    html.Span("Datasets by Domain", style={'font-weight':'bold'}),
    html.Span(" - Amount of Datasets ingested into the Portal by Domain."
        "We count the total number of Datasets inserted in the Portal by each scraped Domain."),
])

INSIGHTS_DATASETS_BY_OFFICE_TOOOLTIP = html.Div([
    html.Span("Datasets by Office", style={'font-weight':'bold'}),
    html.Span(" - Amount of Datasets ingested into the Portal by Office."
        "We count the total number of Datasets inserted in the Portal by each scraped Office."),
])

INSIGHTS_RESOURCES_BY_DOMAIN_TOOOLTIP = html.Div([
    html.Span("Resources by Domain", style={'font-weight':'bold'}),
    html.Span(" - Amount of Resources ingested into the Portal by Domain." 
        "We count the total number of Resources inserted in the Portal by scraped Domain.")  
])

TRENDS_OVERALL_DATA_QUALITY_TOOLTIP = html.Div([
    html.Span("Overall Data Quality Trends", style={'font-weight':'bold'}),
    html.Span(" - Shows the Score of Data Quality based on each Office per day when the scrapers were run.")
])
