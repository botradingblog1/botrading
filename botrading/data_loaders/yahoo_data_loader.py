import os
import yfinance as yf
import pandas as pd
from ..enums import YahooInterval, YahooPeriod


class YahooDataLoader:
    """
    YahooDataLoader provides methods to fetch financial data from Yahoo Finance using yfinance library.
    """

    def __init__(self, cache_dir: str = "cache"):
        """
        Initializes the YahooDataLoader with the specified cache directory.

        Parameters:
            cache_dir (str): Directory to cache the data.
        """
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def fetch_yahoo_prices(self, symbol: str, interval: YahooInterval, start_date_str: str, end_date_str: str) -> pd.DataFrame:
        """
        Fetches historical stock data from Yahoo Finance.

        Parameters:
            symbol (str): Stock symbol.
            interval (Interval): Data interval.
            start_date_str (str): Start date in 'YYYY-MM-DD' format.
            end_date_str (str): End date in 'YYYY-MM-DD' format.

        Returns:
            pd.DataFrame: DataFrame with historical stock data.
        """
        try:
            file_name = f"{symbol}-{interval.value}-{start_date_str}-{end_date_str}-prices.csv"
            path = os.path.join(self.cache_dir, file_name)

            if os.path.exists(path):
                prices_df = pd.read_csv(path)
                prices_df['date'] = pd.to_datetime(prices_df['date'])
                return prices_df
            else:
                data = yf.download(tickers=symbol, start=start_date_str, end=end_date_str, interval=interval.value)
                prices_df = pd.DataFrame(data)
                prices_df.reset_index(inplace=True)
                prices_df.rename(columns=lambda x: x.lower().replace(' ', '_'), inplace=True)
                prices_df['date'] = pd.to_datetime(prices_df['date'])
                prices_df.to_csv(path, index=False)
                return prices_df
        except Exception as ex:
            print(f"Failed to fetch Yahoo data: {ex}")
            return None

    def fetch_yahoo_prices_by_period(self, symbol: str, period: YahooPeriod, interval: YahooInterval) -> pd.DataFrame:
        """
        Fetches historical stock data from Yahoo Finance using period.

        Parameters:
            symbol (str): Stock symbol.
            period (YahooPeriod): Data period.
            interval (YahooInterval): Data interval.

        Returns:
            pd.DataFrame: DataFrame with historical stock data.
        """
        try:
            file_name = f"{symbol}-{period.value}-{interval.value}-prices.csv"
            path = os.path.join(self.cache_dir, file_name)

            if os.path.exists(path):
                prices_df = pd.read_csv(path)
                prices_df['date'] = pd.to_datetime(prices_df['date'])
                return prices_df
            else:
                data = yf.download(tickers=symbol, period=period.value, interval=interval.value)
                prices_df = pd.DataFrame(data)
                prices_df.reset_index(inplace=True)
                prices_df.rename(columns=lambda x: x.lower().replace(' ', '_'), inplace=True)
                prices_df['date'] = pd.to_datetime(prices_df['date'])
                prices_df.to_csv(path, index=False)
                return prices_df
        except Exception as ex:
            print(f"Failed to fetch Yahoo data with period: {ex}")
            return None

    def fetch_dividends(self, symbol: str) -> pd.DataFrame:
        """
        Fetches historical dividend data for a stock from Yahoo Finance.

        Parameters:
            symbol (str): Stock symbol.

        Returns:
            pd.DataFrame: DataFrame with historical dividend data.
        """
        try:
            stock = yf.Ticker(symbol)
            dividends_df = stock.dividends.reset_index()
            dividends_df.rename(columns=lambda x: x.lower().replace(' ', '_'), inplace=True)
            return dividends_df
        except Exception as ex:
            loge(f"Failed to fetch Yahoo dividends data: {ex}")
            return None

    def fetch_stock_info(self, symbol: str) -> dict:
        """
        Fetches stock information from Yahoo Finance.

        Parameters:
            symbol (str): Stock symbol.

        Returns:
            dict: Dictionary with stock information.
        """
        try:
            stock = yf.Ticker(symbol)
            stock_info = stock.info
            return stock_info
        except Exception as ex:
            loge(f"Failed to fetch Yahoo stock info: {ex}")
            return None

    def fetch_financials(self, symbol: str) -> pd.DataFrame:
        """
        Fetches financial statements data for a stock from Yahoo Finance.

        Parameters:
            symbol (str): Stock symbol.

        Returns:
            pd.DataFrame: DataFrame with financial statements data.
        """
        try:
            stock = yf.Ticker(symbol)
            financials_df = stock.financials.T.reset_index()
            financials_df.rename(columns=lambda x: x.lower().replace(' ', '_'), inplace=True)
            return financials_df
        except Exception as ex:
            loge(f"Failed to fetch Yahoo financials data: {ex}")
            return None

    def fetch_earnings(self, symbol: str) -> pd.DataFrame:
        """
        Fetches earnings data for a stock from Yahoo Finance.

        Parameters:
            symbol (str): Stock symbol.

        Returns:
            pd.DataFrame: DataFrame with earnings data.
        """
        try:
            stock = yf.Ticker(symbol)
            earnings_df = stock.earnings.reset_index()
            earnings_df.rename(columns=lambda x: x.lower().replace(' ', '_'), inplace=True)
            return earnings_df
        except Exception as ex:
            loge(f"Failed to fetch Yahoo earnings data: {ex}")
            return None
