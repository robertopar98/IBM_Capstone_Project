# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

options=[
        {'label': 'All Sites', 'value': 'ALL'},
        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ]

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div([
                                dcc.Dropdown(id='site-dropdown',
                                            options=options,
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True
                                            )
                                        ])
                                ,
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div([
                                    dcc.RangeSlider(id='payload-slider',
                                                    min=0, max=10000, step=1000,
                                                    marks={0: '0',
                                                    2500: '2500',
                                                    5000: '5000',
                                                    7500: '7500',
                                                    10000: '10000'},
                                                    value=[min_payload, max_payload])
                                ]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    
    if entered_site == 'ALL':
        data = spacex_df.groupby('Launch Site')['class'].sum()
        fig = px.pie(data, values='class', 
            names=data.index, 
            title='Total Success Launches By Site')
        return fig
    elif entered_site == 'CCAFS LC-40':
        data = spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40']
        data = data.groupby('class')['class'].count()
        fig = px.pie(data, values='class', 
            names=data.index, 
            title='Total Success Launches for site CCAFS LC-40')
        return fig
    elif entered_site == 'VAFB SLC-4E':
        data = spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E']
        data = data.groupby('class')['class'].count()
        fig = px.pie(data, values='class', 
            names=data.index, 
            title='Total Success Launches for site VAFB SLC-4E')
        return fig
    elif entered_site == 'KSC LC-39A':
        data = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
        data = data.groupby('class')['class'].count()
        fig = px.pie(data, values='class', 
            names=data.index, 
            title='Total Success Launches for site KSC LC-39A')
        return fig
    elif entered_site == 'CCAFS SLC-40':
        data = spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40']
        data = data.groupby('class')['class'].count()
        fig = px.pie(data, values='class', 
            names=data.index, 
            title='Total Success Launches for site CCAFS SLC-40')
        return fig
        # return the outcomes piechart for a selected site



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site, payload_value):
    
    if entered_site == 'ALL':
        data2 = spacex_df
        data2 = data2[data2['Payload Mass (kg)'] >= payload_value[0]]
        data2 = data2[data2['Payload Mass (kg)'] <= payload_value[1]]
        fig = px.scatter(data2, x='Payload Mass (kg)', y='class',
            color=data2["Booster Version Category"],
            title='Correlation between Payload and Success for all Sites')
        return fig

    elif entered_site == 'CCAFS LC-40':
        data2 = spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40']
        data2 = data2[data2['Payload Mass (kg)'] >= payload_value[0]]
        data2 = data2[data2['Payload Mass (kg)'] <= payload_value[1]]
        fig = px.scatter(data2, x='Payload Mass (kg)', y='class',
            color=data2["Booster Version Category"],
            title='Correlation between Payload and Success for CCAFS LC-40')
        return fig
    elif entered_site == 'VAFB SLC-4E':
        
        data2 = spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E']
        data2 = data2[data2['Payload Mass (kg)'] >= payload_value[0]]
        data2 = data2[data2['Payload Mass (kg)'] <= payload_value[1]]
        fig = px.scatter(data2, x='Payload Mass (kg)', y='class',
            color=data2["Booster Version Category"],
            title='Correlation between Payload and Success for VAFB SLC-4E')
        return fig
    elif entered_site == 'KSC LC-39A':
        data2 = spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A']
        data2 = data2[data2['Payload Mass (kg)'] >= payload_value[0]]
        data2 = data2[data2['Payload Mass (kg)'] <= payload_value[1]]
        fig = px.scatter(data2, x='Payload Mass (kg)', y='class',
            color=data2["Booster Version Category"],
            title='Correlation between Payload and Success for KSC LC-39A')
        return fig
    elif entered_site == 'CCAFS SLC-40':
        data2 = spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40']
        data2 = data2[data2['Payload Mass (kg)'] >= payload_value[0]]
        data2 = data2[data2['Payload Mass (kg)'] <= payload_value[1]]
        fig = px.scatter(data2, x='Payload Mass (kg)', y='class',
            color=data2["Booster Version Category"],
            title='Correlation between Payload and Success for CCAFS SLC-40')
        return fig
    









# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
