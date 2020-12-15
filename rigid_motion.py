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

UI_GRAPH_HEIGHT = "600px"
UI_GRAPH_WIDTH = "63%"
UI_SIDEBAR_WIDTH = "37%"

app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)
app.title = 'rigid-motion'

def plot_quiver():
    x,y = np.meshgrid(np.arange(-2, 2, .2),
                      np.arange(-2, 2, .25))
    z = x*np.exp(-x**2 - y**2)
    v, u = np.gradient(z, .2, .2)

    # Create quiver figure
    fig = ff.create_quiver(x, y, u, v,
                           scale=.25,
                           arrow_scale=.4,
                           name='quiver',
                           line_width=1)

    # Add points to figure
    fig.add_trace(go.Scatter(x=[-.7, .75], y=[0,0],
                        mode='markers',
                        marker_size=12,
                        name='points'))
    return fig

app.layout = html.Div([
    html.Div([
        dcc.Graph(id='quiver-plot', figure=plot_quiver()),
    ], style={'display': 'inline-block',
              'height': UI_GRAPH_HEIGHT,
              'width': UI_GRAPH_WIDTH}),
    html.Div([
        dcc.Graph(id='base-figure', figure=deepcopy(BASE_FIGURE)),
    ], style={
              'height': UI_GRAPH_HEIGHT,
              'width': UI_GRAPH_WIDTH}),
    
],  style=GLOBAL_PAGE_STYLE)


if __name__ == "__main__":
    app.server.run(debug=DEBUG_MODE)
