import pandas as pd
import dash
from dash import html, dcc, Input, Output, State
from dash import callback_context
import dash_bootstrap_components as dbc
import calendar

from plots.map import MapBox
from plots.hbar import HorizontalBarChart
from plots.line import LineChart
from plots.heatmap import HeatMap
import plotly.graph_objects as go
from README import readme_html


# Dash App initialization
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[
                    dbc.themes.BOOTSTRAP,
                    'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
                    '/assets/style.css'
                ])
app.title = 'VisTool'
df = pd.read_csv('merged_collision_data.csv', low_memory=False, on_bad_lines='skip')


# Colours used throughout pages
elegant_colors = {
    'background': '#F5F5F5',
    'text': '#383838',
    'accent': '#76B041',
    'black': '#000000',
    'background_darker': '#D8DCDC'
}

map = MapBox(html_id='map-graph', data=df)
hbar = HorizontalBarChart(html_id='hbar-graph', data=df)
line = LineChart(html_id='line-graph', data=df)
heatmap = HeatMap(html_id='heatmap-graph', data=df)


month_to_abbr = {month: abbr for month, abbr in zip(calendar.month_name[1:], calendar.month_abbr[1:])}
months = {i + 1: {'label': abbr} for i, abbr in enumerate(calendar.month_abbr[1:])}

df['local_authority_ons_district'] = df['local_authority_ons_district'].replace('E06000057', 'Northumberland')
df['local_authority_ons_district'] = df['local_authority_ons_district'].replace('E06000058', 'Bournemouth,'
                                                                                             ' Christchurch, Poole')
df['local_authority_ons_district'] = df['local_authority_ons_district'].replace('E06000059', 'Dorset')
df['local_authority_ons_district'] = df['local_authority_ons_district'].replace('E06000060', 'Buckinghamshire')
df['local_authority_ons_district'] = df['local_authority_ons_district'].replace('E06000061', 'North Northamptonshire')
df['local_authority_ons_district'] = df['local_authority_ons_district'].replace('E06000062', 'West Northamptonshire')
df['local_authority_ons_district'] = df['local_authority_ons_district'].replace('E08000037', 'Gateshead')
df['local_authority_ons_district'] = df['local_authority_ons_district'].replace('S12000047', 'Fife')
df['local_authority_ons_district'] = df['local_authority_ons_district'].replace('S12000048', 'Perth and Kinross')
df['local_authority_ons_district'] = df['local_authority_ons_district'].replace('S12000049', 'Glasgow City')
df['local_authority_ons_district'] = df['local_authority_ons_district'].replace('S12000050', 'North Lanarkshire')



def build_left_container_mapbox():
    """
       Constructs the left container for the first page in our Dash app.
       This container includes dropdowns for selecting local authorities and severity levels,
       a range slider for selecting a month range, buttons as display options, and a section
       to display total casualties and a tree map.
       """

    # Get sorted unique local authorities and accident severities from the dataframe
    local_authorities = sorted(df['local_authority_ons_district'].unique())
    acc_sev = sorted(df['accident_severity'].unique())

    # Create the layout of the left container
    return html.Div(
        id='left-container',
        className='slide-out',
        style={
            'background-color': elegant_colors['background'],
            'width': '34%',
            'height': '100%',
            'border-radius': '10px',
            'padding': '20px',
            'color': elegant_colors['text'],
            'marginLeft': '0'
        },
        children=[
            # Header for the visualization section
            html.H3("Visualisation: GB Road Safety Data", style={'textAlign': 'center',
                                                                 'color': elegant_colors['text']}),
            # Container for dropdowns
            html.Div([
                # Local authority dropdown
                html.Div([
                    html.P("Select a local authority",
                           style={'textAlign': 'center', 'color': elegant_colors['text']}),
                    dcc.Dropdown(
                        id='local-dropdown',
                        options=[{'label': local, 'value': local} for local in local_authorities],
                        placeholder="Select an authority",
                        style={'width': '200px', 'color': elegant_colors['text'],
                               'background': elegant_colors['background'],
                               'border': f'1px solid {elegant_colors["background_darker"]}',
                               'box-shadow': 'rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px'}
                    ),
                ], style={'display': 'inline-block', 'margin-left': '35px', 'margin-top': '10px'}),
                # Accident severity dropdown
                html.Div([
                    html.P("Select a severity level",
                           style={'textAlign': 'center', 'color': elegant_colors['text']}),
                    dcc.Dropdown(
                        id='severity-dropdown',
                        options=[{'label': severity, 'value': severity} for severity in acc_sev],
                        placeholder="Select a severity",
                        style={'width': '200px', 'color': elegant_colors['text'],
                               'background': elegant_colors['background'],
                               'border': f'1px solid {elegant_colors["background_darker"]}',
                               'box-shadow': 'rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px'}
                    ),
                ], style={'display': 'inline-block', 'margin-left': '30px', 'margin-top': '10px'}),
            ], style={'display': 'flex', 'justify-content': 'start', 'align-items': 'center'}),
            # Month range slider
            html.Div([
                html.P("Select a month range",
                       style={'textAlign': 'left', 'color': elegant_colors['text'], 'margin-left': '30px'}),
                dcc.RangeSlider(
                    id='month-range-slider',
                    min=1,
                    max=12,
                    step=1,
                    value=[1, 12],
                    marks={i: month for i, month in month_to_abbr.items()},
                    tooltip={"placement": "bottom", "always_visible": False},
                    className='dash-slider'
                )
            ], style={'margin-top': '10px', 'width': '450px', 'margin-left': '20px'}),
            # Display options and total casualties
            html.Div([
                # Display options for buttons
                html.Div([
                    html.P("Map Display:",
                           style={'textAlign': 'left', 'color': elegant_colors['text'], 'margin-left': '20px'}),
                    dcc.RadioItems(
                        id='display-options',
                        options=[
                            {'label': 'All', 'value': 'all'},
                            {'label': 'Aggregated', 'value': 'aggregated'}
                        ],
                        value='aggregated',
                        labelStyle={'display': 'inline-block', 'margin-right': '10px'},
                        style={'textAlign': 'center', 'color': elegant_colors['text']}
                    ),
                ], style={'background': elegant_colors['background_darker'],
                          'border': f'1px solid {elegant_colors["background_darker"]}',
                          'box-shadow': 'rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px',
                          'padding': '5px', 'height': '70px', 'margin-left': '70px'}),
                # Total casualties display
                html.Div([
                    html.P("Total Casualties:",
                           style={'textAlign': 'center', 'color': elegant_colors['text'], 'margin-left': '10px'}),
                    html.Div(id='total-casualties',
                             style={'textAlign': 'center', 'color': elegant_colors['text'], 'margin-top': '10px'})
                ], style={'background': elegant_colors['background_darker'],
                          'border': f'1px solid {elegant_colors["background_darker"]}',
                          'box-shadow': 'rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px',
                          'padding': '5px', 'margin-left': '20px', 'height': '70px'})
            ], style={'display': 'flex', 'margin-top': '10px'}),
            # Tree map display
            html.Div([
                # Function call to generate the tree map
                tree_map()
            ], style={'margin-top': '5px'})
        ]
    )


def toggle_button():
    """
        Creates a toggle button to fully view the scatter map in Dash app.
        This button allows users to go in between the left container and the scatter map.
        """
    return html.Div(
        id='toggle-menu-container',
        className='toggle-menu-opened',
        style={'position': 'absolute', 'left': '34%', 'top': '50%', 'transform': 'translate(0, -50%)'},
        children=[
            # Button to toggle
            html.Button(
                id='toggle-menu',
                className='btn btn-default',
                # Tracks the number of clicks
                n_clicks=0
            )
        ]
    )


def tree_map():
    """
        Creates a hierarchical tree map visualization for various conditions affecting road safety.
        The tree map includes weather conditions, road conditions, light conditions, area types,
        road types, and speed limits.
        """

    # Define the data
    weather_conditions = ["Fine no high winds", "Raining no high winds", "Snowing no high winds",
                          "Fine + high winds", "Raining + high winds", "Snowing + high winds", "Fog or mist", "Other"]
    road_conditions = ["Dry", "Wet or damp", "Snow", "Frost or ice", "Flood over 3cm deep", "Oil or diesel", "Mud"]
    light_conditions = ["Daylight", "Darkness + lights lit", "Darkness + lights unlit", "Darkness + no lighting",
                        "Darkness - lighting unknown"]
    urban_rural_areas = ["Urban", "Rural"]
    road_types = ["Roundabout", "One way street", "Dual carriageway", "Single carriageway", "Slip road",
                  "One way street/Slip road", "Unknown"]
    speed_limits = ['20', '50', '30', '40', '60', '70']

    ids = ["All", "Weather Conditions", "Area Type"]
    labels = ["All", "Weather Conditions", "Area Type"]
    parents = ["", "All", "All"]

    # Expand Weather Conditions
    for weather in weather_conditions:
        ids.append(weather)
        labels.append(weather)
        parents.append("Weather Conditions")

        road_label_id = f"{weather} - Road Conditions"
        ids.append(road_label_id)
        labels.append("Road Conditions")
        parents.append(weather)

        # Expand Road Surface Conditions for each Weather Condition
        for road in road_conditions:
            road_id = f"{road_label_id} - {road}"
            ids.append(road_id)
            labels.append(road)
            parents.append(road_label_id)

            # Add Light Conditions placeholder for each Road Surface Condition
            light_label_id = f"{road_id} - Light Conditions"
            ids.append(light_label_id)
            labels.append("Light Conditions")
            parents.append(road_id)

            # Expand Light Conditions for each Road Condition
            for light in light_conditions:
                light_id = f"{light_label_id} - {light}"
                ids.append(light_id)
                labels.append(light)
                parents.append(light_label_id)

    # Expand Area Type
    for area in urban_rural_areas:
        area_id = f"{area}"
        ids.append(area_id)
        labels.append(area)
        parents.append("Area Type")

        road_type_label_id = f"{area} - Road Type"
        ids.append(road_type_label_id)
        labels.append("Road Type")
        parents.append(area_id)

        # Add Road Types under each Urban or Rural Area
        for road_type in road_types:
            road_type_id = f"{road_type_label_id} - {road_type}"
            ids.append(road_type_id)
            labels.append(road_type)
            parents.append(road_type_label_id)

            # Add Speed Limit placeholder for each Road Type
            speed_limit_label_id = f"{road_type_id} - Speed Limit"
            ids.append(speed_limit_label_id)
            labels.append("Speed Limit")
            parents.append(road_type_id)

            # Add Speed Limits under each Road Type
            for speed in speed_limits:
                speed_id = f"{speed_limit_label_id} - {speed}"
                ids.append(speed_id)
                labels.append(speed)
                parents.append(speed_limit_label_id)
    # Create a DataFrame from the hierarchical data
    df = pd.DataFrame({
        'ids': ids,
        'labels': labels,
        'parents': parents
    })
    # Create the tree map figure
    fig = go.Figure()
    fig.add_trace(go.Treemap(
        ids=df['ids'],
        labels=df['labels'],
        parents=df['parents'],
        maxdepth=2,  # Adjust depth as needed
        root_color="lightgrey",
    ))
    fig.update_layout(margin=dict(t=20, l=25, r=25, b=20), paper_bgcolor='rgba(0,0,0,0)')
    return dcc.Graph(id='treemap-graph', figure=fig, style={'height': '400px'})


def build_map_tab():
    """
       Constructs the layout for the first page in our Dash app.
       This includes a left container for filters, a toggle button for the scatter map,
       a map container for displaying the map, and a legend for the map.
       """
    return html.Div(
        style={
            'position': 'relative',
            'height': '100vh',
            'backgroundColor': elegant_colors['background'],
            'margin-right': '10px'
        },
        children=[
            # Container for the legend
            html.Div(
                style={
                    'position': 'absolute',
                    'top': '10px',
                    'right': '10px',
                    'zIndex': 1  # Ensure the legend stays on top
                },
                children=[
                    # Function call to create the legend
                    legend_type()
                ]
            ),
            # Main content container
            html.Div(
                style={
                    'display': 'flex',
                    'flexDirection': 'row',
                    'height': '100%',
                    'backgroundColor': elegant_colors['background']
                },
                children=[
                    # Left container function with filters
                    build_left_container_mapbox(),
                    # Toggle button for the slide left menu
                    toggle_button(),
                    html.Div(
                        id='map-container',
                        style={'flex': 1},
                        children=[
                            dcc.Graph(id='map-graph', figure=map.update(df, None, None), style={'flex': '1'})
                        ]
                    )
                ]
            )
        ]
    )


def legend_type():
    """
        Creates a legend for the map to indicate accident severity types.
        The legend includes icons and labels for 'Fatal', 'Serious', and 'Slight' accident severities.
        """
    return html.Div(
        id='map-legend',
        style={
            'display': 'flex',
            'flexDirection': 'column',
            'backgroundColor': 'rgba(255, 255, 255, 0.8)',
            'padding': '10px',
            'borderRadius': '5px',
            'boxShadow': 'rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px',
            'border': '1px solid black',
            'marginBottom': '10px',
            'height': '120px',
            'width': '120px'
        },
        children=[
            # Title of the legend
            html.P("Accident Severity",
                   style={'textAlign': 'center', 'color': elegant_colors['text'], 'fontWeight': 'bold',
                          'fontSize': '12px'}),
            # Legend for 'Fatal' accidents
            html.Div(
                style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '5px'},
                children=[
                    html.Img(src='/assets/fatal.png',
                             style={'width': '12px', 'height': '12px', 'marginRight': '5px'}),
                    html.Span("Fatal", style={'fontWeight': 'bold', 'fontSize': '10px'})
                ]
            ),
            # Legend for 'Serious' accidents
            html.Div(
                style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '5px'},
                children=[
                    html.Img(src='/assets/serious.png',
                             style={'width': '12px', 'height': '12px', 'marginRight': '5px'}),
                    html.Span("Serious", style={'fontWeight': 'bold', 'fontSize': '10px'})
                ]
            ),
            # Legend for 'Slight' accidents
            html.Div(
                style={'display': 'flex', 'alignItems': 'center'},
                children=[
                    html.Img(src='/assets/slight.png',
                             style={'width': '12px', 'height': '12px', 'marginRight': '5px'}),
                    html.Span("Slight", style={'fontWeight': 'bold', 'fontSize': '10px'})
                ]
            )
        ]
    )


def build_top_container_barChart():
    """
        Constructs the top container for a stacked bar chart visualization in our Dash app.
        This container includes dropdowns for selecting local authority, accident severity,
        and various vehicle, collision, and road-related attributes.
        """

    # Get sorted unique local authorities and accident severities from the dataframe
    local_authorities = sorted(df['local_authority_ons_district'].unique())
    acc_sev = sorted(df['accident_severity'].unique())

    return html.Div(
        style={
            'display': 'flex',
            'padding': '2px',
            'backgroundColor': elegant_colors['background'],
            'margin-bottom': '10px'  # Space between top container and charts
        },
        children=[
            # Combined container for selecting local authority and accident severity
            html.Div([
                # Sub-container for Local Authority Dropdown
                html.Div([
                    html.P("Select Local Authority", style={'textAlign': 'left', 'color': elegant_colors['text'],
                                                            'margin-left': '10px'}),
                    dcc.Dropdown(
                        id='local-authority-dropdown',
                        options=[{'label': local, 'value': local} for local in local_authorities],
                        placeholder="Select local authority",
                        style={'width': '142px', 'color': elegant_colors['text'], 'margin-left': '5px'}
                    ),
                ], style={
                    'flex': '1',  # Takes up 1 portion of the flex container
                }),

                # Sub-container for Accident Severity Buttons
                html.Div([
                    html.P("Accident Severity:",
                           style={'textAlign': 'center', 'color': elegant_colors['text'], 'margin-left': '10px'}),
                    dcc.Dropdown(
                        id='accident-severity-dropdown',
                        options=[{'label': severity, 'value': severity} for severity in acc_sev],
                        placeholder="Select a Severity",
                        style={'width': '142px', 'color': elegant_colors['text'], 'margin-left': '10px'}
                    ),
                ], style={
                    'flex': '1',
                    'alignItems': 'center',
                    'flexDirection': 'column',
                }),
                # Sub-container for RatioItems
                html.Div([
                    html.P("Data:",
                           style={'textAlign': 'left', 'color': elegant_colors['text'], 'margin-right': '110px'}),
                    dcc.RadioItems(
                        id='data-options',
                        options=[
                            {'label': 'All', 'value': 'all'},
                            {'label': 'Excluded', 'value': 'excluded'}
                        ],
                        value='all',
                        labelStyle={'display': 'inline-block', 'margin-right': '5px'},
                        style={'textAlign': 'center', 'color': elegant_colors['text']}
                    ),
                ])
            ], style={
                'display': 'flex',
                'width': '500px',
                'background': elegant_colors['background_darker'],
                'padding': '5px',
                'border-radius': '5px',
                'margin-left': '20px',
                'margin-top': '10px',
                'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px'
            }),
            # Container for Vehicle Related Attributes Dropdown
            html.Div([
                html.H4("Vehicle Related Attributes", style={'textAlign': 'center', 'color': elegant_colors['text']}),
                dcc.Dropdown(
                    id='vehicle-dropdown',
                    options=[{'label': vehicleAttr, 'value': vehicleAttr} for vehicleAttr in
                             ['Vehicle Type', 'Propulsion Type', 'Vehicle Manoeuvre']],
                    placeholder="Select an attribute",
                    style={'width': '100%', 'color': elegant_colors['text'], 'margin-top': '20px',
                           'background': elegant_colors['background'],
                           'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px'}
                ),
            ], style={
                'display': 'inline-block',
                'width': '350',
                'height': '100px',
                'margin-left': '20px',
                'margin-top': '10px',
                'background': elegant_colors['background_darker'],
                'padding': '10px',
                'border-radius': '5px',
                'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px'
            }),
            # Container for Collision Related Attributes Dropdown
            html.Div([
                html.H4("Collision Related Attributes", style={'textAlign': 'center', 'color': elegant_colors['text']}),
                dcc.Dropdown(
                    id='casualty-dropdown',
                    options=[{'label': casualtyAttr, 'value': casualtyAttr} for casualtyAttr in
                             ['Casualty Class', 'Casualty Type', 'First Impact Point', 'Hit Object in Carriageway']],
                    placeholder="Select an attribute",
                    style={'width': '100%', 'color': elegant_colors['text'], 'margin-top': '20px',
                           'background': elegant_colors['background'],
                           'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px'
                           }
                ),
            ], style={
                'display': 'inline-block',
                'width': '350',
                'height': '100px',
                'margin-left': '20px',
                'margin-top': '10px',
                'background': elegant_colors['background_darker'],
                'padding': '10px',
                'border-radius': '5px',
                'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px'
            }),
            # Container for Road Related Attributes Dropdown
            html.Div([
                html.H4("Road Related Attributes", style={'textAlign': 'center', 'color': elegant_colors['text']}),
                dcc.Dropdown(
                    id='road-dropdown',
                    options=[{'label': roadAttr, 'value': roadAttr} for roadAttr in
                             ['Road Type', 'First Road Class', 'Second Road Class', 'Junction Location',
                              'Junction Control', 'Junction Detail']],
                    placeholder="Select an attribute",
                    style={'width': '100%', 'color': elegant_colors['text'], 'margin-top': '20px',
                           'background': elegant_colors['background'],
                           'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px'
                           }
                ),
            ], style={
                'display': 'inline-block',
                'width': '350',
                'height': '100px',
                'margin-left': '20px',
                'margin-top': '10px',
                'background': elegant_colors['background_darker'],
                'padding': '10px',
                'border-radius': '5px',
                'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px'
            }),
        ]
    )


def build_bottom_line_container(df_filtered):
    """
        Constructs the bottom container for a line chart visualization in our Dash app.
        This container includes a title, a dropdown for selecting the x-axis attribute,
        and the line chart itself.
        Parameters:
        - df_filtered: DataFrame with filtered data based on user selections.
        """

    return html.Div([
        html.Div(
            style={'display': 'flex', 'flexDirection': 'column', 'flex': '1'},
            children=[
                # Line chart container
                html.Div(
                    style={
                        'position': 'relative',  # Ensure absolute positioning works inside this container
                        'backgroundColor': elegant_colors['background_darker'],
                        'padding': '10px',
                        'margin-top': '5px',
                        'margin-bottom': '20px',
                        'border-radius': '5px',
                        'width': '1470px',
                        'height': '500px',
                        'margin-left': '30px',
                        'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px',
                    },
                    children=[
                        # Title and dropdown container
                        html.Div(
                            style={
                                'position': 'absolute',
                                'top': '10px',
                                'left': '10px',
                                'backgroundColor': elegant_colors['background'],
                                'padding': '20px',
                                'border-radius': '5px',
                                'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px',
                                'border': f'1px solid {elegant_colors["background_darker"]}'
                            },
                            children=[
                                # Title for the line chart
                                html.H4('Ordered Attribute Analysis', style={'marginBottom': '10px',
                                                                             'textAlign': 'center'}),
                                html.Div(
                                    style={'display': 'flex', 'width': '100%'},
                                    children=[
                                        html.Div(
                                            style={'margin-left': '30px'},
                                            children=[
                                                # Dropdown for selecting the x-axis attribute
                                                dcc.Dropdown(
                                                    id='line-x-dropdown',
                                                    options=[{'label': xAxis, 'value': xAxis} for xAxis in
                                                             ['Time of the Day', 'Day of the Week', 'Month of the Year',
                                                              'Age band of Driver', 'Speed Limit']],
                                                    placeholder="Select an Attribute",
                                                    style={'width': '180px', 'color': elegant_colors['text']}
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        ),
                        # Line chart visualization
                        dcc.Graph(
                            id='line-chart',
                            # Function call to update the line chart with filtered data
                            figure=line.update(df_filtered, None),
                            style={'width': '1000px', 'height': '500px', 'margin-left': '300px', 'margin-right': '20px'}
                        )
                    ]
                )
            ]
        )
    ])


def build_bar_tab(df_filtered, active_severity):
    """
        Constructs the layout for the second page in our Dash app.
        This layout includes a top container for filter selection, a horizontal bar chart,
        and a bottom container for line chart analysis.

        Parameters:
        - df_filtered: DataFrame with filtered data based on user selections.
        - active_severity: The active severity level.
        """

    # Filter the DataFrame based on the active severity
    if active_severity:
        df_filtered = df_filtered[df_filtered['accident_severity'] == active_severity]
    else:
        df_filtered = df_filtered
    return html.Div(
        style={
            'display': 'flex',
            'flexDirection': 'row',
            'minHeight': '100vh',
            'backgroundColor': elegant_colors['background'],
        },
        children=[
            # Main content container
            html.Div(
                style={'display': 'flex', 'flexDirection': 'row', 'flex': '1', 'alignItems': 'flex-start'},
                children=[
                    # Left side vertical layout for charts and analysis
                    html.Div(
                        style={'display': 'flex', 'flexDirection': 'column', 'flex': '1'},
                        children=[
                            # Top container function for filter selection
                            build_top_container_barChart(),
                            # Horizontal bar chart container
                            html.Div(
                                style={
                                    'backgroundColor': elegant_colors['background_darker'],
                                    'padding': '20px',
                                    'margin': '10px 30px',
                                    'border-radius': '5px',
                                    'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px'
                                },
                                children=[
                                    # Horizontal bar chart visualization
                                    dcc.Graph(
                                        id='hbar-chart',
                                        figure=hbar.update(df_filtered, None, None),
                                        style={'height': '100%'}
                                    ),
                                ]
                            ),
                            # Bottom line chart container
                            html.Div(
                                style={'display': 'flex', 'flexDirection': 'row', 'flex': '1',
                                       'alignItems': 'flex-start'},
                                children=[
                                    build_bottom_line_container(df_filtered)
                                ]
                            ),
                        ]
                    ),
                ]
            )
        ]
    )


def build_left_container_heatmap():
    """
       Constructs the left container for a heatmap visualization in our Dash app.
       This container includes dropdowns for selecting x and y axis attributes,
       and buttons for selecting the data used in the heatmap.
       """
    return html.Div(
        style={
            'display': 'flex',
            'flexDirection': 'row',
            'height': '100vh',
            'backgroundColor': elegant_colors['background'],
            'padding': '10px'
        },
        children=[
            # Main container for the heatmap controls
            html.Div(
                id='left-container-heat-map',
                style={
                    'background-color': elegant_colors['background_darker'],
                    'width': '340px',
                    'height': '100%',
                    'border-radius': '10px',
                    'padding': '10px',
                    'color': elegant_colors['text'],
                    'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px'
                },
                children=[
                    # Title for the heatmap section
                    html.H3("Correlation Analysis", style={'textAlign': 'center', 'color': elegant_colors['text']}),
                    html.Div([
                        # Container for x-axis attribute selection
                        html.Div([
                            html.P("Select attribute for x axis",
                                   style={'textAlign': 'left', 'color': elegant_colors['text'],
                                          'margin-right': '100px'}),
                            dcc.Dropdown(
                                id='correlation1',
                                options=[{'label': corr1, 'value': corr1} for corr1 in ['First Point of Impact',
                                                                                        'Pedestrian Movement',
                                                                                        'Junction Location',
                                                                                        'Junction Control',
                                                                                        'Casualty Class',
                                                                                        'Vehicle Manoeuvre']],
                                placeholder="Select an attribute",
                                style={'width': '200px', 'color': elegant_colors['text'],
                                       'background': elegant_colors['background'],
                                       'border': f'1px solid {elegant_colors["background_darker"]}',
                                       'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px'
                                       }
                            ),
                        ], style={'display': 'inline-block', 'margin-left': '10px', 'margin-top': '20px'}),
                        html.Div([
                            html.P("Select attribute for y axis",
                                   style={'textAlign': 'left', 'color': elegant_colors['text'],
                                          'margin-right': '100px'}),
                            dcc.Dropdown(
                                id='correlation2',
                                options=[{'label': corr2, 'value': corr2} for corr2 in ['First Point of Impact',
                                                                                        'Pedestrian Movement',
                                                                                        'Junction Location',
                                                                                        'Junction Control',
                                                                                        'Casualty Class',
                                                                                        'Vehicle Manoeuvre']],
                                placeholder="Select an attribute",
                                style={'width': '200px', 'color': elegant_colors['text'],
                                       'background': elegant_colors['background'],
                                       'border': f'1px solid {elegant_colors["background_darker"]}',
                                       'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px'}
                            ),
                        ], style={'display': 'inline-block', 'margin-left': '10px', 'margin-top': '20px'}),

                        # Data selection RatioItems buttons container
                        html.Div(
                            style={
                                'backgroundColor': elegant_colors['background'],
                                'padding': '10px',
                                'borderRadius': '5px',
                                'width': '80%',  # Adjust width as needed
                                'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px',
                                'marginTop': '30px',
                            },
                            children=[
                                html.P("Data Used:",
                                       style={'textAlign': 'center', 'color': elegant_colors['text'],
                                              'marginLeft': '10px'}),
                                dcc.RadioItems(
                                    id='data-heatmap-options',
                                    options=[
                                        {'label': 'All', 'value': 'all'},
                                        {'label': 'Excluded', 'value': 'excluded'}
                                    ],
                                    value='all',
                                    labelStyle={'display': 'inline-block', 'margin-right': '10px'},
                                    style={'textAlign': 'center', 'color': elegant_colors['text']}
                                )
                            ]
                        )
                    ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})
                ]
            ),
        ]
    )


def build_heat_tab():
    """
        Constructs the layout for the heatmap tab (third page) in our Dash app.
        This layout includes a left container for attribute selection and a main area for displaying the heatmap.
        """
    return html.Div(
        style={
            'display': 'flex',
            'flexDirection': 'row',
            'height': '100vh',
            'backgroundColor': elegant_colors['background'],
            'padding': '0px',
            'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px',
            'overflow': 'hidden'
        },
        children=[
            # Left container for attribute selection
            build_left_container_heatmap(),
            # Main container for the heatmap visualization
            html.Div(
                id='heatmap-container',
                style={
                    'flex': '1',
                    'padding': '10px',
                    'height': '100vh',
                    'display': 'flex',
                    'flexDirection': 'column',
                    'overflow': 'hidden',
                },
                children=[
                    html.H4(
                        "Attribute Correlation Heatmap",
                        style={
                            'textAlign': 'center',
                            'color': elegant_colors['text'],
                            'marginBottom': '10px'
                        }
                    ),
                    html.Div(
                        style={
                            'flex': '1',
                            'background': elegant_colors['background_darker'],
                            'padding': '0px',
                            'border-radius': '5px',
                            'margin-left': '20px',
                            'margin-top': '10px',
                            'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px',
                            'overflow': 'hidden'
                        },
                        children=[
                            # Heatmap graph visualization
                            dcc.Graph(
                                id='heatmap-graph',
                                # Function call to update the heatmap with initial data
                                figure=heatmap.update(data=df, corr1=None, corr2=None),
                                style={
                                    'height': '100%',
                                    'width': '100%',
                                    'overflow': 'hidden'
                                }
                            )
                        ]
                    )
                ]
            )
        ]
    )


def select_dataframe(data, include_missing, selected_column):
    """
        Filters a DataFrame based on whether to include rows with missing values in a specified column.

        Parameters:
        - data: The original DataFrame to filter.
        - include_missing: Boolean flag indicating whether to include rows with missing values.
        - selected_column: The column to check for missing values.

        Returns:
        - filtered_df: The filtered DataFrame.
        """

    filtered_df = data
    # If including missing values, return the original DataFrame
    if include_missing:
        return filtered_df
    else:
        # List of possible representations of missing values
        missing_values = ['Unknown', 'Not known', 'Other/Not known', 'Other', 'Undefined',
                          'Data missing or out of range', 'Data missing', 'Unclassified', 'Unallocated',
                          'unknown (self reported)', 'Unknown vehicle type (self rep only)', 'Other vehicle', -1, -1.0,
                          'Unknown (self reported)', 'Unknown or other']
        # Filter out rows with missing values in the selected column
        filtered_df = filtered_df[~filtered_df[selected_column].isin(missing_values)]

    return filtered_df


def view_modal(readme_html):
    """
       Creates and returns a modal (pop-up) for displaying information in our Dash app.
       Parameters:
       - readme_html: html text file to use for ModalBody

       Returns:
       - A Dash Bootstrap Component Modal.
       """

    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Information README")),
            dbc.ModalBody(html.Iframe(srcDoc=readme_html, style={"width": "100%", "height": "500px", "border": "none"})),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-modal", className="ms-auto", n_clicks=0)
            ),
        ],
        id="view-modal",
        # Initially open for the first tab, Map View
        is_open=True,
        size="lg",
        style={"maxWidth": "80%"}
    )


app.layout = html.Div([
    # Container for tabs and info button
    html.Div(
        style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '10px'},
        children=[
            dbc.Tabs([
                dbc.Tab(label="Map View", tab_id="tab-map"),
                dbc.Tab(label="Statistical Analysis", tab_id="tab-barchart"),
                dbc.Tab(label="Correlation Analysis", tab_id="tab-heat-map")
            ], id="tabs", active_tab="tab-map"),
            dbc.Button("Info", id="open-modal-button", style={'margin-left': 'auto', 'margin-right': '10px'})
        ]
    ),
    # Container for the content of the selected tab
    html.Div(id="tab-content", style={'width': '100%'}),
    # Hidden div for storing intermediate values or triggering callbacks
    html.Div(id='dummy-div', style={'display': 'none'}),

    view_modal(readme_html)
])


def vehicle_attribute_masking(selected_attribute):
    """
       Maps the selected vehicle-related attribute to its corresponding column name in the dataset.

       Parameters:
       - selected_attribute: The name of the vehicle attribute.

       Returns:
       - Tuple of selected_attribute and selected_type, where selected_attribute is the dataset column name,
         and selected_type is a string ('vehicle').
       """
    selected_type = 'vehicle'
    if selected_attribute == 'Vehicle Type':
        selected_attribute = 'vehicle_type'
    elif selected_attribute == 'Propulsion Type':
        selected_attribute = 'propulsion_code'
    elif selected_attribute == 'Vehicle Manoeuvre':
        selected_attribute = 'vehicle_manoeuvre'
    return selected_attribute, selected_type


def casualty_attribute_masking(selected_attribute):
    """
        Maps the selected casualty-related attribute to its corresponding column name in the dataset.

       Parameters:
        - selected_attribute: The name of the casualty attribute.

        Returns:
        - Tuple of selected_attribute and selected_type, where selected_attribute is the dataset column name,
          and selected_type is a string ('casualty').
        """
    selected_type = 'casualty'
    if selected_attribute == 'Casualty Class':
        selected_attribute = 'casualty_class'
    elif selected_attribute == 'Casualty Type':
        selected_attribute = 'casualty_type'
    elif selected_attribute == 'First Impact Point':
        selected_attribute = 'first_point_of_impact'
    elif selected_attribute == 'Hit Object in Carriageway':
        selected_attribute = 'hit_object_in_carriageway'
    return selected_attribute, selected_type


def road_attribute_masking(selected_attribute):
    """
       Maps the selected road-related attribute to its corresponding column name in the dataset.

        Parameters:
       - selected_attribute: The name of the road attribute.

       Returns:
       - Tuple of selected_attribute and selected_type, where selected_attribute is the dataset column name,
         and selected_type is a string ('road').
       """
    selected_type = 'road'
    if selected_attribute == 'Road Type':
        selected_attribute = 'road_type'
    elif selected_attribute == 'First Road Class':
        selected_attribute = 'first_road_class'
    elif selected_attribute == 'Second Road Class':
        selected_attribute = 'second_road_class'
    elif selected_attribute == 'Junction Location':
        selected_attribute = 'junction_location'
    elif selected_attribute == 'Junction Control':
        selected_attribute = 'junction_control'
    elif selected_attribute == 'Junction Detail':
        selected_attribute = 'junction_detail'
    return selected_attribute, selected_type


def accident_severity_masking(selected_severity):
    """
       Filters the dataset based on the selected accident severity.

       Parameters:
       - selected_severity: The name of the accident severity.

       Returns:
       - filtered_df: DataFrame filtered by the selected accident severity.
       """
    filtered_df = df.copy()
    if selected_severity == 'Slight':
        filtered_df = filtered_df[filtered_df['accident_severity'] == 'Slight']
    elif selected_severity == 'Serious':
        filtered_df = filtered_df[filtered_df['accident_severity'] == 'Serious']
    elif selected_severity == 'Fatal':
        filtered_df = filtered_df[filtered_df['accident_severity'] == 'Fatal']
    return filtered_df


def treemap_masking(clickData, df):
    """
    Filters the DataFrame based on the hierarchy path provided by the clickData from a treemap.

    Parameters:
    - clickData: The data from a click event on the treemap.
    - df: The original DataFrame to be filtered.

    Returns:
    - filtered_df: The DataFrame filtered based on the hierarchy path from clickData.
    """
    filtering_df = df.copy()
    # Normalize data for matching conditions
    filtering_df['light_conditions'] = filtering_df['light_conditions'].str.replace('-', '+')
    filtering_df['speed_limit'] = filtering_df['speed_limit'].astype(str)

    # Check if clickData is valid
    if clickData is None or 'points' not in clickData or not clickData['points']:
        return filtering_df

    # Extract the path from clickData
    path = clickData['points'][0]['id'].split(' - ')

    if "All" in path:
        return filtering_df

    # Map for condition names to DataFrame column names
    condition_map = {
        "Weather Conditions": "weather_conditions",
        "Road Conditions": "road_surface_conditions",
        "Light Conditions": "light_conditions",
        "Area Type": "urban_or_rural_area",
        "Road Type": "road_type",
        "Speed Limit": "speed_limit"
    }

    filtered_df = filtering_df

    # Determine the initial key for filtering
    if any(condition in path[0] for condition in
           ["Fine no high winds", "Raining no high winds", "Snowing no high winds", "Fine + high winds",
            "Raining + high winds", "Snowing + high winds", "Fog or mist", "Other", "Dry", "Wet or damp",
            "Snow", "Frost or ice", "Flood over 3cm deep", "Oil or diesel", "Mud"]):
        current_key = condition_map["Weather Conditions"]
    elif any(condition in path[0] for condition in ["Urban", "Rural", "Roundabout", "One way street",
                                                    "Dual carriageway", "Single carriageway",
                                                    "Slip road", "One way street/Slip road", "Unknown", "20", "30",
                                                    "40", "50", "60", "70"]):
        current_key = condition_map["Area Type"]
    else:
        current_key = condition_map["Weather Conditions"]

    # Apply filters based on the path
    for part in path:
        if part in condition_map:
            current_key = condition_map[part]
        elif current_key:
            cleaned_part = part.strip()
            if cleaned_part not in filtering_df[current_key].unique():
                filtered_df = pd.DataFrame(columns=filtered_df.columns)  # Return empty DataFrame with same columns
            else:
                filtered_df = filtered_df[filtered_df[current_key] == cleaned_part]

    return filtered_df if not filtered_df.empty else pd.DataFrame(columns=df.columns)


def heatmap_masking(correlation):
    """
       Maps the selected correlation attribute to its corresponding column name in the dataset.

       Parameters:
       - correlation: The name of the correlation attribute.

       Returns:
       - correlation: The dataset column name corresponding to the selected correlation attribute.
       """
    if correlation == 'First Point of Impact':
        correlation = 'first_point_of_impact'
    elif correlation == 'Pedestrian Movement':
        correlation = 'pedestrian_movement'
    elif correlation == 'Junction Location':
        correlation = 'junction_location'
    elif correlation == 'Junction Control':
        correlation = 'junction_control'
    elif correlation == 'Casualty Class':
        correlation = 'casualty_class'
    elif correlation == 'Vehicle Manoeuvre':
        correlation = 'vehicle_manoeuvre'
    return correlation


# Client-side callback for toggling the left container
app.clientside_callback(
    """
    function(n_clicks) {
        const menuContainer = document.getElementById('toggle-menu-container');
        const leftContainer = document.getElementById('left-container');
        const mapContainer = document.getElementById('map-container');
        // Check if it's the initial load by examining if the leftContainer is already positioned correctly
        if (!window.initialized) {
            window.initialized = true;  // Set a flag to mark initialization
            return;  // Skip any further processing to maintain initial state
        }
        // Toggle the visibility based on the current state
        if (leftContainer.style.marginLeft === '0px' || leftContainer.style.marginLeft === '') {
            leftContainer.style.marginLeft = '-34%';  // Hide the left container
            menuContainer.style.left = '0';  // Move toggle to the edge
        } else {
            leftContainer.style.marginLeft = '0';  // Show the left container
            menuContainer.style.left = '34%';  // Move toggle to the right of the left container
        }
        // Adjust the map container width regardless of state
        mapContainer.style.width = leftContainer.style.marginLeft === '0' ? 'calc(66% - 10px)' : '100%';
        mapContainer.style.height = '100%';  // Adjust map container height
    }
    """,
    Output('dummy-div', 'children'),
    [Input('toggle-menu', 'n_clicks')]
)


# Callback for rendering tab content based on the active tab
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def render_tab_content(active_tab):
    filtered_df = df.copy()
    if active_tab == "tab-map":
        return build_map_tab()
    elif active_tab == "tab-barchart":
        return build_bar_tab(filtered_df, None)
    elif active_tab == 'tab-heat-map':
        return build_heat_tab()

    return "No tab selected"


# Callback for updating the map and total casualties based on user inputs
@app.callback(
    [Output('map-graph', 'figure'),
     Output('total-casualties', 'children')],
    [Input('local-dropdown', 'value'),
     Input('severity-dropdown', 'value'),
     Input('month-range-slider', 'value'),
     Input('treemap-graph', 'clickData'),
     Input('display-options', 'value')]
)
def update_map(selected_local_authority, selected_severity, month_range, selected_tree, display_option):
    """
       Updates the map based on user-selected filters such as local authority, severity, month range, and treemap selection.

       Parameters:
       - selected_local_authority: The selected local authority.
       - selected_severity: The selected accident severity.
       - month_range: The selected range of months.
       - selected_tree: The data from a click event on the treemap.
       - display_option: The display option (e.g., 'aggregated').

       Returns:
       - A tuple containing the updated map figure and total casualties.
       """

    filtered_df = df.copy()
    # Filter by selected local authority
    if selected_local_authority:
        filtered_df = filtered_df[filtered_df['local_authority_ons_district'] == selected_local_authority]
    # Filter by selected severity
    if selected_severity:
        filtered_df = filtered_df[filtered_df['accident_severity'] == selected_severity]
    # Filter by selected month range
    if month_range:
        selected_months = [calendar.month_abbr[i] for i in range(month_range[0], month_range[1] + 1)]
        filtered_df = filtered_df[df['month'].map(month_to_abbr).isin(selected_months)]
    # Apply treemap masking if selected
    if selected_tree:
        filtered_df = treemap_masking(selected_tree, filtered_df)
    # Aggregate data if 'aggregated' option is selected
    if display_option == 'aggregated':
        filtered_df = filtered_df.groupby('local_authority_ons_district').agg(
            latitude=('latitude', 'mean'),
            longitude=('longitude', 'mean'),
            number_of_casualties=('number_of_casualties', 'sum'),
            accident_severity=('accident_severity', lambda x: x.mode()[0])  # Most common severity
        ).reset_index()
    # Calculate total casualties
    total_casualties = filtered_df['number_of_casualties'].sum() if not filtered_df.empty else 0
    # Return updated map figure and total casualties
    return (map.update(data=filtered_df, local_aut=selected_local_authority, display_option=display_option),
            f"{total_casualties}")


# Callback for updating the line chart based on dropdown activity
@app.callback(
    Output('line-chart', 'figure'),  # Assume you have this in your layout for debugging
    [Input('line-x-dropdown', 'value')]
)
def line_update(selected_attribute):
    """
        Updates the line chart based on selected attributes, severity, and local authority.

        Parameters:
        - selected_attribute: The selected attribute for the x-axis.
        - selected_severity: The selected accident severity.
        - selected_ons: The selected local authority.

        Returns:
        - The updated line chart figure.
        """
    filtered_df = df.copy()
    s_attr = None
    if selected_attribute == 'Time of the Day':
        s_attr = 'time'
    elif selected_attribute == 'Day of the Week':
        s_attr = 'day_of_week'
    elif selected_attribute == 'Month of the Year':
        s_attr = 'month'
    elif selected_attribute == 'Age band of Driver':
        s_attr = 'age_band_of_driver'
    elif selected_attribute == 'Speed Limit':
        s_attr = 'speed_limit'
    return line.update(filtered_df, s_attr)


# Callback for updating the barchart based on dropdown inputs
@app.callback(
    [Output('vehicle-dropdown', 'value'),
     Output('casualty-dropdown', 'value'),
     Output('road-dropdown', 'value'),
     Output('hbar-chart', 'figure')],
    [Input('vehicle-dropdown', 'value'),
     Input('casualty-dropdown', 'value'),
     Input('road-dropdown', 'value'),
     Input('accident-severity-dropdown', 'value'),
     Input('data-options', 'value'),
     Input('local-authority-dropdown', 'value')]
)
def update_chart(selected_vtype, selected_ctype, selected_rtype, selected_severity, selected_dataframe, selected_ons):
    """
       Updates the horizontal bar chart and dropdown values based on user-selected filters.

       Parameters:
       - selected_vtype: The selected vehicle attribute.
       - selected_ctype: The selected casualty attribute.
       - selected_rtype: The selected road attribute.
       - selected_severity: The selected accident severity.
       - selected_dataframe: The selected data option (e.g., 'all', 'excluded').
       - selected_ons: The selected local authority.

       Returns:
       - A tuple containing the updated dropdown values and the updated horizontal bar chart figure.
       """

    # Get the context of the callback
    ctx = callback_context
    # Get the IDs of the inputs that triggered the callback
    trigger_ids = list(ctx.triggered_prop_ids.keys())
    # Filter by accident severity if selected
    filtered_df = df.copy()
    if selected_severity:
        filtered_df = accident_severity_masking(selected_severity)

    # Filter by local authority if selected
    if selected_ons:
        filtered_df = filtered_df[filtered_df['local_authority_ons_district'] == selected_ons]

    vehicle_value, casualty_value, road_value = None, None, None
    selected_attribute, selected_type = None, None

    # Check which dropdown triggered the callback
    if 'vehicle-dropdown.value' in trigger_ids:
        vehicle_value = selected_vtype
        selected_attribute, selected_type = vehicle_attribute_masking(vehicle_value)
    elif 'casualty-dropdown.value' in trigger_ids:
        casualty_value = selected_ctype
        selected_attribute, selected_type = casualty_attribute_masking(casualty_value)
    elif 'road-dropdown.value' in trigger_ids:
        road_value = selected_rtype
        selected_attribute, selected_type = road_attribute_masking(road_value)

    # Assign values to vehicle, collision, and road-based on selected type
    vehicle_value = vehicle_value if selected_type == 'vehicle' else None
    casualty_value = casualty_value if selected_type == 'casualty' else None
    road_value = road_value if selected_type == 'road' else None

    # Filter DataFrame based on data option
    if selected_dataframe == 'excluded':
        filtered_df = select_dataframe(filtered_df, include_missing=False, selected_column=selected_attribute)
    elif selected_dataframe == 'all':
        filtered_df = select_dataframe(filtered_df, include_missing=True, selected_column=selected_attribute)

    # Update the chart figure
    chart_figure = hbar.update(filtered_df, selected_attribute, selected_type)

    return vehicle_value, casualty_value, road_value, chart_figure


# Callback for updating the heatmap based on dropdown inputs
@app.callback(
    Output('heatmap-graph', 'figure'),
    [Input('correlation1', 'value'),
     Input('correlation2', 'value'),
     Input('data-heatmap-options', 'value')]
)
def update_heatmap(corr1, corr2, selected_dataframe):
    """
        Updates the heatmap based on selected correlation attributes and data options.

        Parameters:
        - corr1: The first correlation attribute.
        - corr2: The second correlation attribute.
        - selected_dataframe: The selected data option (e.g., 'all', 'excluded').

        Returns:
        - The updated heatmap figure.
        """

    filtered_df = df.copy()
    # Map correlation attributes to corresponding dataset columns
    corr1 = heatmap_masking(corr1)
    corr2 = heatmap_masking(corr2)
    # Filter DataFrame based on data option
    if selected_dataframe == 'excluded':
        filtered_df = select_dataframe(filtered_df, include_missing=False, selected_column=corr1)
        filtered_df = select_dataframe(filtered_df, include_missing=False, selected_column=corr2)
    elif selected_dataframe == 'all':
        filtered_df = df.copy()
    return heatmap.update(data=filtered_df, corr1=corr1, corr2=corr2)


# This function gets inputs and decides open or close for the pop-up based clicks.
@app.callback(
    Output("view-modal", "is_open"),
    [Input("open-modal-button", "n_clicks"), Input("close-modal", "n_clicks")],
    [State("view-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_modal(open_clicks, close_clicks, is_open):
    """
      Changes (open or close) the state of a modal based on button clicks.

      Parameters:
      - open_clicks: Number of clicks on the open button.
      - close_clicks: Number of clicks on the close button.
      - is_open: Current state of the modal (open or closed).

      Returns:
      - The new state of the modal (True if opening, False if closing, and current state if no action).
      """
    ctx = callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "open-modal-button":
        return not is_open
    elif button_id == "close-modal":
        return False
    return is_open


if __name__ == '__main__':
    app.run_server(debug=False, port='8585')
