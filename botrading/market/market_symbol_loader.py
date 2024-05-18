import os
import pandas as pd


class MarketSymbolLoader:
    """
    MarketSymbolLoader provides the ability to load a list of stock symbols for different market indexes

    Attributes:
        None
    """
    def __init__(self):
        pass

    def fetch_nasdaq100_symbols(self, cache_file=False, cache_dir="cache", file_name=f"nasdaq100_symbols.csv"):
        """
        Fetches the list of NASDAQ 100 symbols.

        Parameters:
            cache_file (bool): Flag to indicate if the list should be cached
            cache_dir (str): Cache directory
            file_name (str): Cache file name

        Returns:
            DataFrame: dataframe with list of symbols and additional info.
        """
        wiki_url = 'https://en.wikipedia.org/wiki/Nasdaq-100#:~:text=It%20created%20two%20indices%3A%20the,firms%2C%20and%20Mortgage%20loan%20companies.'
        try:
            cache_path = os.path.join(cache_dir, file_name)
            # Create cache dir if needed
            if cache_file is True and not os.path.exists(cache_path):
                os.mkdirs(cache_dir)

            # Try to load file from cache
            if os.path.exists(cache_path) and cache_file is True:
                symbols_df = pd.read_csv(cache_path)
                return symbols_df
            else:
                table = pd.read_html(wiki_url)
                symbols_df = table[4]
                symbols_df.rename(columns={'Ticker': "SYMBOL"}, inplace=True)
                # Cache file
                if os.path.exists(cache_path) and cache_file is True:
                    symbols_df.to_csv(cache_path)
                return symbols_df
        except Exception as e:
            print(f"Failed to fetch NASDAQ 100 symbols, error: {str(e)}")
            return None