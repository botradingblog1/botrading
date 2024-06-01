import os
import requests
import pandas as pd
from ..utils.df_utils import standardize_ohlcv_dataframe


class FmpDataLoader:
    """
    FmpDataLoader provides methods to interact with the Financial Modeling Prep (FMP) API to fetch various financial data.

    Attributes:
        api_key (str): FMP API key.
    """

    def __init__(self, api_key: str):
        """
        Initializes the FmpDataLoader with the given API key.

        Parameters:
            api_key (str): FMP API key.
        """
        self._api_key = api_key

    def fetch_stock_screener_results(
        self,
        exchange_list=None,
        market_cap_more_than=None,
        market_cap_lower_than=None,
        price_more_than=None,
        price_lower_than=None,
        beta_more_than=None,
        beta_lower_than=None,
        volume_more_than=None,
        volume_lower_than=None,
        dividend_more_than=None,
        dividend_lower_than=None,
        is_etf=None,
        is_fund=None,
        is_actively_trading=None,
        sector=None,
        industry=None,
        country=None,
        exchange=None,
        limit=1000,
        cache_data=False,
        cache_dir="cache",
        file_name="eft_data.csv"
    ):
        """
        Fetches stock screener results from the FMP API.

        Parameters:
            exchange_list (str): List of exchanges.
            market_cap_more_than (int): Minimum market cap.
            market_cap_lower_than (int): Maximum market cap.
            price_more_than (float): Minimum stock price.
            price_lower_than (float): Maximum stock price.
            beta_more_than (float): Minimum beta.
            beta_lower_than (float): Maximum beta.
            volume_more_than (int): Minimum volume.
            volume_lower_than (int): Maximum volume.
            dividend_more_than (float): Minimum dividend yield.
            dividend_lower_than (float): Maximum dividend yield.
            is_etf (bool): Filter for ETFs.
            is_fund (bool): Filter for funds.
            is_actively_trading (bool): Filter for actively trading stocks.
            sector (str): Sector filter.
            industry (str): Industry filter.
            country (str): Country filter.
            exchange (str): Exchange filter.
            limit (int): Maximum number of results.
            cache_data (bool): Cache data locally?
            cache_dir (str): cache directory
            file_name (str): cache file name

        Returns:
            pd.DataFrame: DataFrame with stock screener results.
        """
        try:
            path = os.path.join(cache_dir, file_name)

            # Try to load from cache
            if cache_data and os.path.exists(path):
                securities_df = pd.read_csv(path)
                return securities_df

            # Load data remotely
            url = "https://financialmodelingprep.com/api/v3/stock-screener?"
            params = {
                "exchange": exchange_list,
                "limit": limit,
                "marketCapMoreThan": market_cap_more_than,
                "marketCapLowerThan": market_cap_lower_than,
                "priceMoreThan": price_more_than,
                "priceLowerThan": price_lower_than,
                "betaMoreThan": beta_more_than,
                "betaLowerThan": beta_lower_than,
                "volumeMoreThan": volume_more_than,
                "volumeLowerThan": volume_lower_than,
                "dividendMoreThan": dividend_more_than,
                "dividendLowerThan": dividend_lower_than,
                "isEtf": is_etf,
                "isFund": is_fund,
                "isActivelyTrading": is_actively_trading,
                "sector": sector,
                "industry": industry,
                "country": country,
                "exchange": exchange,
                "apikey": self._api_key
            }

            # Filter out parameters that are None
            params = {k: v for k, v in params.items() if v is not None}

            response = requests.get(url, params=params)

            if response.status_code == 200:
                securities_data = response.json()
                if securities_data:
                    securities_df = pd.DataFrame(securities_data)

                    # Cache locally if requested
                    if cache_data:
                        os.makedirs(cache_dir, exist_ok=True)
                        securities_df.to_csv(path, index=False)

                    return securities_df
                return None
            else:
                return None
        except Exception as ex:
            print(ex)
            return None

    def fetch_dividend_calendar(self, start_date_str: str, end_date_str: str) -> pd.DataFrame:
        """
        Fetches the dividend calendar from the FMP API.

        Parameters:
            start_date_str (str): Start date in 'YYYY-MM-DD' format.
            end_date_str (str): End date in 'YYYY-MM-DD' format.

        Returns:
            pd.DataFrame: DataFrame with dividend calendar data.
        """
        try:
            url = f"https://financialmodelingprep.com/api/v3/stock_dividend_calendar?from={start_date_str}&to={end_date_str}&apikey={self._api_key}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if data:
                    dividend_calendar_df = pd.DataFrame(data)
                    return dividend_calendar_df
                return None
            else:
                return None
        except Exception as ex:
            print(ex)
            return None

    def fetch_daily_prices_by_date(self, symbol: str, start_date_str: str, end_date_str: str,
                                   cache_data: bool = False, cache_dir: str = "cache") -> pd.DataFrame:
        """
        Fetches daily prices by date from the FMP API.

        Parameters:
            symbol (str): Stock symbol.
            start_date_str (str): Start date in 'YYYY-MM-DD' format.
            end_date_str (str): End date in 'YYYY-MM-DD' format.
            cache_data (bool): Flag to specify if data should be cached
            cache_dir (str): Directory to cache the data.

        Returns:
            pd.DataFrame: DataFrame with daily prices.
        """

        file_name = f"{symbol}-{start_date_str}-{end_date_str}-prices.csv"
        path = os.path.join(cache_dir, file_name)
        if cache_data is True:
            if os.path.exists(path) is True:
                prices_df = pd.read_csv(path)
                prices_df['date'] = pd.to_datetime(prices_df['date'])
                prices_df.set_index('date', inplace=True)
                return prices_df

        try:
            url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={start_date_str}&to={end_date_str}&apikey={self._api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                historical_data = data.get('historical', [])
                if historical_data:
                    prices_df = pd.DataFrame(historical_data)
                    prices_df = standardize_ohlcv_dataframe(prices_df)
                    prices_df['date'] = pd.to_datetime(prices_df['date'])
                    prices_df.set_index('date', inplace=True)
                    prices_df.sort_values(by=['date'], ascending=True, inplace=True)

                    if cache_data is True:
                        os.makedirs(cache_dir, exist_ok=True)
                        prices_df.to_csv(path)
                    return prices_df
                else:
                    return None
            else:
                print(f"Failed to fetch prices. Error: {response.reason}")
                return None
        except Exception as ex:
            print(ex)
            return None

    def fetch_multiple_daily_prices_by_date(self, symbol_list: list, start_date_str: str, end_date_str: str, cache_data: bool = False, cache_dir: str = "cache") -> dict:
        """
        Fetches daily prices by date for multiple symbols from the FMP API.

        Parameters:
            symbol_list (list): List of stock symbols.
            start_date_str (str): Start date in 'YYYY-MM-DD' format.
            end_date_str (str): End date in 'YYYY-MM-DD' format.
            cache_data (bool): Flag to specify if data should be cached
            cache_dir (str): Directory to cache the data.

        Returns:
            dict: A dictionary with symbols as keys and DataFrames with daily prices as values.
        """
        results = {}
        for symbol in symbol_list:
            print(f"Now fetching price data for {symbol}...")
            df = self.fetch_daily_prices_by_date(symbol, start_date_str, end_date_str, cache_data, cache_dir)
            if df is not None:
                results[symbol] = df
            else:
                print(f"Failed to fetch data for {symbol}")
        return results

    def fetch_dividends(self, symbol: str) -> pd.DataFrame:
        """
        Fetches historical dividends for a stock from the FMP API.

        Parameters:
            symbol (str): Stock symbol.

        Returns:
            pd.DataFrame: DataFrame with historical dividends data.
        """
        try:
            url = f"https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{symbol}?apikey={self._api_key}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                historical_data = data.get('historical', [])
                if historical_data:
                    dividends_df = pd.DataFrame(historical_data)
                    dividends_df['payment_date'] = pd.to_datetime(dividends_df['paymentDate'])
                    dividends_df['declaration_date'] = pd.to_datetime(dividends_df['declarationDate'])
                    dividends_df.set_index('payment_date', inplace=True)
                    return dividends_df
                else:
                    return None
            else:
                return None
        except Exception as ex:
            print(ex)
            return None


