import dash
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from components.contents import *

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server