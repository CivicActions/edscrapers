# -*- coding: utf-8 -*-
import dash_html_components as html

INSIGHTS_TOTALS_SCRAPED_TOOLTIP = html.Div([
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

INSIGHTS_TOTALS_INGESTED_TOOLTIP = html.Div([
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
    html.Span(" - Total Datasets ingested into the data portal by Domain (webpages)."
        "A Publisher will have 1 or more domains."),
])

INSIGHTS_DATASETS_BY_OFFICE_TOOOLTIP = html.Div([
    html.Span("Datasets by Publisher", style={'font-weight':'bold'}),
    html.Span(" - Total Datasets ingested into the data portal by Publisher (aka Office)"),
])

INSIGHTS_RESOURCES_BY_DOMAIN_TOOOLTIP = html.Div([
    html.Span("Resources by Domain", style={'font-weight':'bold'}),
    html.Span(" - Total Resources (ie datafiles / data assets) ingested into the Portal by Domain")  
])

INSIGHTS_RESOURCES_BY_OFFICE_TOOOLTIP = html.Div([
    html.Span("Resources by Publisher ", style={'font-weight':'bold'}),
    html.Span(" - Total Resources ingested into the data portal by Publisher (aka Office)"),
])

TRENDS_OVERALL_DATA_QUALITY_TOOLTIP = html.Div([
    html.Span("Data Quality Trend", style={'font-weight':'bold'}),
    html.Span(" - This shows the progression of metadata quality across all offices over time.")
])
