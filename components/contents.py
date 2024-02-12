import pandas as pd
import numpy as np

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash import dash_table

import plotly.graph_objs as go
import plotly.express as px

from datetime import timedelta, date
from datetime import datetime

def median_age_content_update(DF1_plot, yearX, continent_in):
    DF1_plot_x = DF1_plot[DF1_plot['Year']==yearX]
    DF1_plot_x = DF1_plot_x[DF1_plot_x['Population']>1000000]
    DF1_plot_x.loc[:,'Pop'] = round(np.sqrt(DF1_plot_x['Population']/1000))
    DF1_plot_x=DF1_plot_x[DF1_plot_x['Continent'].isin(continent_in)]

    fig1 = px.scatter(DF1_plot_x, x="Median age", y="Fertility rate", size=  "Population", color="Continent",
                    hover_name="Entity", size_max=60,
                    title="Fertility Rate (%) vs. Median Age") 
    fig1.add_hline(y=2.1, line_dash="dash",line_color="gray")
    # Add a label to the horizontal line
    fig1.add_annotation(
        xref="paper",  # Use 'paper' to position x based on the width of the plot
        x= 0.05,  # Position the label horizontally
        y=2.2,  # Position the label at the same y-coordinate as the line
        text="Replacement rate=2.1",  # The text of the label
        showarrow=False,  # Do not show an arrow pointing to the text
        font=dict(
            size=12,
            color="gray",
        ),
        align="center"  
    )
    fig1.update_layout(
        xaxis_title="Median Age",
        yaxis_title="Fertility Rate (%)"
    )
    fig1.update_layout(width=1280, height=720, title_x=0.5)
    return fig1

def pop_growth_content_update(DF1_1_plot, yearX, continent_in):
    DF1_1_plot_x = DF1_1_plot[DF1_1_plot['Year']==yearX]
    DF1_1_plot_x = DF1_1_plot_x[DF1_1_plot_x['Population']>1000000]
    DF1_1_plot_x = DF1_1_plot_x[DF1_1_plot_x['Continent'].isin(continent_in)]
    fig2 = px.scatter(DF1_1_plot_x, y="Median age", x="Natural growth rate", size=  "Population", color="Continent",
                     hover_name="Entity", size_max=60,
                     title="Median Age vs. Population Growth Rate") 
    fig2.update_layout(
        yaxis_title="Median Age",
        xaxis_title="Population Growth Rate (%)"
    )
    fig2.update_layout(width=1280, height=720, title_x=0.5)
    return fig2

def age_group_content_update(DF2, countryX):
    DF2_plot_x = DF2[DF2['Entity']==countryX]
    DF2_plot_x = DF2_plot_x.drop('Code', axis=1)
    DF2_plot_x.columns = ['Entity','Year', 'Ages 65+', 'Ages 25-64', 'Ages 15-24', 'Ages 5-14', 'Ages 0-4']
    DF2_plot_x = pd.melt(DF2_plot_x, id_vars=['Entity','Year'], value_vars=['Ages 65+', 'Ages 25-64', 'Ages 15-24', 'Ages 5-14', 'Ages 0-4'], value_name="Population")
    DF2_plot_x.columns = ['Entity','Year','Group','Population']
    country = DF2_plot_x['Entity'][0]

    fig = px.area(DF2_plot_x, x="Year", y="Population", color='Group',
                  category_orders={'Group':['Ages 0-4', 'Ages 5-14', 'Ages 15-24', 'Ages 25-64', 'Ages 65+']},
                  hover_name="Entity",
                  title="Population by Age Group, "+country
                )
    fig.update_layout(width=1280, height=720, title_x=0.5)
    return fig

def dependency_content_update(DF3, countryX):
    DF3_plot_x = DF3[DF3['Entity']==countryX]
    DF3_plot_x = DF3_plot_x.drop('Code', axis=1)
    DF3_plot_x.columns = ['Entity','Year', 'Elderly (Ages 65+)', 'Young (Ages 0-14)']
    DF3_plot_x = pd.melt(DF3_plot_x, id_vars=['Entity','Year'], value_vars=['Elderly (Ages 65+)', 'Young (Ages 0-14)'], value_name="Proportion")
    DF3_plot_x.columns = ['Entity','Year','Group','Percentage']
    country = DF3_plot_x['Entity'][0]

    fig = px.area(DF3_plot_x, x="Year", y="Percentage", color='Group',
                category_orders={'Group':['Young (Ages 0-14)',  'Elderly (Ages 65+)']},
                hover_name="Entity",
                title="Age Dependency Breakdown by Young and Old Dependents, "+country
                )
    fig.update_layout(
        yaxis_title="Percentage of Population (%)",
        xaxis_title="Year"
    )
    fig.update_layout(width=1280, height=720, title_x=0.5)
    return fig

def pop_proj_content_update(DF4, countryX):
    DF4_plot_x = DF4[DF4['Entity']==countryX]
    DF4_plot_x = DF4_plot_x.drop('Code', axis=1)
    DF4_plot_x.columns = ['Entity','Year', 'Elderly (Ages 65+)','Elderly (Ages 65+) Proj.', 
                          'Working (Ages 15-64)', 'Working (Ages 15-64) Proj.',
                          'Young (Ages 0-14)', 'Young (Ages 0-14) Proj.']
    DF4_plot_x = pd.melt(DF4_plot_x, id_vars=['Entity','Year'], value_vars=['Elderly (Ages 65+)','Elderly (Ages 65+) Proj.', 
                          'Working (Ages 15-64)', 'Working (Ages 15-64) Proj.',
                          'Young (Ages 0-14)', 'Young (Ages 0-14) Proj.'], 
                          value_name="Population")
    DF4_plot_x.columns = ['Entity','Year','Group','Population']
    country = DF4_plot_x['Entity'][0]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=DF4_plot_x.loc[DF4_plot_x['Group']=="Elderly (Ages 65+)","Year"], 
                             y=DF4_plot_x.loc[DF4_plot_x['Group']=="Elderly (Ages 65+)","Population"], 
                             name='Elderly (Ages 65+)',
                             line=dict(color='firebrick', width=4)))
    fig.add_trace(go.Scatter(x=DF4_plot_x.loc[DF4_plot_x['Group']=="Elderly (Ages 65+) Proj.","Year"], 
                             y=DF4_plot_x.loc[DF4_plot_x['Group']=="Elderly (Ages 65+) Proj.","Population"], 
                             name='Elderly (Ages 65+) Proj.',
                             line=dict(color='firebrick', dash='dash',width=4)))
    fig.add_trace(go.Scatter(x=DF4_plot_x.loc[DF4_plot_x['Group']=='Working (Ages 15-64)',"Year"], 
                             y=DF4_plot_x.loc[DF4_plot_x['Group']=='Working (Ages 15-64)',"Population"], 
                             name='Working (Ages 15-64)',
                             line=dict(color='royalblue', width=4)))
    fig.add_trace(go.Scatter(x=DF4_plot_x.loc[DF4_plot_x['Group']=="Working (Ages 15-64) Proj.","Year"], 
                             y=DF4_plot_x.loc[DF4_plot_x['Group']=="Working (Ages 15-64) Proj.","Population"], 
                             name='Working (Ages 15-64) Proj.',
                             line=dict(color='royalblue', dash='dash',width=4)))
    fig.add_trace(go.Scatter(x=DF4_plot_x.loc[DF4_plot_x['Group']=='Young (Ages 0-14)',"Year"], 
                             y=DF4_plot_x.loc[DF4_plot_x['Group']=='Young (Ages 0-14)',"Population"], 
                             name='Young (Ages 0-14)',
                             line=dict(color='orange', width=4)))
    fig.add_trace(go.Scatter(x=DF4_plot_x.loc[DF4_plot_x['Group']=="Young (Ages 0-14) Proj.","Year"], 
                             y=DF4_plot_x.loc[DF4_plot_x['Group']=="Young (Ages 0-14) Proj.","Population"], 
                             name='Young (Ages 0-14) Proj.',
                             line=dict(color='orange', dash='dash',width=4)))
    fig.update_layout(title="Population Projections by Age Group, "+country,
                       xaxis_title='Year',
                       yaxis_title='Population')

    fig.update_layout(width=1280, height=720, title_x=0.5)
    return fig
