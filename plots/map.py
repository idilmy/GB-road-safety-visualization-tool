from dash import dcc, html
import plotly.express as px
import pandas as pd


class MapBox(html.Div):
    """
    A class to create a Scatter Map component in our Dash app.

    """

    def __init__(self, html_id, data):
        """
        Initializes the Scatter Map with the specified HTML ID and data.

        Parameters:
        - html_id: The ID for the HTML component.
        - data: The data to be used in the MapBox.
        """
        self.html_id = html_id
        self.data = data
        self._encode()
        super().__init__(
            children=[
                dcc.Graph(id=self.html_id)  # Create a Graph component with the specified HTML ID
            ]
        )
        self.update(self.data, None, None)  # Initial update of the map with default options

    def _encode(self):
        """
        Encodes the data for use in the map.

        Converts date strings to datetime objects, extracts month names, and maps day of the week integers
        to their corresponding names.
        """
        self.data['date'] = pd.to_datetime(self.data['date'], dayfirst=True)
        self.data['month'] = self.data['date'].dt.strftime('%B')

        day_mapping = {
            1: 'Sunday',
            2: 'Monday',
            3: 'Tuesday',
            4: 'Wednesday',
            5: 'Thursday',
            6: 'Friday',
            7: 'Saturday'
        }
        self.data['day_of_week'] = self.data['day_of_week'].replace(day_mapping)

    def update(self, data, local_aut, display_option):
        """
        Updates the map based on the provided data, selected local authority, and display option.

        Parameters:
        - data: The data to be used for updating the map.
        - local_aut: The selected local authority.
        - display_option: The display option ('all' or 'aggregated').

        Returns:
        - A Plotly figure object. (Scatter Map)
        """
        # Define color schemes
        elegant_colors = {
            'background': '#F5F5F5',
            'text': '#383838',
            'accent': '#76B041'
        }
        severity_colors = {
            'Fatal': 'rgba(139, 0, 0, 0.5)',
            'Serious': 'rgba(255, 0, 0, 0.5)',
            'Slight': 'rgba(255, 159, 0, 0.5)'
        }
        self.data = data
        if display_option is None:
            display_option = 'all'

        df = data.copy()
        max_size = 15

        if local_aut is None:
            # Set default center and zoom level if no local authority is selected
            center_lat = 55.09621
            center_long = -4.0286298
            zoom_level = 4.6
        else:
            # Filter data for the selected local authority
            df = data[data['local_authority_ons_district'] == local_aut]
            center_lat = df['latitude'].median()
            center_long = df['longitude'].median()
            difference_lat = abs(df['latitude'].max() - df['latitude'].min())
            zoom_level = 11 - difference_lat * 12 / 10

        if display_option == 'aggregated':
            # Aggregate data by local authority for the 'aggregated' display option
            data = data.groupby('local_authority_ons_district').agg(
                latitude=('latitude', 'mean'),
                longitude=('longitude', 'mean'),
                number_of_casualties=('number_of_casualties', 'sum'),
                accident_severity=('accident_severity', lambda x: x.mode()[0])
            ).reset_index()
            max_size = 30
            severity_colors = {
                'Fatal': '#8B0000',
                'Serious': '#FF0000',
                'Slight': '#FF9F00'
            }
        elif display_option == 'all':
            # Use the filtered data for the 'all' display option
            data = df.copy()

        if self.data.empty:
            # Handle case where data is empty
            self.fig = px.scatter_mapbox(lat=[], lon=[],
                                         size_max=max_size, zoom=zoom_level,
                                         center={"lat": center_lat, "lon": center_long},
                                         mapbox_style="carto-positron")

            self.fig.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                paper_bgcolor="#F5F5F5",
                plot_bgcolor="#F5F5F5",
                font=dict(
                    family="Helvetica Neue, sans-serif",
                    size=12,
                    color="#383838",
                ),
                showlegend=False,
            )
            return self.fig
        else:
            # Ensure latitude and longitude are of float type
            self.data["latitude"] = self.data["latitude"].astype(float)
            self.data["longitude"] = self.data["longitude"].astype(float)

            self.fig = px.scatter_mapbox(data, lat="latitude", lon="longitude",
                                         color="accident_severity",
                                         color_discrete_map=severity_colors,
                                         size="number_of_casualties",
                                         size_max=max_size,
                                         zoom=zoom_level,
                                         center={"lat": center_lat, "lon": center_long},
                                         mapbox_style="carto-positron")

            self.fig.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                paper_bgcolor=elegant_colors['background'],
                plot_bgcolor=elegant_colors['background'],
                font=dict(
                    family="Helvetica Neue, sans-serif",
                    size=12,
                    color=elegant_colors['text'],
                ),
                showlegend=False,
                coloraxis_showscale=False,
            )

            return self.fig
