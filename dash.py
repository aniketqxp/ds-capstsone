# Imports
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read in Data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# App instance
app = dash.Dash(__name__)

# Styling
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1:
    # Dropdown Menu
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            ],
        value='ALL', # DEFAULT <-
        placeholder="Select a Launch Site here",
        searchable=True
        ),
    html.Br(),

    # TASK 2:
    # Pie Chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # TASK 3:
    # Range Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: f'{i}' for i in range(0, 10001, 1000)},
        value=[min_payload, max_payload]
        ),
    html.Br(),

    # TASK 4:
    # Scatter Plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ])

# Callback function for changing data
@app.callback(
        Output(component_id='success-pie-chart', component_property='figure'),
        Input(component_id='site-dropdown', component_property='value')
        )

# Chart functions
def update_pie_chart(launch_site):
    if launch_site == 'ALL':
        fig = px.pie(
                spacex_df,
                names='Launch Site',
                values='class',
                title='Total Launches by Site'
                )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == launch_site]
        filtered_df['class_label'] = filtered_df['class'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(
                filtered_df,
                names='class_label',
                title=f'Total Success vs Failure Launches for {launch_site}'
                )

    return fig

@app.callback(
        Output(component_id='success-payload-scatter-chart', component_property='figure'),
        [
            Input(component_id='site-dropdown', component_property='value'),
            Input(component_id='payload-slider', component_property='value')
            ]
        )
def update_scatter_chart(launch_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]

    if launch_site == 'ALL':
        fig = px.scatter(
                filtered_df,
                x='Payload Mass (kg)', 
                y='class',
                color='Booster Version Category',
                title='Correlation between Payload and Success for All Sites',
                hover_data=['Launch Site'],
                labels={'class': 'Success'}
                )
    else:
        site_filtered_df = filtered_df[filtered_df['Launch Site'] == launch_site]
        fig = px.scatter(
                site_filtered_df,
                x='Payload Mass (kg)', 
                y='class',
                color='Booster Version Category',
                title=f'Correlation between Payload and Success for {launch_site}',
                hover_data=['Launch Site'],
                labels={'class': 'Success'}
                )

    return fig

if __name__ == '__main__':
    app.run_server()
