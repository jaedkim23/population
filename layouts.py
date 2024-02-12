import pandas as pd
import numpy as np

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash import dash_table

import plotly.graph_objs as go
import plotly.express as px
import matplotlib.pyplot as plt

from datetime import timedelta, date
from datetime import datetime
from population import app
from components.contents import *
# from callbacks import *

# #####################################
# # Add your data
# #####################################

countries = pd.read_pickle("Data_app/countries.pkl")
DF1 = pd.read_pickle("Data_app/DF1.pkl")
DF1_plot = pd.merge(DF1, countries[['Code','Continent']], on="Code",how='inner')

DF1_1 = pd.read_pickle("Data_app/DF1_1.pkl")
DF1_1 = DF1_1[~DF1_1['Natural growth rate'].isna()]
DF1_1_plot = pd.merge(DF1_1, countries[['Code','Continent']], on="Code",how='inner')

DF2 = pd.read_pickle("Data_app/DF2.pkl")
DF2 = DF2[~DF2['Code'].isna()]

DF3 = pd.read_pickle("Data_app/DF3.pkl")
DF3 = DF3[~DF3['Code'].isna()]

DF4 = pd.read_pickle("Data_app/DF4.pkl")
DF4 = DF4[~DF4['Code'].isna()]

#####################################
# Styles & Colors
#####################################

NAVBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "12rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "top":0,
    "margin-top":'2rem',
    "margin-left": "14rem",
    "margin-right": "2rem",
}

#####################################
# Create Auxiliary Components Here
#####################################

def nav_bar():
    """
    Creates Navigation bar
    """
    navbar = html.Div(
    [
        html.H5("Brow by Topic", className="display-10",style={'textAlign':'center'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Median Age", href="/page1",active="exact", external_link=True),
                dbc.NavLink("Population by Group", href="/page2", active="exact", external_link=True),
                dbc.NavLink("Age Depenedency", href="/page3", active="exact", external_link=True),
                dbc.NavLink("Population Projections", href="/page4", active="exact", external_link=True),
                dbc.NavLink("About", href="/page5", active="exact", external_link=True),
            ],
            pills=True,
            vertical=True
        ),
    ],
    style=NAVBAR_STYLE,
    )  
    return navbar

#####################################
# Create Page Layouts Here
#####################################

### create year dictionar
# years = DF1['Year'].unique()
# # years = dict(zip(years, years.astype(str)))
# years_list = {}
# for year in years:
#     years_list[year] = {'value':str(year)}

### Layout 1
layout1 = html.Div([
    html.H1("World Population Trends"),
    html.Hr(),
    html.H4("Effects of Fertility Rate and Population Growth on Median Age"),
    html.H5("The median age varies across the globe. Western and advanced economies tend to be much older. Countries in Africa and the Middle East tend to be much younger."),
    html.H5("Two factors that are highly correlated with median are the fertility rate and population growth rate. As both factors fall, the median age increases."),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H6("Select a year:"),
                    # dcc.Slider(min=DF1_plot['Year'].unique().min(),max= DF1_plot['Year'].unique().max(),
                            #    step=4, value=DF1_plot['Year'].unique().max(), 
                            #    marks = years_list, 
                            #    included=False,id='tab1-year-select'),
                    dcc.Dropdown(DF1_plot['Year'].unique(),value=DF1_plot['Year'].unique().max(), id='tab1-year-select'),    
                ]),
                html.Div([
                    html.H6("Enter a continent(s)"),
                    dcc.Checklist(DF1_plot['Continent'].unique(), DF1_plot['Continent'].unique(),inline=True, id='tab1-continent-select'),
                ]),
            ],width=12),
            # dbc.Col([
            #     html.Div([
            #         html.H6("Enter a continent(s)"),
            #         dcc.Checklist(DF1_plot['Continent'].unique(), DF1_plot['Continent'].unique(),inline=True, id='tab1-continent-select'),
            #     ]),
            # ],width=8),
        ]),
    ]),
    html.Hr(),
    html.H4(html.Div(id='tab-chosen-year')),
    dbc.Container([
        dbc.Row(
            [
                html.Div(
                    [
                        html.Div([
                            dcc.Graph(id='fig1'),
                            html.Hr(),
                            dcc.Graph(id='fig2')
                        ])
                    ]
                )
            ]
        )
    ])
])

layout2 = html.Div([
    html.H1("Population by Age Groups"),
    html.Hr(),
    html.H4("The age groups within a given population reveals the underlying population dynamics."),
    html.H5("The proportion of various age groups within a population reveals why the population growth rate slows down. A large young population indicates a high growth potential but the rate slows as the 'graying' of the population quickly lowers the rate."),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H6("Enter a country/region:"),
                    dcc.Dropdown(DF2['Entity'].unique(),value="Japan", id='tab2-country-select'),    
                ]),
            ],width=4),
            # dbc.Col([
            #     html.Div([
            #         html.H6("Enter a continent(s)"),
            #         dcc.Checklist(DF1_plot['Continent'].unique(), DF1_plot['Continent'].unique(),inline=True, id='tab1-continent-select'),
            #     ]),
            # ],width=8),
        ]),
    ]),
    html.Hr(),
    dbc.Container([
        dbc.Row(
            [
                html.Div(
                    [
                        html.Div([
                            dcc.Graph(id='figtab2'),
                        ])
                    ]
                )
            ]
        )
    ])
])

layout3 = html.Div([
    html.H1("Dependency by Age Groups"),
    html.Hr(),
    html.H5("In a given population, the old and young are dependent on the working age group, therefore, often refered to as the dependent groups. A population's greater proportion in the dependent groups can cause great stress for policymakers for such issues as healthcare and education. "),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H6("Enter a country/region:"),
                    dcc.Dropdown(DF3['Entity'].unique(),value="Japan", id='tab3-country-select'),    
                ]),
            ],width=4),
            # dbc.Col([
            #     html.Div([
            #         html.H6("Enter a continent(s)"),
            #         dcc.Checklist(DF1_plot['Continent'].unique(), DF1_plot['Continent'].unique(),inline=True, id='tab1-continent-select'),
            #     ]),
            # ],width=8),
        ]),
    ]),
    html.Hr(),
    dbc.Container([
        dbc.Row(
            [
                html.Div(
                    [
                        html.Div([
                            dcc.Graph(id='figtab3'),
                        ])
                    ]
                )
            ]
        )
    ])
])

layout4 = html.Div([
    html.H1("Population Projections"),
    html.Hr(),
    html.H5("Expected population changes by age groups. "),
    html.H5("The following plot shows the age groups of a population and future projections. Most advanced economies have large older age groups while developing countries in regions such as Africa have large younger age groups."),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H6("Enter a country/region:"),
                    dcc.Dropdown(DF4['Entity'].unique(),value="Japan", id='tab4-country-select'),    
                ]),
            ],width=4),
            # dbc.Col([
            #     html.Div([
            #         html.H6("Enter a continent(s)"),
            #         dcc.Checklist(DF1_plot['Continent'].unique(), DF1_plot['Continent'].unique(),inline=True, id='tab1-continent-select'),
            #     ]),
            # ],width=8),
        ]),
    ]),
    html.Hr(),
    dbc.Container([
        dbc.Row(
            [
                html.Div(
                    [
                        html.Div([
                            dcc.Graph(id='figtab4'),
                        ])
                    ]
                )
            ]
        )
    ])
])

layout5 = html.Div(
    [
        html.H5("Last update: 2/1/2024"),
        html.H6("Created by Jae D. Kim, Ph.D."),
        html.H6("All visualizations are generated from publicly available data provided by Go Solar California & San Diego Gas & Electric unless specified otherwise."),
        html.H6("This tool is for informational purposes only."),
        html.H6("Send any questions/comments to: jaedkim at sandiego dot edu")
    ]
)

######################################################################
## Callbacks
######################################################################
@app.callback(
        Output('tab-chosen-year', 'children'), Input('tab1-year-select','value')
)
def update_tab1_year(value):
    # value = int(value)
    return 'Showing results for year {}'.format(value)

@app.callback(
        Output('fig1', 'figure'),
        [Input('tab1-year-select','value'),
         Input('tab1-continent-select','value')]
)
def fig1_update(value1, value2):
    # value1 = int(value1)
    return median_age_content_update(DF1_plot, value1, value2)

@app.callback(
        Output('fig2', 'figure'),
        [Input('tab1-year-select','value'),
         Input('tab1-continent-select','value')]
)
def fig2_update(value1, value2):
    # value1 = int(value1)
    return pop_growth_content_update(DF1_1_plot, value1, value2)

@app.callback(
        Output('figtab2', 'figure'),
        [Input('tab2-country-select','value')]
)
def figtab2_update(value1):
    return age_group_content_update(DF2, value1)

@app.callback(
        Output('figtab3', 'figure'),
        [Input('tab3-country-select','value')]
)
def figtab3_update(value1):
    return dependency_content_update(DF3, value1)

@app.callback(
        Output('figtab4', 'figure'),
        [Input('tab4-country-select','value')]
)
def figtab4_update(value1):
    return pop_proj_content_update(DF4, value1)

