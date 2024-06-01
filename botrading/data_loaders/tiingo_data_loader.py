import os
import requests
import pandas as pd
from datetime import datetime
from ..enums import TiingoDailyInterval, TiingoIntradayInterval, DataType
from typing import List


class TiingoDataLoader:
    """
    TiingoDataLoader provides methods to interact with Tiingo APIs to fetch data such as stock prices, crypto prices, news, and forex data.

    Attributes:
        api_key (str): Tiingo API key.
    """

    def __init__(self, api_key: str):
        """
        Initializes the TiingoDataLoader with the given API key.

        Parameters:
            api_key (str): Tiingo API key.
        """
        self.api_key = api_key

    def fetch_intraday_prices(self, symbol: str, start_date_str: str, end_date_str: str, interval: TiingoIntradayInterval, cache_data=False, cache_dir="cache") -> pd.DataFrame:
        """
        Fetches stock prices from Tiingo API.

        Parameters:
            symbol (str): Stock symbol.
            start_date (str): Start date in 'YYYY-MM-DD' format.
            end_date (str): End date in 'YYYY-MM-DD' format.
            interval (TiingoIntradayInterval): Data interval.
            cache_data (bool): Whether to cache the data.
            cache_dir (str): Directory to save the cached data.

        Returns:
            pd.DataFrame: DataFrame with stock prices.
        """
        try:
            file_name = f"{symbol}_{interval.value}_{start_date_str}_{end_date_str}.csv"
            path = os.path.join(cache_dir, file_name)

            if cache_data and os.path.exists(path):
                prices_df = pd.read_csv(path, parse_dates=['date'])
                prices_df.set_index('date', inplace=True)
                prices_df.index.name = 'date'
                return prices_df
            else:
                fetch_url = f"https://api.tiingo.com/iex/{symbol}/prices?startDate={start_date_str}&endDate={end_date_str}&resampleFreq={interval.value}&columns=date,open,high,low,close,volume&token={self.api_key}"
                headers = {'Accept': 'application/json'}

                response = requests.get(fetch_url, headers=headers)
                response.raise_for_status()  # Raise an error for bad status codes

                data = response.json()

                if not data:
                    print("No data returned from Tiingo API.")
                    return None

                prices_df = pd.DataFrame()
                for row in data:
                    row_df = pd.DataFrame({
                        'date': [row['date']],
                        'open': [row['open']],
                        'high': [row['high']],
                        'low': [row['low']],
                        'close': [row['close']],
                        'volume': [row['volume']]
                    })
                    prices_df = pd.concat([prices_df, row_df], axis=0, ignore_index=True)

                prices_df['date'] = pd.to_datetime(prices_df['date'])

                if cache_data:
                    os.makedirs(cache_dir, exist_ok=True)
                    prices_df.to_csv(path, index=False)

                prices_df.set_index('date', inplace=True)
                prices_df.index.name = 'date'

                return prices_df
        except Exception as ex:
            print(f"Failed to fetch Tiingo prices: {ex}")
            return None

    def fetch_multiple_intraday_prices(self, symbol_list: List[str], start_date_str: str, end_date_str: str, interval: TiingoIntradayInterval, cache_data=False, cache_dir="cache") -> pd.DataFrame:
        prices_dict = {}
        for symbol in symbol_list:
            print(f"Fetching prices for {symbol}")
            # fetch prices
            prices_df = self.fetch_intraday_prices(symbol, start_date_str, end_date_str,
                                                                 interval, cache_data=cache_data,
                                                                 cache_dir=cache_dir)
            prices_dict[symbol] = prices_df
        return prices_dict

    def fetch_end_of_day_prices(self, symbol: str, start_date: str, end_date: str, interval: TiingoDailyInterval, cache_data = False, cache_dir: str = "cache") -> pd.DataFrame:
        """
        Fetches daily stock prices from Tiingo API.

        Parameters:
            symbol (str): Stock symbol.
            interval (TiingoDailyInterval): Data interval.
            start_date (str): Start date in 'YYYY-MM-DD' format.
            end_date (str): End date in 'YYYY-MM-DD' format.
            data_dir (str): Directory to save the data.

        Returns:
            pd.DataFrame: DataFrame with stock prices.
        """
        try:
            file_name = f"{symbol}_{interval.value}_{start_date}_{end_date}.csv"
            path = os.path.join(cache_dir, file_name)

            if cache_data is True and os.path.exists(path):
                prices_df = pd.read_csv(path, parse_dates=['date'])
                if 'date' in prices_df.columns:
                    prices_df.set_index('date', inplace=True)
                    prices_df.index.name = 'date'
                return prices_df
            else:
                fetch_url = f"https://api.tiingo.com/tiingo/daily/{symbol}/prices?startDate={start_date}&endDate={end_date}&resampleFreq={interval.value}&columns=date,open,high,low,close,volume&token={self.api_key}"
                headers = {'Accept': 'application/json'}

                response = requests.get(fetch_url, headers=headers)
                data = response.json()

                prices_df = pd.DataFrame()
                for row in data:
                    row_df = pd.DataFrame({
                        'date': [row['date']],
                        'open': [row['open']],
                        'high': [row['high']],
                        'low': [row['low']],
                        'close': [row['close']],
                        'volume': [row['volume']],
                        'adj_close': [row.get('adjClose')]
                    })
                    prices_df = pd.concat([prices_df, row_df], axis=0, ignore_index=True)


                if cache_data is True:
                    os.makedirs(cache_dir, exist_ok=True)
                    prices_df.to_csv(path, index=False)

                prices_df.set_index('date', inplace=True)
                prices_df.index.name = 'date'

                return prices_df
        except Exception as ex:
            print(f"Failed to fetch Tiingo prices: {ex}")
            return None

    def fetch_multiple_end_of_day_prices(self, symbol_list: List[str], start_date_str: str, end_date_str: str, interval=TiingoDailyInterval.DAILY, cache_data=False, cache_dir="cache") -> pd.DataFrame:
        """
         Fetches daily prices for multiple symbols.

         Parameters:
         symbol_list (List[str]): List of stock symbols.
         start_date_str (str): Start date in 'YYYY-MM-DD' format.
         end_date_str (str): End date in 'YYYY-MM-DD' format.
         interval (TiingoDailyInterval): The interval, e.g. daily, weekly, monthly
         cache_data (bool): Flag to specify if data should be cached. Default is False.
         cache_dir (str): Directory to cache the data. Default is "cache".

         Returns:
         pd.DataFrame: DataFrame containing the daily prices for multiple symbols.
         """
        prices_dict = {}
        for symbol in symbol_list:
            print(f"Fetching prices for {symbol}")
            # fetch prices
            prices_df = self.fetch_end_of_day_prices(symbol, start_date_str, end_date_str, interval, cache_data=cache_data, cache_dir=cache_dir)
            prices_dict[symbol] = prices_df
        return prices_dict
