import os
import requests
import pandas as pd
from datetime import datetime
from ..enums import TiingoDailyInterval, TiingoIntradayInterval, DataType


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

    def fetch_tiingo_intraday_prices(self, symbol: str, start_date: str, end_date: str, interval: TiingoIntradayInterval, cache_data=False, cache_dir="cache") -> pd.DataFrame:
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
            file_name = f"{symbol}_{interval.value}_{start_date}_{end_date}.csv"
            path = os.path.join(cache_dir, file_name)

            if cache_data and os.path.exists(path):
                prices_df = pd.read_csv(path, parse_dates=['date'])
                return prices_df
            else:
                fetch_url = f"https://api.tiingo.com/iex/{symbol}/prices?startDate={start_date}&endDate={end_date}&resampleFreq={interval.value}&columns=date,open,high,low,close,volume&token={self.api_key}"
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
                prices_df.reset_index(drop=True, inplace=True)

                if cache_data:
                    os.makedirs(cache_dir, exist_ok=True)
                    prices_df.to_csv(path, index=False)

                return prices_df
        except Exception as ex:
            print(f"Failed to fetch Tiingo prices: {ex}")
            return None

    def fetch_tiingo_daily_prices(self, symbol: str, start_date: str, end_date: str, interval: TiingoDailyInterval, cache_data = False, cache_dir: str = "cache") -> pd.DataFrame:
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

                prices_df.reset_index(drop=True, inplace=True)
                if cache_data is True:
                    os.makedirs(cache_dir, exist_ok=True)
                    prices_df.to_csv(path, index=False)

                return prices_df
        except Exception as ex:
            print(f"Failed to fetch Tiingo prices: {ex}")
            return None

    def fetch_tiingo_crypto_prices(self, symbol: str, start_date: str, end_date: str, data_dir: str = "data") -> pd.DataFrame:
        """
        Fetches crypto prices from Tiingo API.

        Parameters:
            symbol (str): Crypto symbol.
            start_date (str): Start date in 'YYYY-MM-DD' format.
            end_date (str): End date in 'YYYY-MM-DD' format.
            data_dir (str): Directory to save the data.

        Returns:
            pd.DataFrame: DataFrame with crypto prices.
        """
        try:
            print(f"Loading crypto prices for {symbol}")
            file_name = f"{symbol}_crypto_{start_date}_{end_date}.csv"
            path = os.path.join(data_dir, file_name)

            if os.path.exists(path):
                prices_df = pd.read_csv(path, parse_dates=['date'])
                return prices_df
            else:
                fetch_url = f"https://api.tiingo.com/tiingo/crypto/prices?tickers={symbol}&startDate={start_date}&endDate={end_date}&token={self.api_key}"
                headers = {'Accept': 'application/json'}

                response = requests.get(fetch_url, headers=headers)
                data = response.json()

                prices_df = pd.DataFrame()
                for row in data[0]['priceData']:
                    row_df = pd.DataFrame({
                        'date': [row['date']],
                        'open': [row['open']],
                        'high': [row['high']],
                        'low': [row['low']],
                        'close': [row['close']],
                        'volume': [row['volume']]
                    })
                    prices_df = pd.concat([prices_df, row_df], axis=0, ignore_index=True)

                prices_df.reset_index(drop=True, inplace=True)
                os.makedirs(data_dir, exist_ok=True)
                prices_df.to_csv(path, index=False)

                return prices_df
        except Exception as ex:
            print(f"Failed to fetch Tiingo crypto prices: {ex}")
            return None

    # Additional methods for other Tiingo APIs like news and forex can be added here
