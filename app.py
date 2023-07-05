import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import time
import datetime
import data
import hermes
import threading
import plotly.io as pio  

pio.templates.default = "plotly_dark"

data.set_interval(data.update_df, 10)

# Create a Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Graph(id='scatter-plot'),
    html.Div([
        dcc.Link('total index', href='/total', style={'marginRight': '10px'}),
        dcc.Link('funds index', href='/funds')
    ],
        style={'textAlign': 'center', 'marginTop': '20px'}
    ),

    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  # Update every 10 seconds (in milliseconds)
        n_intervals=0
    )
], style={    'backgroundColor': '#111111'})

figure_style ={
    'backgroundColor': '#111111',
    'color': '#ffffff',
    'fontFamily': 'Arial, sans-serif',
    'padding': '20px',
    'margin': '0 auto',
    'maxWidth': '800px'
}
# Page 1 layout
page1_layout = html.Div([
    html.H1("Total Index", style={'color': '#ffffff'}),
],
    style=figure_style
)


# Page 2 layout
page2_layout = html.Div([
    html.H1("funds Index", style={'color': '#ffffff'}),
],
    style=figure_style
)



@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def render_page_content(pathname):
    if pathname == '/total':
        return page1_layout
    elif pathname == '/funds':
        return page2_layout
    else:
        return page1_layout  # Default to page 1 layout if the URL is invalid



# Update the scatter plot every 5 seconds
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('interval-component', 'n_intervals'),
    Input('url', 'pathname')]
)
def update_scatter_plot(n, pathname):
    if pathname == '/funds':
        fig = go.Figure(data=go.Scatter(
            x=data.dft['time'],
            y=data.dft['index'],
        ))
    else:
        fig = go.Figure(data=go.Scatter(
            x=data.dff['time'],
            y=data.dff['index'],
        ))
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Index",
        xaxis_dtick=10
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
