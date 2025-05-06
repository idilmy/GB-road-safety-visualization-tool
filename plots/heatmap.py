import pandas as pd
from dash import dcc, html
import plotly.graph_objects as go


class HeatMap(html.Div):
    """
    A class to create a heatmap component in our Dash app.

    """

    def __init__(self, html_id, data):
        """
        Initializes the HeatMap with the specified HTML ID and data.

        Parameters:
        - html_id: The ID for the HTML component.
        - data: The data to be used in the heatmap.
        """
        self.html_id = html_id
        self.data = data
        super().__init__(
            children=[
                dcc.Graph(id=self.html_id)  # Create a Graph component with the specified HTML ID
            ]
        )

    def update(self, data, corr1, corr2):
        """
        Updates the heatmap based on the provided data and selected correlation attributes.

        Parameters:
        - data: The data to be used for updating the heatmap.
        - corr1: The selected attribute for the x-axis.
        - corr2: The selected attribute for the y-axis.

        Returns:
        - A Plotly figure. (heatmap)
        """
        if corr1 is None:
            corr1 = 'junction_location'
        if corr2 is None:
            corr2 = 'junction_control'

        # Calculate the frequency of accidents for the heatmap
        heatmap_data = data.groupby([corr1, corr2]).size().reset_index(name='number_of_casualties')

        # Create a complete matrix of all possible combinations of corr1 and corr2
        unique_corr1 = data[corr1].unique()
        unique_corr2 = data[corr2].unique()
        complete_index = pd.MultiIndex.from_product([unique_corr1, unique_corr2], names=[corr1, corr2])

        # Reindex the heatmap_data to fill missing values with zeroes
        heatmap_data = heatmap_data.set_index([corr1, corr2]).reindex(complete_index, fill_value=0).reset_index()

        # Create the heatmap figure
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data['number_of_casualties'],
            x=heatmap_data[corr1],
            y=heatmap_data[corr2],
            text=heatmap_data['number_of_casualties'],
            texttemplate="%{text}",
            textfont={"size": 10},
            colorscale='Viridis',
            colorbar=dict(title='Accident Count')
        ))

        # Customize the layout
        fig.update_layout(
            xaxis_title=corr1,
            yaxis_title=corr2,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(
                family="Helvetica Neue, sans-serif",
                size=12,
                color="#383838",
            ),
        )

        return fig
