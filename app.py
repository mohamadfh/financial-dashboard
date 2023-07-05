import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import random
import datetime

# Create a Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    "Total Index:"
])


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
