import numpy as np
import pandas as pd
import requests
import io
from datetime import datetime
from ..enums import EconomicIndicators


class FredDataLoader:
    """
    Fetches data using FRED Data API
    """

    def __init__(self):
        """
        Initializes the FredDataLoader with necessary configurations.
        """
        self._name = "FredDataLoader"

    def fetch_fred_data(self, code_list, start_date_str, end_date_str):
        """
        Fetches data from FRED for the given list of codes within the specified date range.

        Parameters:
            code_list (list): List of FRED data series codes.
            start_date_str (str): Start date in 'YYYY-MM-DD' format.
            end_date_str (str): End date in 'YYYY-MM-DD' format.

        Returns:
            pd.DataFrame: DataFrame with fetched data.
        """
        try:
            base_url = "https://fred.stlouisfed.org/graph/fredgraph.csv"
            dfs = []

            for code in code_list:
                params = {
                    "id": code,
                    "cosd": start_date_str,
                    "coed": end_date_str
                }
                response = requests.get(base_url, params=params)
                response.raise_for_status()
                df_temp = pd.read_csv(io.StringIO(response.text))
                df_temp = df_temp.rename(columns={"DATE": "date", code: code})
                dfs.append(df_temp)

            df = dfs[0]
            for temp_df in dfs[1:]:
                df = pd.merge(df, temp_df, on="date", how="outer")

            df['date'] = pd.to_datetime(df['date'])
            df['date'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df.dropna(inplace=True)
            return df

        except Exception as ex:
            print(f"Failed in {self._name}.fetch_fred_data(): {ex}")
            return None

    def translate_symbol_to_name(self, symbol):
        """
        Translates a FRED data series code to its human-readable name.

        Parameters:
            symbol (str): FRED data series code.

        Returns:
            str: Human-readable name of the data series.
        """
        mapping = {
            'GDPC1': 'Gross Domestic Product',
            'PAYEMS': 'Non-Farm Payroll',
            'UNRATE': 'Unemployment Rate',
            'CSCICP03USM665S': 'Consumer Confidence Index',
            'CPIAUCSL': 'Consumer Price Index',
            'MRTSSM44X72USS': 'Retail and Food Sales',
            'PPIACO': 'Producer Price Index',
            'INDPRO': 'Industrial Production Index',
            'DGS2': '2-Year Treasury Yield',
            'DGS10': '10-Year Treasury Yield',
            'VIXCLS': 'VIX',
            'SP500': 'S&P 500',
            'UMCSENT': 'University of Michigan Consumer Sentiment',
            'USARECM': 'US Recession Probabilities',
            'NFCI': 'Chicago Fed National Financial Conditions Index',
            'BAMLHYH0A0HYM2TRIV': 'ICE BofA High Yield Index',
            'STLFSI4': 'St. Louis Fed Financial Stress Index',
            'T10YIE': '10-Year Breakeven Inflation Rate'
        }
        return mapping.get(symbol, '')

    def calculate_deltas(self, df):
        """
        Calculates percentage changes over specified time periods.

        Parameters:
            df (pd.DataFrame): DataFrame with economic data.

        Returns:
            pd.DataFrame: DataFrame with calculated deltas.
        """
        time_periods = [1, 2, 3, 6, 9, 12]
        column_names = ['delta_1m', 'delta_2m', 'delta_3m', 'delta_6m', 'delta_9m', 'delta_12m']

        combined_deltas_df = pd.DataFrame()
        symbols = df['symbol'].unique()
        for symbol in symbols:
            symbol_df = df[df['symbol'] == symbol]
            deltas_df = pd.DataFrame()
            deltas_df['date'] = symbol_df['date']
            deltas_df['symbol'] = symbol
            deltas_df['name'] = self.translate_symbol_to_name(symbol)
            deltas_df['value'] = symbol_df['value']

            for i, period in enumerate(time_periods):
                pct_change_value = (symbol_df['value'] / symbol_df['value'].shift(period)) - 1
                deltas_df[column_names[i]] = pct_change_value

            combined_deltas_df = pd.concat([combined_deltas_df, deltas_df], axis=0, ignore_index=True)

        combined_deltas_df.replace([np.inf, -np.inf], np.nan, inplace=True)
        combined_deltas_df.dropna(inplace=True)

        return combined_deltas_df

    def fetch_economic_indicators(self, start_date_str: str, end_date_str: str) -> pd.DataFrame:
        """
        Fetches economic indicators data from FRED within the specified date range.

        Parameters:
            start_date_str (str): Start date in 'YYYY-MM-DD' format.
            end_date_str (str): End date in 'YYYY-MM-DD' format.

        Returns:
            pd.DataFrame: DataFrame with economic indicators data.
        """
        fred_codes = [indicator.value for indicator in EconomicIndicators]
        temp_data_df = self.fetch_fred_data(fred_codes, start_date_str, end_date_str)
        if temp_data_df is not None:
            data_df = pd.DataFrame()
            for index, row in temp_data_df.iterrows():
                for code in fred_codes:
                    if code in row:
                        ind_row = pd.DataFrame({'date': [row['date']],
                                                'symbol': [code],
                                                'name': [self.translate_symbol_to_name(code)],
                                                'value': [row[code]]})
                        data_df = pd.concat([data_df, ind_row], axis=0, ignore_index=True)

            data_df['value'] = data_df['value'].replace(".", "0.0")
            data_df['value'] = data_df['value'].astype(float)
            data_df = data_df.replace(0, np.nan).ffill()

            return data_df
        return None

    def fetch_economic_indicator_deltas(self, start_date_str: str, end_date_str: str) -> pd.DataFrame:
        """
        Fetches economic indicators data from FRED and calculates deltas within the specified date range.

        Parameters:
            start_date_str (str): Start date in 'YYYY-MM-DD' format.
            end_date_str (str): End date in 'YYYY-MM-DD' format.

        Returns:
            pd.DataFrame: DataFrame with economic indicators deltas.
        """
        data_df = self.fetch_economic_indicators(start_date_str, end_date_str)
        if data_df is not None:
            deltas_df = self.calculate_deltas(data_df)
            return deltas_df
        return None
