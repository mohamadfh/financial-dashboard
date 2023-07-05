
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import random
import time
import datetime
import data 
import hermes
import threading


data.set_interval(data.update_df,10)

# # Create an empty DataFrame to store the scatter plot data
# df = pd.DataFrame(columns=['index', 'time'])

# Create a Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    dcc.Graph(id='scatter-plot'),
    
    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  # Update every 10 seconds (in milliseconds)
        n_intervals=0
    )
])

# Update the scatter plot every 10 seconds
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_scatter_plot(n):
    # time = datetime.datetime.now().strftime('%H:%M:%S')
    # stock_df = hermes.Market_with_askbid()
    # ti = data.calc_total_index(stock_df)
    # new_data = {'time': time, 'index': ti}
    # print(time)
    # print(ti)
    # df.loc[len(df)] = new_data

    # Create the scatter plot
    fig = go.Figure(data=go.Scatter(
        x=data.df['time'],
        y=data.df['index'],
    ))
    fig.update_xaxes(
    rangeslider_visible=True,
    tickformatstops = [
        dict(dtickrange=[None, 60000], value="%H:%M:%S s"),
        dict(dtickrange=[60000, 3600000], value="%H:%M m"),
        dict(dtickrange=[3600000, 86400000], value="%H:%M h")
    ])
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
