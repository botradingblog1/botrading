import os
import requests
import pandas as pd
from ..utils.df_utils import standardize_ohlcv_dataframe
from typing import Union


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

    def fetch_historical_dividends(self, symbol: str) -> pd.DataFrame:
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

    def fetch_multiple_historical_dividends(self, symbol_list: list, cache_data: bool = False, cache_dir: str = "cache") -> dict:
        """
        Fetches multiple historic dividends for a list of symbols from FMP API.

        Parameters:
            symbol_list (list): List of stock symbols.
            cache_data (bool): Flag to specify if data should be cached
            cache_dir (str): Directory to cache the data.

        Returns:
            dict: A dictionary with symbols as keys and DataFrames with daily prices as values.
        """
        results = {}
        for symbol in symbol_list:
            print(f"Fetching historicsl for {symbol}...")
            df = self.fetch_historical_dividends(symbol, cache_data, cache_dir)
            if df is not None:
                results[symbol] = df
            else:
                print(f"Failed to fetch data for {symbol}")
        return results

    def fetch_historical_splits(self, symbol: str) -> pd.DataFrame:
        """
        Fetches historical stock splits for a stock from the FMP API.

        Parameters:
            symbol (str): Stock symbol.

        Returns:
            pd.DataFrame: DataFrame with historical stock splits data.
        """
        try:
            url = f"https://financialmodelingprep.com/api/v3/historical-price-full/stock_split/{symbol}?apikey={self._api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                historical_data = data.get('historical', [])
                if historical_data:
                    splits_df = pd.DataFrame(historical_data)
                    splits_df['date'] = pd.to_datetime(splits_df['date'])
                    splits_df.set_index('date', inplace=True)
                    return splits_df
                else:
                    return None
            else:
                return None
        except Exception as ex:
            print(ex)
            return None

    def fetch_multiple_historical_splits(self, symbol_list: list, cache_data: bool = False, cache_dir: str = "cache") -> dict:
        """
        Fetches multiple historical stock splits for a list of symbols from FMP API.

        Parameters:
            symbol_list (list): List of stock symbols.
            cache_data (bool): Flag to specify if data should be cached.
            cache_dir (str): Directory to cache the data.

        Returns:
            dict: A dictionary with symbols as keys and DataFrames with stock splits data as values.
        """
        results = {}
        for symbol in symbol_list:
            print(f"Fetching historical splits for {symbol}...")
            df = self.fetch_historical_splits(symbol, cache_data, cache_dir)
            if df is not None:
                results[symbol] = df
            else:
                print(f"Failed to fetch data for {symbol}")
        return results

    def fetch_tradable_list(self):
        """
        Fetch a list of tradable securities.
    
        Returns:
        - pd.DataFrame: DataFrame containing the tradable securities data, or None if no data is found.
        """
        try:
            url = f"https://financialmodelingprep.com/api/v3/available-traded/list?apikey={self._api_key}"
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
    
    
    def get_analyst_ratings(self, symbol):
        """
        Get analyst ratings for a given stock symbol.
    
        Parameters:
        - symbol (str): Stock symbol.
    
        Returns:
        - pd.DataFrame: DataFrame containing the analyst ratings data, or None if no data is found.
        """
        try:
            url = f"https://financialmodelingprep.com/api/v3/grade/{symbol}?apikey={self._api_key}"
            response = requests.get(url)
    
            if response.status_code == 200:
                grades_data = response.json()
                if grades_data:
                    grades_df = pd.DataFrame(grades_data)
                    grades_df['date'] = pd.to_datetime(grades_df['date'], errors='coerce')
                    # Filter out invalid dates (NaT values after conversion)
                    grades_df = grades_df.dropna(subset=['date'])
    
                    return grades_df
                return None
            else:
                return None
        except Exception as ex:
            print(ex)
            return None
    
    
    def get_income_growth(self, symbol, period='annual'):
        """
        Get income growth data for a given stock symbol.
    
        Parameters:
        - symbol (str): Stock symbol.
        - period (str): Reporting period, either 'annual' or 'quarterly' (default: 'annual').
    
        Returns:
        - pd.DataFrame: DataFrame containing the income growth data, or None if no data is found.
        """
        try: 
            url = f"https://financialmodelingprep.com/api/v3/income-statement-growth/{symbol}?period={period}&apikey={self._api_key}"
            response = requests.get(url)
    
            if response.status_code == 200:
                growth_data = response.json()
                if growth_data:
                    growth_df = pd.DataFrame(growth_data)
                    return growth_df
                return None
            else:
                return None
        except Exception as ex:
            print(ex)
            return None

    def get_financial_ratios(self, symbol, period):
        """
        Get financial ratios for a given stock symbol.
    
        Parameters:
        - symbol (str): Stock symbol.
        - period (str): Reporting period, either 'annual' or 'quarterly'.
    
        Returns:
        - pd.DataFrame: DataFrame containing the financial ratios data, or None if no data is found.
        """
        try:
            url = f"https://financialmodelingprep.com/api/v3/ratios/{symbol}?period={period}&apikey={self._api_key}"
            response = requests.get(url)
    
            if response.status_code == 200:
                ratios_data = response.json()
                if ratios_data:
                    ratios_df = pd.DataFrame(ratios_data)
                    return ratios_df
                return None
            else:
                return None
        except Exception as ex:
            print(ex)
            return None
    
    def get_social_sentiment(self, symbol):
        """
        Get social sentiment data for a given stock symbol.
    
        Parameters:
        - symbol (str): Stock symbol.
    
        Returns:
        - pd.DataFrame: DataFrame containing the social sentiment data, or None if no data is found.
        """
        try:
            url = f"https://financialmodelingprep.com/api/v4/historical/social-sentiment?symbol={symbol}&apikey={self._api_key}"
            response = requests.get(url)
    
            if response.status_code == 200:
                social_sentiment_data = response.json()
                if social_sentiment_data:
                    social_sentiment_df = pd.DataFrame(social_sentiment_data)
                    social_sentiment_df['date'] = pd.to_datetime(social_sentiment_df['date'], errors='coerce')
                    # Filter out invalid dates (NaT values after conversion)
                    social_sentiment_df = social_sentiment_df.dropna(subset=['date'])
    
                    return social_sentiment_df
                return None
            else:
                return None
        except Exception as ex:
            print(ex)
            return None

    def get_stock_news(self, symbol, limit):
        """
        Get the latest stock news for a given stock symbol.
    
        Parameters:
        - symbol (str): Stock symbol.
        - limit (int): Number of news articles to fetch.
    
        Returns:
        - pd.DataFrame: DataFrame containing the news articles, or None if no data is found.
        """
        try:
            url = f"https://financialmodelingprep.com/api/v3/stock_news?tickers={symbol}&limit={limit}&apikey={self._api_key}"
            response = requests.get(url)
    
            if response.status_code == 200:
                news_data = response.json()
                if news_data:
                    news_df = pd.DataFrame(news_data)
                    news_df['publishedDate'] = pd.to_datetime(news_df['publishedDate'], errors='coerce')
                    # Filter out invalid dates (NaT values after conversion)
                    news_df = news_df.dropna(subset=['publishedDate'])
    
                    return news_df
                return None
            else:
                return None
        except Exception as ex:
            print(ex)
            return None

    def fetch_all_prices(self):
        """
        Fetch real-time prices for all stocks.
    
        Returns:
        - pd.DataFrame: DataFrame containing real-time price data for all stocks, or None if no data is found.
        """
        try:
            url = f"https://financialmodelingprep.com/api/v3/stock/full/real-time-price?apikey={self._api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    all_prices_df = pd.DataFrame(data)
                    return all_prices_df
                else:
                    return None
            else:
                return None
        except Exception as ex:
            print(ex)
            return None

    def fetch_institutional_ownership_changes(self, symbol, include_current_quarter=True):
        try:
            url = f"https://financialmodelingprep.com/api/v4/institutional-ownership/symbol-ownership?symbol={symbol}&includeCurrentQuarter={str(include_current_quarter)}&apikey={self._api_key}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if data:
                    inst_own_df = pd.DataFrame(data)

                    # Sort by date
                    inst_own_df['date'] = pd.to_datetime(inst_own_df['date'], errors='coerce')
                    inst_own_df.sort_values(by=['date'], ascending=False, inplace=True)

                    # Calculate total invested percent change
                    if len(inst_own_df) > 0:
                        latest_total_invested = inst_own_df['totalInvested'].iloc[0]
                        previous_total_invested = inst_own_df['lastTotalInvested'].iloc[0]
                        if previous_total_invested > 0:
                            total_invested_percent_change = round(
                                ((latest_total_invested - previous_total_invested) / previous_total_invested), 2)
                        else:
                            total_invested_percent_change = 0

                        # Calculate investors holding change
                        latest_investors_holding = inst_own_df['investorsHolding'].iloc[0]
                        previous_investors_holding = inst_own_df['lastInvestorsHolding'].iloc[0]
                        if previous_investors_holding > 0:
                            investors_holding_change = round(
                                ((latest_investors_holding - previous_investors_holding) / previous_investors_holding), 2)
                        else:
                            investors_holding_change = 0
                    else:
                        total_invested_percent_change = 0
                        investors_holding_change = 0
                    inst_own_df['totalInvestedChange'] = total_invested_percent_change
                    inst_own_df['investorsHoldingChange'] = investors_holding_change

                    return inst_own_df
                return None
            else:
                return None
        except Exception as ex:
            print(ex)
            return None

    def fetch_multiple_institutional_ownership_changes(self, symbol_list: list, include_current_quarter: bool = True) -> dict:
        """
        Fetches historical institutional ownership for multiple symbols from FMP API for a specific date.

        Parameters:
            symbol_list (list): List of stock symbols.
            include_current_quarter (str): include current quarter

        Returns:
            dict: A dictionary with symbols as keys and DataFrames with institutional ownership data as values.
        """
        results_dict = {}
        for symbol in symbol_list:
            df = self.fetch_institutional_ownership_changes(symbol, include_current_quarter)
            if df is not None:
                results_dict[symbol] = df
            else:
                print(f"Failed to fetch data for {symbol}")
        return results_dict

    def fetch_earnings_calendar(self, start_date_str, end_date_str):
        url = f"https://financialmodelingprep.com/api/v3/earning_calendar?from={start_date_str}&to={end_date_str}&apikey={self._api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Create DataFrame from the data
            df = pd.DataFrame(data)
            return df

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the earnings calendar: {e}")
            return pd.DataFrame()  # Return an empty DataFrame in case of error

    def fetch_insider_trades(self, symbol: str, from_date_str: str, to_date_str: str, cache_data: bool = False,
                             cache_dir: str = "cache") -> pd.DataFrame:
        """
        Fetches insider trades from the FMP API.

        Parameters:
            symbol (str): Stock symbol.
            from_date_str (str): Start date in 'YYYY-MM-DD' format.
            to_date_str (str): End date in 'YYYY-MM-DD' format.
            cache_data (bool): Flag to specify if data should be cached.
            cache_dir (str): Directory to cache the data.

        Returns:
            pd.DataFrame: DataFrame with insider trades.
        """

        file_name = f"{symbol}-insider-trades-{from_date_str}-to-{to_date_str}.csv"
        path = os.path.join(cache_dir, file_name)
        if cache_data is True:
            if os.path.exists(path) is True:
                trades_df = pd.read_csv(path)
                trades_df['transactionDate'] = pd.to_datetime(trades_df['transactionDate'])
                trades_df.set_index('transactionDate', inplace=True)
                trades_df = trades_df[(trades_df.index >= from_date_str) & (trades_df.index <= to_date_str)]
                return trades_df

        try:
            url = f"https://financialmodelingprep.com/api/v4/insider-trading?symbol={symbol}&apikey={self._api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    trades_df = pd.DataFrame(data)
                    trades_df['transactionDate'] = pd.to_datetime(trades_df['transactionDate'])
                    trades_df.set_index('transactionDate', inplace=True)
                    trades_df.sort_values(by=['transactionDate'], ascending=True, inplace=True)

                    # Filter by date range
                    trades_df = trades_df[(trades_df.index >= from_date_str) & (trades_df.index <= to_date_str)]

                    if cache_data is True:
                        os.makedirs(cache_dir, exist_ok=True)
                        trades_df.to_csv(path)
                    return trades_df
                else:
                    return None
            else:
                print(f"Failed to fetch insider trades. Error: {response.reason}")
                return None
        except Exception as ex:
            print(ex)
            return None

    def fetch_multiple_insider_trades_by_date(self, symbol_list: list, start_date_str: str, end_date_str: str, cache_data: bool = False, cache_dir: str = "cache") -> dict:
        """
        Fetches daily prices by date for multiple insider trades from the FMP API.

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
            print(f"Now fetching insider trades data for {symbol}...")
            df = self.fetch_insider_trades(symbol, start_date_str, end_date_str, cache_data, cache_dir)
            if df is not None:
                results[symbol] = df
            else:
                print(f"Failed to fetch insider trades data for {symbol}")
        return results

    def fetch_analyst_earnings_estimates(self, symbol: str, period: str, limit: int=100) -> Union[pd.DataFrame, None]:
        """
        Fetches analyst estimates data from the FMP API.

        Parameters:
            symbol (str): Stock symbol.
            period (Period): Period for the estimates, either 'quarter' or 'annual'
            limit (int): Number of records to fetch.
            api_key (str): Your FMP API key.

        Returns:
            pd.DataFrame: DataFrame with analyst estimates data or None if the request fails.
        """
        try:
            url = f"https://financialmodelingprep.com/api/v3/analyst-estimates/{symbol}?period={period}&limit={limit}&apikey={self._api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    estimates_df = pd.DataFrame(data)
                    return estimates_df
                else:
                    print(f"No data found for {symbol}.")
                    return None
            else:
                print(f"Failed to fetch analyst estimates. Error: {response.reason}")
                return None
        except Exception as ex:
            print(ex)
            return None

    def fetch_multiple_analyst_earnings_estimates(self, symbol_list: list, period: str, limit=100) -> dict:
        """
        Fetches analyst earnings estimates for multiple symbols from the FMP API.

        Parameters:
            symbol_list (list): List of stock symbols
            period (Period): Period for the estimates, either 'quarter' or 'annual'
            cache_data (bool): Flag to specify if data should be cached
            cache_dir (str): Directory to cache the data.

        Returns:
            dict: A dictionary with symbols as keys and DataFrames with daily prices as values.
        """
        results = {}
        for symbol in symbol_list:
            print(f"Now fetching earnings estimate data for {symbol}...")
            df = self.fetch_analyst_earnings_estimates(symbol, period, limit)
            if df is not None:
                results[symbol] = df
            else:
                print(f"Failed to fetch data for {symbol}")
        return results

    def fetch_earnings_surprises(self, symbol: str) -> Union[pd.DataFrame, None]:
        """
        Fetches earnings surprises data from the FMP API.

        Parameters:
            symbol (str): Stock symbol.

        Returns:
            pd.DataFrame: DataFrame with earnings surprises data or None if the request fails.
        """
        try:
            url = f"https://financialmodelingprep.com/api/v3/earnings-surprises/{symbol}?apikey={self._api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    surprises_df = pd.DataFrame(data)
                    if len(surprises_df) > 0:
                        # Convert date to pd format
                        surprises_df['date'] = pd.to_datetime(surprises_df['date'])
                        # Sort by date
                        surprises_df.sort_values(by="date", ascending=True)
                    return surprises_df
                else:
                    print(f"No data found for {symbol}.")
                    return None
            else:
                print(f"Failed to fetch earnings surprises. Error: {response.reason}")
                return None
        except Exception as ex:
            print(ex)
            return None

    def fetch_price_targets(self, symbol: str, cache_data: bool = False,
                            cache_dir: str = "cache") -> pd.DataFrame:
        """
        Fetches price targets from the FMP API.

        Parameters:
            symbol (str): Stock symbol.
            cache_data (bool): Flag to specify if data should be cached.
            cache_dir (str): Directory to cache the data.

        Returns:
            pd.DataFrame: DataFrame with price targets.
        """

        file_name = f"{symbol}-price-targets.csv"
        path = os.path.join(cache_dir, file_name)
        if cache_data is True:
            if os.path.exists(path) is True:
                price_targets_df = pd.read_csv(path)
                price_targets_df['publishedDate'] = pd.to_datetime(price_targets_df['publishedDate'])
                return price_targets_df

        try:
            url = f"https://financialmodelingprep.com/api/v4/price-target?symbol={symbol}&apikey={self._api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    price_targets_df = pd.DataFrame(data)
                    price_targets_df['publishedDate'] = pd.to_datetime(price_targets_df['publishedDate'])
                    price_targets_df.sort_values(by=['publishedDate'], ascending=True, inplace=True)

                    if cache_data is True:
                        os.makedirs(cache_dir, exist_ok=True)
                        price_targets_df.to_csv(path)
                    return price_targets_df
                else:
                    return None
            else:
                print(f"Failed to fetch price targets. Error: {response.reason}")
                return None
        except Exception as ex:
            print(ex)
            return None

    def fetch_multiple_price_targets_by_date(self, symbol_list: list,
                                             cache_data: bool = False, cache_dir: str = "cache") -> dict:
        """
        Fetches price targets by date for multiple symbols from the FMP API.

        Parameters:
            symbol_list (list): List of stock symbols.
            cache_data (bool): Flag to specify if data should be cached.
            cache_dir (str): Directory to cache the data.

        Returns:
            dict: A dictionary with symbols as keys and DataFrames with price targets as values.
        """
        results = {}
        for symbol in symbol_list:
            #print(f"Now fetching price target data for {symbol}...")
            df = self.fetch_price_targets(symbol, cache_data, cache_dir)
            if df is not None:
                results[symbol] = df
            else:
                print(f"Failed to fetch price target data for {symbol}")
        return results
