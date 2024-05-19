import os
import base64
import pandas as pd
from plotly.io import to_image
from ..themes.light_theme import LightTheme
from ..themes.dark_theme import DarkTheme


class HTMLReportGenerator:
    """
    Class to generate HTML reports with tables, images, text, and headings.
    """

    def __init__(self, title="HTML Report", theme=LightTheme):
        """
        Initializes the HTMLReportGenerator with a title and optional theme.

        Parameters:
            title (str): The title of the report. Defaults to "Report".
            theme (object): The theme for the report. Defaults to LightTheme.
        """
        self.title = title
        self.theme = theme.color_palette if theme else LightTheme.color_palette
        self.sections = []

    def add_heading(self, heading, level=1):
        """
        Adds a heading to the report.

        Parameters:
            heading (str): The heading text.
            level (int): The level of the heading (1-6). Defaults to 1.
        """
        self.sections.append(f"<h{level} style='color: {self.theme['text_color']};'>{heading}</h{level}>")

    def add_text(self, text):
        """
        Adds a text section to the report.

        Parameters:
            text (str): The text content.
        """
        self.sections.append(f"<p style='color: {self.theme['text_color']};'>{text}</p>")

    def add_table_from_dataframe(self, df, title=None):
        """
        Adds a table to the report.

        Parameters:
            df (pd.DataFrame): The dataframe to convert to an HTML table.
            title (str): Optional title for the table.
        """
        if title:
            self.sections.append(f"<h2 style='color: {self.theme['text_color']};'>{title}</h2>")
        self.sections.append(df.to_html(index=False, classes='table table-striped', border=0))

    def add_image_from_fig(self, fig, title=None):
        """
        Adds an image to the report.

        Parameters:
            fig (plotly.graph_objs._figure.Figure): The plotly figure to convert to an image.
            title (str): Optional title for the image.
        """
        img_bytes = to_image(fig, format="png")
        img_base64 = base64.b64encode(img_bytes).decode("utf8")
        if title:
            self.sections.append(f"<h2 style='color: {self.theme['text_color']};'>{title}</h2>")
        self.sections.append(f'<img src="data:image/png;base64,{img_base64}" style="max-width: 100%;">')

    def generate_report(self, filepath):
        """
        Generates the HTML report and saves it to a file.

        Parameters:
            filepath (str): The file path to save the report.
        """
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{self.title}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: {self.theme['bg_color']};
                    color: {self.theme['text_color']};
                }}
                .container {{
                    max-width: 800px;
                    margin: auto;
                    background-color: {self.theme['bg_color']};
                    padding: 20px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                .table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                    color: {self.theme['text_color']};
                }}
                .table th, .table td {{
                    border: 1px solid {self.theme['grid_color']};
                    padding: 8px;
                }}
                .table th {{
                    padding-top: 12px;
                    padding-bottom: 12px;
                    text-align: left;
                    background-color: {self.theme['color_1']};
                    color: {self.theme['text_color']};
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 style='color: {self.theme['text_color']};'>{self.title}</h1>
                {"".join(self.sections)}
            </div>
        </body>
        </html>
        """
        with open(filepath, 'w') as f:
            f.write(html_content)
