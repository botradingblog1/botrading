import pandas as pd
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from themes.light_theme import LightTheme


class SupportResistanceAgglomerativeClustering:
    """
    Class to calculate support and resistance levels using agglomerative clustering.
    """

    def __init__(self, rolling_wave_length=14, num_clusters=5):
        """
        Initializes the SupportResistanceAgglomerativeClustering with specified parameters.

        Parameters:
            rolling_wave_length (int): The window length for rolling max and min calculations. Defaults to 14.
            num_clusters (int): The number of clusters for agglomerative clustering. Defaults to 5.
        """
        self.rolling_wave_length = rolling_wave_length
        self.num_clusters = num_clusters

    def calculate_support_resistance(self, df):
        """
        Calculates the support and resistance levels.

        Parameters:
            df (pd.DataFrame): The OHLC dataframe.

        Returns:
            pd.Series: A series of support and resistance levels.
        """
        date = df.index

        # Reset index for merging
        df.reset_index(inplace=True)

        # Create min and max waves
        max_waves_temp = df.High.rolling(self.rolling_wave_length).max().rename('waves')
        min_waves_temp = df.Low.rolling(self.rolling_wave_length).min().rename('waves')

        max_waves = pd.concat([max_waves_temp, pd.Series(np.ones(len(max_waves_temp)))], axis=1)
        min_waves = pd.concat([min_waves_temp, pd.Series(np.ones(len(min_waves_temp)) * -1)], axis=1)

        # Remove duplicates
        max_waves.drop_duplicates('waves', inplace=True)
        min_waves.drop_duplicates('waves', inplace=True)

        # Merge max and min waves
        waves = pd.concat([max_waves, min_waves]).sort_index()
        waves = waves[waves[0] != waves[0].shift()].dropna()

        # Find Support/Resistance with clustering using the rolling stats
        x = np.concatenate((waves.waves.values.reshape(-1, 1), (np.zeros(len(waves)) + 1).reshape(-1, 1)), axis=1)

        # Initialize Agglomerative Clustering
        cluster = AgglomerativeClustering(n_clusters=self.num_clusters, affinity='euclidean', linkage='ward')
        cluster.fit_predict(x)
        waves['clusters'] = cluster.labels_

        # Get index of the max wave for each cluster
        waves2 = waves.loc[waves.groupby('clusters')['waves'].idxmax()]
        df.index = date

        waves2.waves.drop_duplicates(keep='first', inplace=True)

        return waves2.reset_index().waves

    def plot_chart(self, symbol, df, support_resistance_levels):
        """
        Plots the chart with support and resistance levels.

        Parameters:
            symbol (str): The stock symbol.
            df (pd.DataFrame): The OHLC dataframe.
            support_resistance_levels (pd.Series): The support and resistance levels.

        Returns:
            plotly.graph_objs._figure.Figure: The plotly figure with the chart.
        """
        light_palette = {
            "bg_color": "#ffffff",
            "plot_bg_color": "#ffffff",
            "grid_color": "#e6e6e6",
            "text_color": "#2e2e2e",
            "dark_candle": "#4d98c4",
            "light_candle": "#b1b7ba",
            "volume_color": "#c74e96",
            "border_color": "#2e2e2e",
            "color_1": "#5c285b",
            "color_2": "#802c62",
            "color_3": "#a33262",
            "color_4": "#c43d5c",
            "color_5": "#de4f51",
            "color_6": "#f26841",
            "color_7": "#fd862b",
            "color_8": "#ffa600",
            "color_9": "#3366d6"
        }
        palette = LightTheme.color_palette

        # Array of colors for support/resistance lines
        support_resistance_colors = [
            "#5c285b", "#802c62", "#a33262", "#c43d5c", "#de4f51",
            "#f26841", "#fd862b", "#ffa600", "#3366d6"
        ]

        # Create subplots
        fig = make_subplots(
            rows=1, cols=1, subplot_titles=[f"{symbol} Chart"],
            specs=[[{"secondary_y": False}]],
            vertical_spacing=0.04, shared_xaxes=True
        )

        # Add legend with the support/resistance prices
        support_resistance_prices = ""
        for level in support_resistance_levels.to_list():
            support_resistance_prices += "$ {:.2f}".format(level) + "<br>"

        fig.add_annotation(
            text=support_resistance_prices,
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=0.9,
            bordercolor='black',
            borderwidth=1
        )

        # Plot close price
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['Open'],
                close=df['Close'],
                low=df['Low'],
                high=df['High'],
                increasing_line_color=palette['light_candle'],
                decreasing_line_color=palette['dark_candle'],
                name='Price'
            ),
            row=1, col=1
        )

        # Add Support/Resistance levels
        for i, level in enumerate(support_resistance_levels.to_list()):
            line_color = support_resistance_colors[i] if i < len(support_resistance_colors) else support_resistance_colors[0]
            fig.add_hline(y=level, line_width=1, line_dash="dash", line_color=line_color, row=1, col=1)

        fig.update_layout(
            title={'text': '', 'x': 0.5},
            font=dict(family="Verdana", size=12, color=palette["text_color"]),
            autosize=True,
            width=1280, height=720,
            xaxis={"rangeslider": {"visible": False}},
            plot_bgcolor=palette["plot_bg_color"],
            paper_bgcolor=palette["bg_color"]
        )
        fig.update_yaxes(visible=False, secondary_y=True)
        fig.update_xaxes(showline=True, linewidth=1, linecolor=palette["grid_color"], gridcolor=palette["grid_color"])
        fig.update_yaxes(showline=True, linewidth=1, linecolor=palette["grid_color"], gridcolor=palette["grid_color"])

        return fig
