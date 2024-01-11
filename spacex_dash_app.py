# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Dropdown list for Launch Site selection
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True),
    html.Br(),

    # TASK 2: Pie chart for launch success counts
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    html.P("Payload range (Kg):"),

    # TASK 3: Slider for payload range
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 10000: '10000'},
                    value=[min_payload, max_payload]),
    
    html.Br(),

    # TASK 4: Scatter chart for payload vs. launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback function for updating the pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value')]
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', names='Launch Site', title='Total Success Launches by Site')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, values='class', names='Outcome', title=f'Successful and Failed Launches for {entered_site}')
    return fig

# TASK 4: Callback for the scatter chart


# TASK 4: Callback for updating the scatter chart based on selected site and payload range
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(entered_site, payload_range):
    # Filtering data based on payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]

    if entered_site == 'ALL':
        # If ALL sites are selected, use the filtered dataset without further filtering
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category', 
                         title='Correlation between Payload and Success for all Launch Sites')
    else:
        # If specific site is selected, filter data based on the site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                         color='Booster Version Category', 
                         title=f'Correlation between Payload and Success for {entered_site} Site')

    return fig








# Run the app
if __name__ == '__main__':
    app.run_server()
