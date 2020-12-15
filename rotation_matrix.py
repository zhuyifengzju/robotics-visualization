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
app.title = 'rotation matrix'

input_2d_section = html.Div(
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

input_3d_section = html.Div(
    [
        dcc.Input(
            id="omega_1",
            type="number",
            placeholder="omega_1",
        ),
        dcc.Input(
            id="omega_2",
            type="number",
            placeholder="omega_2",            
        ),
        dcc.Input(
            id="omega_3",
            type="number",
            placeholder="omega_3",            
        )
        
    ], style={'display': 'inline-block',
              'height': UI_GRAPH_HEIGHT,              
              'width': UI_SIDEBAR_WIDTH}
)

app.layout = html.Div([
    input_2d_section,    
    html.Div([
        dcc.Graph(id='quiver-2d-plot'),
    ], style={'display': 'inline-block',
              'height': UI_GRAPH_HEIGHT,
              'width': UI_GRAPH_WIDTH}),
    input_3d_section,    
    html.Div([
        dcc.Graph(id='quiver-3d-plot'),
    ], style={'display': 'inline-block',
              'height': UI_GRAPH_HEIGHT,
              'width': UI_GRAPH_WIDTH}),    
    # html.Div([
    #     dcc.Graph(id='base-figure', figure=deepcopy(BASE_FIGURE)),
    # ], style={
    #           'height': UI_GRAPH_HEIGHT,
    #           'width': UI_GRAPH_WIDTH}),
    
],  style=GLOBAL_PAGE_STYLE)

def plot_2d_quiver(omega, theta):

    # skew_matrix = skew2d(omega)
    skew_matrix = np.array([[0, -omega], [omega, 0]])
    
    x,y = np.meshgrid(np.arange(-2, 2, .5),
                      np.arange(-2, 2, .5))

    u = skew_matrix[0][0] * x + skew_matrix[0][1] * y
    v = skew_matrix[1][0] * x + skew_matrix[1][1] * y
    
    # Create quiver figure
    fig = ff.create_quiver(x, y, u, v,
                           scale=.25,
                           arrow_scale=.4,
                           name='quiver',
                           line_width=1)

    # Add points to figure
    fig.add_trace(go.Scatter(x=[0.], y=[0.],
                        mode='markers',
                        marker_size=12,
                        name='points'))

    x0 = 1.0
    y0 = 0.6

    x_traj = [x0]
    y_traj = [y0]
    dt = 0.05
    t = 0
    while t < theta:
        t += dt
        dx = skew_matrix[0][0] * x_traj[-1] + skew_matrix[0][1] * y_traj[-1]
        dy = skew_matrix[1][0] * x_traj[-1] + skew_matrix[1][1] * y_traj[-1]
        x_traj.append(x_traj[-1] + dx * dt)
        y_traj.append(y_traj[-1] + dy * dt)

    if theta > 0:
        fig.add_trace(go.Scatter(x=x_traj, y=y_traj,
                                 mode="lines",
                                 line=dict(color='firebrick', width=4)))

    # Add calculation

    
    return fig

@app.callback(
    dash.dependencies.Output('quiver-2d-plot', 'figure'),
    [dash.dependencies.Input('omega', 'value'),
     dash.dependencies.Input('theta', 'value')]
)
def update_2d_quiver_plot(omega, theta):
    return plot_2d_quiver(omega or 0, theta or 1)

def plot_3d_quiver(omega1,
                   omega2,
                   omega3):

    # skew_matrix = skew3d(omega1, omega2, omega3)
    
    skew_matrix = np.array([[0, -omega3, omega2],
                            [omega3, 0, -omega1],
                            [-omega2, omega1, 0]])
    
    x,y,z = np.meshgrid(np.arange(-2, 2, 1),
             np.arange(-2, 2, 1),
             np.arange(-2, 2, 1))
    # z = x + y + z
    # u, v, w = np.gradient(z, .2, .2, .2)
    
    u = skew_matrix[0][0] * x + skew_matrix[0][1] * y + skew_matrix[0][2] * z
    v = skew_matrix[1][0] * x + skew_matrix[1][1] * y + skew_matrix[1][2] * z
    w = skew_matrix[2][0] * x + skew_matrix[2][1] * y + skew_matrix[2][2] * z

    x = x.reshape(-1)
    y = y.reshape(-1)
    z = z.reshape(-1)
    u = u.reshape(-1)
    v = v.reshape(-1)
    w = w.reshape(-1)

    
    # Create quiver figure

    fig = go.Figure(data = go.Cone(
        x=x,
        y=y,
        z=z,
        u=u,
        v=v,
        w=w,
        colorscale='Blues',
        sizemode="absolute",
        sizeref=5))
    return fig

@app.callback(
    dash.dependencies.Output('quiver-3d-plot', 'figure'),
    [
        dash.dependencies.Input('omega_1', 'value'),
        dash.dependencies.Input('omega_2', 'value'),
        dash.dependencies.Input('omega_3', 'value')        
    ]
)
def update_3d_quiver_plot(omega_1, omega_2, omega_3):
    omega1 = omega_1 or 0
    omega2 = omega_2 or 0
    omega3 = omega_3 or 0
    
    return plot_3d_quiver(omega1,
                          omega2,
                          omega3)

# def plot_homogeneous_3d_quiver(omega1,
#                                omega2,
#                                omega3,
#                                vx,
#                                vy,
#                                vz):

#     # skew_matrix = skewhomogeneous_3d(omega1, omega2, omega3)
    
#     skew_matrix = np.array([[0, -omega3, omega2],
#                             [omega3, 0, -omega1],
#                             [-omega2, omega1, 0]])
    
#     x,y,z = np.meshgrid(np.arange(-2, 2, 1),
#              np.arange(-2, 2, 1),
#              np.arange(-2, 2, 1))
#     # z = x + y + z
#     # u, v, w = np.gradient(z, .2, .2, .2)
    
#     u = skew_matrix[0][0] * x + skew_matrix[0][1] * y + skew_matrix[0][2] * z
#     v = skew_matrix[1][0] * x + skew_matrix[1][1] * y + skew_matrix[1][2] * z
#     w = skew_matrix[2][0] * x + skew_matrix[2][1] * y + skew_matrix[2][2] * z

#     x = x.reshape(-1)
#     y = y.reshape(-1)
#     z = z.reshape(-1)
#     u = u.reshape(-1)
#     v = v.reshape(-1)
#     w = w.reshape(-1)

    
#     # Create quiver figure

#     fig = go.Figure(data = go.Cone(
#         x=x,
#         y=y,
#         z=z,
#         u=u,
#         v=v,
#         w=w,
#         colorscale='Blues',
#         sizemode="absolute",
#         sizeref=5))
#     return fig

# @app.callback(
#     dash.dependencies.Output('quiver-homogeneous-3d-plot', 'figure'),
#     [
#         dash.dependencies.Input('omega_1', 'value'),
#         dash.dependencies.Input('omega_2', 'value'),
#         dash.dependencies.Input('omega_3', 'value')        
#     ]
# )
# def update_homogeneous_3d_quiver_plot(omega_1, omega_2, omega_3):
#     omega1 = omega_1 or 0
#     omega2 = omega_2 or 0
#     omega3 = omega_3 or 0
    
#     return plot_homogeneous_3d_quiver(omega1,
#                           omega2,
#                           omega3)


if __name__ == "__main__":
    app.server.run(debug=DEBUG_MODE)
