import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta


class YahooDataLoader:
    def __init__(self):
        pass

    @staticmethod
    def fetch_intraday_prices(symbol: str, interval: str, start_date_str: str, end_date_str: str, cache_data: bool=False, cache_dir: str="cache"):
        try:
            # Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            file_name = f"{symbol}_i{interval}_start{start_date_str}_end{end_date_str}.csv"
            path = os.path.join(cache_dir, file_name)
            if cache_data is True and os.path.exists(path):
                prices_df = pd.read_csv(path, parse_dates=['date'])
            else:
                data = yf.download(tickers=symbol, start=start_date_str, end=end_date_str, interval=interval)
                prices_df = pd.DataFrame(data)
                prices_df.reset_index(inplace=True)
                prices_df.columns = [col.lower().replace(' ', '_') for col in prices_df.columns]

                # Store for caching
                os.makedirs(cache_dir, exist_ok=True)
                prices_df.to_csv(path, index=False)

            return prices_df
        except Exception as ex:
            print(f"Failed to fetch Yahoo prices: {ex}")
            return None

    def fetch_multiple_intraday_prices(self, symbol_list: list[str], interval: str, start_date_str: str, end_date_str: str, cache_data: bool=False, cache_dir: str="cache"):
        prices_dict = {}
        for symbol in symbol_list:
            prices_df = self.fetch_intraday_prices(symbol, interval, start_date_str, end_date_str, cache_data, cache_dir)
            if prices_df is not None:
                prices_dict[symbol] = prices_df

        return prices_dict

    def fetch_risk_free_rate(self, symbol: str = "^IRX", start_date_str: str = None, end_date_str: str = None, cache_data: bool = False, cache_dir: str = "cache"):
        try:
            if start_date_str is None:
                start_date = datetime.today() - timedelta(days=5)
                start_date_str = start_date.strftime("%Y-%m-%d")
            if end_date_str is None:
                end_date = datetime.today()
                end_date_str = end_date.strftime("%Y-%m-%d")

            file_name = f"{symbol}_risk_free_rate.csv"
            path = os.path.join(cache_dir, file_name)

            if cache_data and os.path.exists(path):
                prices_df = pd.read_csv(path, parse_dates=['date'])
            else:
                data = yf.download(tickers=symbol, start=start_date_str, end=end_date_str, interval='1d')
                prices_df = pd.DataFrame(data)
                prices_df.reset_index(inplace=True)
                prices_df.columns = [col.lower().replace(' ', '_') for col in prices_df.columns]

                if cache_data:
                    os.makedirs(cache_dir, exist_ok=True)
                    prices_df.to_csv(path, index=False)

            # Extract the most recent risk-free rate
            recent_rate = prices_df['close'].iloc[-1] / 100  # Convert percentage to decimal
            return recent_rate
        except Exception as ex:
            print(f"Failed to fetch risk-free rate: {ex}")
            return None