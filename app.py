import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import data
import dash_bootstrap_components as dbc


data.set_interval(data.update_dfs, 10)

# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Define the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Total Index", href="/total")),
                dbc.NavItem(dbc.NavLink("Funds Index", href="/funds")),
            ],
            navbar=True,
        )
    ),
    html.Div(id='page-content'),
    dcc.Graph(id='scatter-plot'),

    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  # Update every 5 seconds (in milliseconds)
        n_intervals=0
    )
])

# Page 1 layout
page1_layout = html.Div([
    html.H1("Total Index"),
],
)

# Page 2 layout
page2_layout = html.Div([
    html.H1("Funds Index"),
],
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
        return page1_layout 


# Update the scatter plot every 5 seconds
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('interval-component', 'n_intervals'),
     Input('url', 'pathname')]
)
def update_scatter_plot(n, pathname):
    if pathname == '/funds':
        fig = go.Figure(data=go.Scatter(
            x=data.funds_index_df['datetime'],
            y=data.funds_index_df['value'],
        ))
    else:
        fig = go.Figure(data=go.Scatter(
            x=data.total_index_df['datetime'],
            y=data.total_index_df['value'],
        ))
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Index",
        autosize=True
    )
    fig['layout']['yaxis'].update(autorange=True)
    fig['layout']['xaxis'].update(autorange=True)

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
