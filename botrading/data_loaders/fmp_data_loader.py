import os
import requests
import pandas as pd


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

    def fetch_stock_screener_results(self, exchange_list="nyse,nasdaq,amex", market_cap_more_than=2000000000,
                                     price_more_than=10, beta_lower_than=1, country='US', limit=1000):
        """
        Fetches stock screener results from the FMP API.

        Parameters:
            exchange_list (str): List of exchanges.
            market_cap_more_than (int): Minimum market cap.
            price_more_than (float): Minimum stock price.
            beta_lower_than (float): Maximum beta.
            country (str): Country filter.
            limit (int): Maximum number of results.

        Returns:
            pd.DataFrame: DataFrame with stock screener results.
        """
        try:
            url = f"https://financialmodelingprep.com/api/v3/stock-screener?exchange={exchange_list}&limit={limit}&marketCapMoreThan={market_cap_more_than}&betaLowerThan={beta_lower_than}&country={country}&priceMoreThan={price_more_than}&isActivelyTrading=true&isFund=false&isEtf=false&apikey={self._api_key}"
            response = requests.get(url)

            if response.status_code == 200:
                securities_data = response.json()
                if securities_data:
                    securities_df = pd.DataFrame(securities_data)
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
                                   cache_dir: str = "cache") -> pd.DataFrame:
        """
        Fetches daily prices by date from the FMP API.

        Parameters:
            symbol (str): Stock symbol.
            start_date_str (str): Start date in 'YYYY-MM-DD' format.
            end_date_str (str): End date in 'YYYY-MM-DD' format.
            cache_dir (str): Directory to cache the data.

        Returns:
            pd.DataFrame: DataFrame with daily prices.
        """
        try:
            file_name = f"{symbol}-{start_date_str}-{end_date_str}-prices.csv"
            path = os.path.join(cache_dir, file_name)
            if os.path.exists(path):
                prices_df = pd.read_csv(path)
                prices_df['date'] = pd.to_datetime(prices_df['date'])
                prices_df.set_index('date', inplace=True)
                return prices_df
            else:
                url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?from={start_date_str}&to={end_date_str}&apikey={self._api_key}"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    historical_data = data.get('historical', [])
                    if historical_data:
                        prices_df = pd.DataFrame(historical_data)
                        prices_df['date'] = pd.to_datetime(prices_df['date'])
                        prices_df.set_index('date', inplace=True)
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

    def fetch_forex_rates(self, from_currency: str, to_currency: str) -> pd.DataFrame:
        """
        Fetches forex rates from the FMP API.

        Parameters:
            from_currency (str): The base currency.
            to_currency (str): The target currency.

        Returns:
            pd.DataFrame: DataFrame with forex rates.
        """
        try:
            url = f"https://financialmodelingprep.com/api/v3/fx/{from_currency}-{to_currency}?apikey={self._api_key}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                forex_rates_df = pd.DataFrame(data)
                return forex_rates_df
            else:
                return None
        except Exception as ex:
            print(ex)
            return None

    def fetch_crypto_prices(self, symbol: str) -> pd.DataFrame:
        """
        Fetches crypto prices from the FMP API.

        Parameters:
            symbol (str): Crypto symbol.

        Returns:
            pd.DataFrame: DataFrame with crypto prices.
        """
        try:
            url = f"https://financialmodelingprep.com/api/v3/historical-price-full/crypto/{symbol}?apikey={self._api_key}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                historical_data = data.get('historical', [])
                if historical_data:
                    crypto_prices_df = pd.DataFrame(historical_data)
                    crypto_prices_df['date'] = pd.to_datetime(crypto_prices_df['date'])
                    crypto_prices_df.set_index('date', inplace=True)
                    return crypto_prices_df
                else:
                    return None
            else:
                return None
        except Exception as ex:
            print(ex)
            return None
