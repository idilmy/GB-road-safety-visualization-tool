from dash import dcc, html
import plotly.graph_objects as go
import pandas as pd


class LineChart(html.Div):
    """
    A class to create a line chart component in our Dash app.
    """

    def __init__(self, html_id, data):
        """
        Initializes the LineChart with the specified HTML ID and data.

        Parameters:
        - html_id: The ID for the HTML component.
        - data: The data to be used in the line chart.
        """
        self.html_id = html_id
        self.data = data
        super().__init__(
            children=[
                dcc.Graph(id=self.html_id)  # Create a Graph component with the specified HTML ID
            ]
        )

    def update(self, data, x_attr=None):
        """
        Updates the line chart based on the provided data and selected x-axis attribute.

        Parameters:
        - data: The data to be used for updating the line chart.
        - x_attr: The selected attribute for the x-axis (default is 'time').

        Returns:
        - A Plotly figure object. (line chart)
        """
        if x_attr is None:
            x_attr = 'time'  # Default x-axis attribute
        if x_attr == 'time':
            # Ensure datetime format for plotting
            data[x_attr] = pd.to_datetime(data[x_attr], dayfirst=True)
            data['hour'] = data[x_attr].dt.strftime('%H:00')
            x_attr = 'hour'  # Change the x_attr to 'hour' for plotting
        elif x_attr == 'age_band_of_driver':
            # Define the categorical order for age_band_of_driver
            age_band_order = [
                '0 - 5', '6 - 10', '11 - 15', '16 - 20', '21 - 25',
                '26 - 35', '36 - 45', '46 - 55', '56 - 65', '66 - 75', 'Over 75'
            ]
            data[x_attr] = pd.Categorical(data[x_attr], categories=age_band_order, ordered=True)
        elif x_attr == 'month':
            # Define the categorical order for months
            month_order = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                           'October', 'November', 'December')
            data[x_attr] = pd.Categorical(data[x_attr], categories=month_order, ordered=True)

        # Define color map for accident severity
        severity_colors = {
            'Fatal': 'red',
            'Serious': 'orange',
            'Slight': 'blue'
        }

        # Set the title based on x_attr
        title = x_attr.replace('_', ' ').title()
        if x_attr == 'hour':
            title = 'Time'
        elif x_attr == 'day_of_week':
            title = 'Day of Week'
        elif x_attr == 'month':
            title = 'Month'
        elif x_attr == 'age_band_of_driver':
            title = 'Age Band of Driver'
        elif x_attr == 'speed_limit':
            title = 'Speed Limit'

        # Initialize an empty figure
        self.fig = go.Figure()

        # Plot each severity level separately
        for severity in data['accident_severity'].unique():
            filtered_data = data[data['accident_severity'] == severity]

            if x_attr == 'hour':
                # Group by hour for datetime data
                grouped_data = filtered_data.groupby(x_attr)['number_of_casualties'].sum().reset_index()
                x_values = grouped_data[x_attr]
            else:
                # Group by x_attr for non-datetime data
                grouped_data = filtered_data.groupby(x_attr)['number_of_casualties'].sum().reset_index()
                x_values = grouped_data[x_attr]

            # Add trace to the figure
            self.fig.add_trace(
                go.Scatter(
                    x=x_values,
                    y=grouped_data['number_of_casualties'],
                    mode='lines',
                    name=f'{severity} Accidents',
                    line=dict(color=severity_colors[severity]),
                    hovertemplate=
                    f'<b>{severity} Accidents</b><br>' +
                    f'{title}: %{{x}}<br>' +
                    'Total Casualties: %{y}<extra></extra>'
                )
            )

        # Customize the layout
        self.fig.update_layout(
            xaxis=dict(
                title='Hour of the Day' if x_attr == 'hour' else x_attr.replace('_', ' ').title(),
                tickmode='linear' if x_attr == 'hour' else 'auto',
                dtick=1 if x_attr == 'hour' else None,
                tickformat='%H:00' if x_attr == 'hour' else None,
                tickvals=[f'{i:02}:00' for i in range(24)] if x_attr == 'hour' else None,
            ),
            yaxis_title='Total Casualties',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title=f'Total Casualties Over {title} by Severity'
        )

        return self.fig
