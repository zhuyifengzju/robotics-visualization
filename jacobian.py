"""Visualize jacobian"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
from style_settings import GLOBAL_PAGE_STYLE, EXTERNAL_STYLESHEETS

from shared import BASE_FIGURE
from copy import deepcopy

DEBUG_MODE = True

UI_GRAPH_HEIGHT = "300px"
UI_GRAPH_WIDTH = "63%"
UI_SIDEBAR_WIDTH = "30%"

app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)

input_1_section = html.Div(
    [
        dcc.Input(
            id="omega",
            type="number",
            placeholder="omega",
        ),
        dcc.Input(
            id="theta",
            type="number",
            placeholder="theta"
        )
    ], style={'display': 'inline-block',
              'height': UI_GRAPH_HEIGHT,              
              'width': UI_SIDEBAR_WIDTH}
)

app.layout = html.Div([
    input_1_section,
    html.Div([
        dcc.Graph(id='pos-vel-jacobian'),            
    ], style={'display': 'inline-block',
              'height': UI_GRAPH_HEIGHT,
              'width': UI_GRAPH_WIDTH}),
    input_2_section,
    html.Div([
        dcc.Graph(id='torque-force-jacobian'),            
    ], style={'display': 'inline-block',
          'height': UI_GRAPH_HEIGHT,
          'width': UI_GRAPH_WIDTH})
    
])




if __name__ == "__main__":
    app.server.run(debug=DEBUG_MODE)
