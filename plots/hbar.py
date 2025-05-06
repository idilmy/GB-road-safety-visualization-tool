from dash import dcc, html
import plotly.graph_objects as go


class HorizontalBarChart(html.Div):
    """
    A class to create a horizontal bar chart component in our Dash app.

    """

    def __init__(self, html_id, data):
        """
        Initializes the HorizontalBarChart with the specified HTML ID and data.

        Parameters:
        - html_id: The ID for the HTML component.
        - data: The data to be used in the chart.
        """
        self.html_id = html_id
        self.data = data
        self.vehicle_attr = None
        self.casualty_attr = None
        self.road_attr = None
        super().__init__(
            children=[
                dcc.Graph(id=self.html_id)  # Create a Graph component with the specified HTML ID
            ]
        )

    def update(self, data, attribute, attribute_type):
        """
        Updates the chart based on the provided data and selected attribute.

        Parameters:
        - data: The data to be used for updating the chart.
        - attribute: The selected attribute to group the data by.
        - attribute_type: The type of the selected attribute ('vehicle', 'collision', 'road').

        Returns:
        - A Plotly object. (stacked bar chart)
        """
        self.data = data

        # Reset the attributes based on which dropdown is selected
        if attribute_type == 'vehicle':
            self.vehicle_attr = attribute
            self.casualty_attr = None
            self.road_attr = None
        elif attribute_type == 'casualty':
            self.casualty_attr = attribute
            self.vehicle_attr = None
            self.road_attr = None
        elif attribute_type == 'road':
            self.road_attr = attribute
            self.vehicle_attr = None
            self.casualty_attr = None

        # Determine the selected attribute
        selected_attribute = self.vehicle_attr or self.casualty_attr or self.road_attr or 'vehicle_type'

        # Group and process the data
        grouped_data = self.data.groupby([selected_attribute, 'accident_severity']).size().reset_index(name='count')
        grouped_data = grouped_data.sort_values(by='count', ascending=True)
        total_accidents = grouped_data['count'].sum()  # Calculate the total number of accidents

        # Calculate the percentage of each group relative to the total number of accidents
        grouped_data['percentage'] = (grouped_data['count'] / total_accidents * 100).apply(lambda x: f'{x:.2f}%')

        # Define color map for accident severity
        severity_colors = {
            'Fatal': '#8B0000',
            'Serious': '#FF0000',
            'Slight': '#FF9F00'
        }

        # Map severity colors
        grouped_data['color'] = grouped_data['accident_severity'].map(severity_colors)

        # Create the figure with hover text for each accident severity
        self.fig = go.Figure(go.Bar(
            x=grouped_data['count'],
            y=grouped_data[selected_attribute],
            orientation='h',
            text=grouped_data['percentage'],  # Display the overall percentage of the bar
            textposition='inside',
            hovertemplate=
            '<b>%{y}</b><br>' +
            'Percentage of Total Accidents: %{customdata}<extra></extra>',
            customdata=grouped_data['percentage'],  # Use custom data for hover template
            marker_color=grouped_data['color']  # Apply colors based on severity
        ))

        # Customize the layout
        self.fig.update_layout(
            xaxis_title='Number of Accidents',
            yaxis_title=selected_attribute.replace('_', ' ').title(),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            autosize=True,
            margin=dict(l=20, r=20, t=20, b=20),
            hovermode='closest'
        )
        return self.fig
