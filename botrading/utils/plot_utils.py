import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import matplotlib.ticker as mticker
from ..themes.dark_theme import DarkTheme
from ..themes.light_theme import LightTheme
import mplfinance as mpf
import os


def plot_candlestick_chart(df,
                           volume=False,
                           extra_cols=None,
                           extra_cols_in_main_chart=None,
                           title="Candlestick Chart",
                           fig_size=(10, 6),
                           dpi=300,
                           path=None,
                           file_name=None,
                           theme_class=LightTheme):
    """
    Plots a candlestick chart with optional additional columns and themes.

    Parameters:
    df (pd.DataFrame): DataFrame with columns 'Open', 'High', 'Low', 'Close', and optionally 'Volume'.
    volume (bool): Flag to add a volume histogram. Default is False.
    extra_cols (list of str, optional): List of additional columns to chart.
    extra_cols_in_main_chart (list of bool, optional): List of booleans specifying if the extra columns should be plotted in the main chart.
    title (str): Title of the chart
    fig_size (tuple, optional): Size of the plot. Default is (10, 6).
    show (bool, optional): Whether to display the plot. Default is True.
    dpi (int, optional): DPI for the saved figure. Default is 300.
    path (str, optional): Path to save the chart. Default is None.
    file_name (str, optional): File name to save the chart. Default is None.
    theme_class (class, optional): Theme class with color palette. Default is LightTheme.

    Returns:
    None
    """
    color_palette = theme_class.color_palette

    # Setup market colors
    mc = mpf.make_marketcolors(
        up=color_palette['dark_candle'],
        down=color_palette['light_candle'],
        edge={'up': color_palette['dark_candle'], 'down': color_palette['light_candle']},
        volume=color_palette['volume_color']
    )

    # Setup style
    s = mpf.make_mpf_style(
        marketcolors=mc,
        facecolor=color_palette['plot_bg_color'],
        gridcolor=color_palette['grid_color'],
        gridstyle='-',
        rc={'axes.edgecolor': color_palette['border_color'],
            'axes.labelcolor': color_palette['text_color'],
            'xtick.color': color_palette['text_color'],
            'ytick.color': color_palette['text_color']}
    )

    # Additional plots
    add_plots = []
    if extra_cols and extra_cols_in_main_chart:
        for col, in_main in zip(extra_cols, extra_cols_in_main_chart):
            if in_main:
                add_plots.append(mpf.make_addplot(df[col], color=color_palette['color_1']))
            else:
                add_plots.append(mpf.make_addplot(df[col], panel=1, color=color_palette['color_1']))

    save_path = None
    if path and file_name:
        os.makedirs(path, exist_ok=True)
        save_path = os.path.join(path, file_name)

    # Plot the candlestick chart
    mpf.plot(df,
             title=title,
             type='candle',
             volume=volume,
             addplot=add_plots,
             style=s,
             figsize=fig_size,
             savefig=dict(fname=save_path, dpi=dpi, facecolor=color_palette['bg_color']) if save_path else None)


def plot_line_chart(df,
                    column_list=['close'],
                    new_chart_column_list=None,
                    title="Line Chart",
                    fig_size=(10, 12),
                    dpi=300,
                    path=None,
                    file_name=None,
                    theme_class=LightTheme):
    """
    Plots a line chart for specified columns using a given theme. Adds additional lines in separate sub charts for specified columns.

    Parameters:
    df (pd.DataFrame): DataFrame containing the data to be plotted.
    column_list (list of str): List of columns to plot in the main chart. Default is ['close'].
    new_chart_column_list (list of str, optional): List of columns to plot in separate sub charts below the main chart. Default is None.
    title (str): Title of the chart.
    fig_size (tuple, optional): Size of the plot. Default is (10, 12).
    dpi (int, optional): DPI for the saved figure. Default is 300.
    path (str, optional): Path to save the chart. Default is None.
    file_name (str, optional): File name to save the chart. Default is None.
    theme_class (class, optional): Theme class with color palette. Default is LightTheme.

    Returns:
    None
    """
    color_palette = theme_class.color_palette
    colors = [color_palette[f'color_{i + 1}'] for i in range(len(column_list))]
    if new_chart_column_list:
        new_chart_colors = [color_palette[f'color_{i + 1 + len(column_list)}'] for i in range(len(new_chart_column_list))]
    else:
        new_chart_colors = []

    num_sub_charts = len(new_chart_column_list) if new_chart_column_list else 0
    fig, axes = plt.subplots(num_sub_charts + 1, 1, figsize=fig_size, dpi=dpi, gridspec_kw={'height_ratios': [3] + [1] * num_sub_charts})
    plt.style.use('seaborn-whitegrid')
    plt.rcParams.update({
        'axes.facecolor': color_palette['plot_bg_color'],
        'axes.edgecolor': color_palette['border_color'],
        'axes.labelcolor': color_palette['text_color'],
        'xtick.color': color_palette['text_color'],
        'ytick.color': color_palette['text_color'],
        'grid.color': color_palette['grid_color'],
        'figure.facecolor': color_palette['bg_color'],
        'text.color': color_palette['text_color']
    })

    if num_sub_charts > 0:
        axes = axes.flatten()
    else:
        axes = [axes]

    # Plotting main chart columns
    ax1 = axes[0]
    for idx, column in enumerate(column_list):
        if column in df.columns:
            ax1.plot(df.index, df[column], label=column, color=colors[idx % len(colors)])

    ax1.legend()
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Value')
    ax1.set_title(title)

    # Plotting sub charts
    if new_chart_column_list:
        for i, column in enumerate(new_chart_column_list):
            if column in df.columns:
                ax = axes[i + 1]
                ax.plot(df.index, df[column], label=column, color=new_chart_colors[i % len(new_chart_colors)])
                ax.legend()
                ax.set_xlabel('Date')
                ax.set_ylabel('Value')
                ax.set_title(f'{column} chart')

    plt.tight_layout()

    if path and file_name:
        os.makedirs(path, exist_ok=True)
        plt.savefig(os.path.join(path, file_name), bbox_inches='tight', dpi=dpi)