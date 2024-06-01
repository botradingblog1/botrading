# botrading
Python package with utilities for trading developed for B/O Trading Blog (https://algorithmictrading.substack.com/).

## Installation
```commandline
pip install botrading
```

### Install TA-Lib using Conda
In case the TA-Lib installation fails, you can install TA-Lib using conda:
```
conda install -c conda-forge ta-lib
```

## MarketSymbol Loader
MarketSymbolLoader Class
The MarketSymbolLoader class provides methods to load a list of stock symbols for different market indexes from Wikipedia.

### Methods
**fetch_nasdaq100_symbols**
Fetches the list of NASDAQ 100 symbols.

**Parameters**
cache_file (bool): Flag to indicate if the list should be cached.
cache_dir (str): Cache directory.
file_name (str): Cache file name.

Returns
pd.DataFrame: DataFrame with list of symbols and additional info.

Example
```
loader = MarketSymbolLoader()
nasdaq100_symbols = loader.fetch_nasdaq100_symbols(cache_file=True)
```

**fetch_dji_symbols**
Fetches the list of Dow Jones Industrial Average (DJI) symbols.

**Parameters**
cache_file (bool): Flag to indicate if the list should be cached.
cache_dir (str): Cache directory.
file_name (str): Cache file name.

**Returns**
pd.DataFrame: DataFrame with list of symbols and additional info.

**Example**
```
dji_symbols = loader.fetch_dji_symbols(cache_file=True)
```

**fetch_sp500_symbols**
Fetches the list of S&P 500 symbols.

**Parameters**
cache_file (bool): Flag to indicate if the list should be cached.
cache_dir (str): Cache directory.
file_name (str): Cache file name.

**Returns**
pd.DataFrame: DataFrame with list of symbols and additional info.

```
sp500_symbols = loader.fetch_sp500_symbols(cache_file=True)
```

**fetch_russell1000_symbols**
Fetches the list of Russell 1000 symbols.

**Parameters**
cache_file (bool): Flag to indicate if the list should be cached.
cache_dir (str): Cache directory.
file_name (str): Cache file name.

**Returns**
pd.DataFrame: DataFrame with list of symbols and additional info.

**Example**
```
russell1000_symbols = loader.fetch_russell1000_symbols(cache_file=True)
```

**fetch_russell2000_symbols**
Fetches the list of Russell 2000 symbols.

**Parameters**
cache_file (bool): Flag to indicate if the list should be cached.
cache_dir (str): Cache directory.
file_name (str): Cache file name.

**Returns**
pd.DataFrame: DataFrame with list of symbols and additional info.

Example
```
russell2000_symbols = loader.fetch_russell2000_symbols(cache_file=True)
```

**fetch_symbols**
Fetches the list of symbols for the specified market index.

**Parameters**
market_index (MarketIndex): The market index to fetch symbols for.
cache_file (bool): Flag to indicate if the list should be cached.
cache_dir (str): Cache directory.

**Returns**
pd.DataFrame: DataFrame with list of symbols and additional info.

**Example**
```
from botrading.enums import MarketIndex

loader = MarketSymbolLoader()
symbols = loader.fetch_symbols(MarketIndex.NASDAQ_100, cache_file=True)
```

## Tiingo API Wrapper
The TiingoDataLoader class provides methods to easily interact with Tiingo APIs to fetch data such as stock prices and in the future we will add APIs for crypto prices, news, and forex data.

**fetch_intraday_prices**
Fetches intraday stock prices from Tiingo API.

**Parameters**
symbol (str): Stock symbol.
start_date_str (str): Start date in 'YYYY-MM-DD' format.
end_date_str (str): End date in 'YYYY-MM-DD' format.
interval (TiingoIntradayInterval): Data interval.
cache_data (bool): Whether to cache the data.
cache_dir (str): Directory to save the cached data.

**Returns**
pd.DataFrame: DataFrame with stock prices.

**Example**
```
from botrading.enums import TiingoIntradayInterval

loader = TiingoDataLoader(api_key='your_api_key')
prices = loader.fetch_intraday_prices(
    symbol='AAPL', 
    start_date_str='2023-01-01', 
    end_date_str='2023-01-31', 
    interval=TiingoIntradayInterval.ONE_MINUTE,
    cache_data=True
)
```

**fetch_multiple_intraday_prices**
Fetches intraday stock prices for multiple symbols from Tiingo API.

**Parameters**
symbol_list (List[str]): List of stock symbols.
start_date_str (str): Start date in 'YYYY-MM-DD' format.
end_date_str (str): End date in 'YYYY-MM-DD' format.
interval (TiingoIntradayInterval): Data interval.
cache_data (bool): Whether to cache the data.
cache_dir (str): Directory to save the cached data.

**Returns**
dict: Dictionary with stock symbols as keys and DataFrames with stock prices as values.

**Example**
```
from botrading.enums import TiingoIntradayInterval

loader = TiingoDataLoader(api_key='your_api_key')
symbols = ['AAPL', 'MSFT']
prices_dict = loader.fetch_multiple_intraday_prices(
    symbol_list=symbols, 
    start_date_str='2023-01-01', 
    end_date_str='2023-01-31', 
    interval=TiingoIntradayInterval.ONE_MINUTE,
    cache_data=True
)
for symbol, prices in prices_dict.items():
    print(f"Prices for {symbol}:\n", prices.head())
```

**fetch_end_of_day_prices**
Fetches daily stock prices from Tiingo API.

**Parameters**
symbol (str): Stock symbol.
start_date (str): Start date in 'YYYY-MM-DD' format.
end_date (str): End date in 'YYYY-MM-DD' format.
interval (TiingoDailyInterval): Data interval.
cache_data (bool): Whether to cache the data.
cache_dir (str): Directory to save the cached data.

**Returns**
pd.DataFrame: DataFrame with stock prices.

**Example**
```
from botrading.enums import TiingoDailyInterval

loader = TiingoDataLoader(api_key='your_api_key')
daily_prices = loader.fetch_end_of_day_prices(
    symbol='AAPL', 
    start_date='2023-01-01', 
    end_date='2023-12-31', 
    interval=TiingoDailyInterval.DAILY,
    cache_data=True
)
```

**Enum Classes (from botrading.enums)**
To use the TiingoDataLoader class methods, you need to import the necessary enums from botrading.enums.

**TiingoIntradayInterval**
Defines the intervals for intraday data.

```
class TiingoIntradayInterval(Enum):
    ONE_MINUTE = '1min'
    FIVE_MINUTES = '5min'
    FIFTEEN_MINUTES = '15min'
    THIRTY_MINUTES = '30min'
    HOURLY = '1hour'
```

**TiingoDailyInterval**
Defines the intervals for daily data.

```
class TiingoDailyInterval(Enum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
```

**fetch_multiple_end_of_day_prices**
Fetches daily prices for multiple stock symbols.

**Parameters**
symbol_list (List[str]): List of stock symbols.
start_date_str (str): Start date in 'YYYY-MM-DD' format.
end_date_str (str): End date in 'YYYY-MM-DD' format.
interval (TiingoDailyInterval): The interval, e.g. daily, weekly, monthly
cache_data (bool): Flag to specify if data should be cached. Default is False.
cache_dir (str): Directory to cache the data. Default is "cache".

**Returns**
pd.DataFrame: DataFrame containing the daily prices for multiple symbols.

**Example**
```
from datetime import datetime
import pandas as pd
from botrading.data_loaders.tiingo_data_loader import TiingoDataLoader

loader = TiingoDataLoader()
symbols = ['AAPL', 'GOOGL', 'MSFT']
start_date = '2023-01-01'
end_date = '2023-03-01'

prices_df = loader.fetch_multiple_daily_prices(symbols, start_date, end_date)
```

## FinancialModelingPrep (FMP) API Wrapper
### FmpDataLoader Class
The FmpDataLoader class provides methods to interact with the Financial Modeling Prep (FMP) API to fetch various financial data.

#### Initialization
```
def __init__(self, api_key: str):
    """
    Initializes the FmpDataLoader with the given API key.
    """
```


#### Methods
**fetch_stock_screener_results**
Fetches stock screener results from the FMP API.

**Parameters**
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
cache_dir (str): Cache directory.
file_name (str): Cache file name.

Returns
pd.DataFrame: DataFrame with stock screener results.

```
loader = FmpDataLoader(api_key='your_api_key')
results = loader.fetch_stock_screener_results(exchange='NYSE', limit=100)
```

**fetch_dividend_calendar**
Fetches the dividend calendar from the FMP API.

**Parameters**
start_date_str (str): Start date in 'YYYY-MM-DD' format.
end_date_str (str): End date in 'YYYY-MM-DD' format.
Returns
pd.DataFrame: DataFrame with dividend calendar data.

```commandline
dividend_calendar = loader.fetch_dividend_calendar(start_date_str='2023-01-01', end_date_str='2023-12-31')
```

**fetch_daily_prices_by_date**
Fetches daily prices by date from the FMP API.

**Parameters**
symbol (str): Stock symbol.
start_date_str (str): Start date in 'YYYY-MM-DD' format.
end_date_str (str): End date in 'YYYY-MM-DD' format.
cache_data (bool): Flag to specify if data should be cached.
cache_dir (str): Directory to cache the data.

Returns
pd.DataFrame: DataFrame with daily prices.

```
prices = loader.fetch_daily_prices_by_date(symbol='AAPL', start_date_str='2023-01-01', end_date_str='2023-12-31')
```

**fetch_multiple_daily_prices_by_date**
Fetches daily prices by date for multiple symbols from the FMP API.

**Parameters**
symbol_list (list): List of stock symbols.
start_date_str (str): Start date in 'YYYY-MM-DD' format.
end_date_str (str): End date in 'YYYY-MM-DD' format.
cache_data (bool): Flag to specify if data should be cached.
cache_dir (str): Directory to cache the data.

Returns
dict: A dictionary with symbols as keys and DataFrames with daily prices as values.

Example
```
symbols = ['AAPL', 'MSFT']
prices = loader.fetch_multiple_daily_prices_by_date(symbol_list=symbols, start_date_str='2023-01-01', end_date_str='2023-12-31')
for symbol, df in prices.items():
    print(f"Prices for {symbol}:\n", df.head())
```

**fetch_dividends**
Fetches historical dividends for a stock from the FMP API.

**Parameters**
symbol (str): Stock symbol.

Returns
pd.DataFrame: DataFrame with historical dividend data.

Example:
```
dividends = loader.fetch_dividends(symbol='AAPL')
```

## Data Processing Tools

**normalize_dataframe_columns**
Normalizes specific columns of a DataFrame using either StandardScaler or MinMaxScaler.

**Parameters**
df (pd.DataFrame): DataFrame containing the column to normalize.
column_list (list): List of columns to normalize.
scaler_type (str): The type of scaler to use ('minmax' or 'standard').

**Returns**
pd.DataFrame: DataFrame with the normalized column.

**Example**
```
from botrading.data_processing.data_processing_tools import normalize_dataframe_column

# Sample dataframe
df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [5, 6, 7, 8, 9], 'C': [10, 20, 30, 40, 50]})

# Normalize
normalized_df = normalize_dataframe_columns(df, ['A', 'B'], scaler_type='minmax'
```

**normalize_dataframe**
Normalizes all columns of a DataFrame independently using either StandardScaler or MinMaxScaler.

**Parameters**
df (pd.DataFrame): DataFrame to normalize.
scaler_type (str): The type of scaler to use ('minmax' or 'standard').

**Returns**
pd.DataFrame: DataFrame with all columns normalized.

**Example**
```
from botrading.data_processing.data_processing_tools import normalize_dataframe

# Create a sample DataFrame
df = pd.DataFrame({'A': [1, 2, 3, 4, 5], 'B': [5, 6, 7, 8, 9]})

# Normalize all columns using StandardScaler
normalized_df = normalize_dataframe(df, scaler_type='standard')
```

**add_kernel_reg_smoothed_line**
Adds smoothed lines to the DataFrame using kernel regression for multiple columns.

**Parameters**
df (pd.DataFrame): The input DataFrame containing the data.
column_list (list of str): A list of column names containing the data to be smoothed. Default is ['close'].
output_cols (list of str, optional): A list of output column names where the smoothed data will be stored. If None, the output column names will be the input column names with _smoothed appended.
bandwidth (float): The bandwidth parameter for kernel regression. Default is 2.
var_type (str): A string of length equal to the number of variables in exog, containing a code for each variable. Default is 'c' for continuous variables.

**Returns**
pd.DataFrame: The DataFrame with additional columns containing the smoothed values.

**Example**
```
from botrading.data_processing.data_processing_tools import add_kernel_reg_smoothed_line

# Create a sample DataFrame
df = pd.DataFrame({
    'close': [10, 12, 13, 15, 16, 18, 20, 22, 24, 25],
    'volume': [100, 110, 105, 115, 120, 125, 130, 135, 140, 145]
})

# Add smoothed lines to the DataFrame
smoothed_df = add_kernel_reg_smoothed_line(df, column_list=['close'], bandwidth=1)
```

**normalize_dataframe_columns**
Normalizes specific columns of a DataFrame and adds new columns with a _norm suffix.

**Parameters**
df (pd.DataFrame): DataFrame containing the columns to normalize.
column_list (list): List of column names to normalize. Default is ['close'].
scaler_type (str): The type of scaler to use ('minmax' or 'standard'). Default is 'minmax'.
keep_original (bool): Flag to keep the original columns. If False, original columns will be dropped. Default is True.

**Returns**
pd.DataFrame: DataFrame with the normalized columns added.

**Example**
```commandline
from botrading.data_processing.data_processing_tools import normalize_dataframe_columns

# Create a sample DataFrame
df = pd.DataFrame({
    'close': [1, 2, 3, 4, 5],
    'volume': [5, 6, 7, 8, 9]
})

# Normalize the 'close' and 'volume' columns using MinMaxScaler
normalized_df = normalize_dataframe_columns(df, column_list=['close', 'volume'], scaler_type='minmax', keep_original=True)
```

**normalize_dataframe**
Normalizes all columns of a DataFrame independently and adds new columns with a _norm suffix.

**Parameters**
df (pd.DataFrame): DataFrame to normalize.
scaler_type (str): The type of scaler to use ('minmax' or 'standard'). Default is 'minmax'.
keep_original (bool): Flag to keep the original columns. If False, original columns will be dropped. Default is True.

**Returns**
pd.DataFrame: DataFrame with all normalized columns added.

**Example**
```
from botrading.data_processing.data_processing_tools import normalize_dataframe

# Create a sample DataFrame
df = pd.DataFrame({
    'close': [1, 2, 3, 4, 5],
    'volume': [5, 6, 7, 8, 9]
})

# Normalize all columns using MinMaxScaler
normalized_df = normalize_dataframe(df, scaler_type='minmax', keep_original=True)
```

## Feature analysis tools
**process_dict_calculate_peer_correlation**
Calculates peer correlations between pairs of stock symbols based on their price data.

**Parameters**
prices_dict (dict): A dictionary where keys are stock symbols and values are DataFrames containing price data.
target_column (str): The column name in the DataFrames that contains the price data to be used for correlation calculations. Default is 'close'.

**Returns**
pd.DataFrame: DataFrame containing the correlation scores for each pair of symbols.
dict: Dictionary containing merged DataFrames for each pair of symbols.

**Example**
```
import numpy as np
import pandas as pd
from botrading.feature_engineering.feature_analysis import process_dict_calculate_peer_correlation

# Create sample DataFrames
df_aapl = pd.DataFrame({
    'date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
    'close': np.random.rand(100)
})
df_googl = pd.DataFrame({
    'date': pd.date_range(start='2023-01-01', periods=100, freq='D'),
    'close': np.random.rand(100)
})


# Create a dictionary of price data
prices_dict = {
    'AAPL': df_aapl,
    'GOOGL': df_googl,
}

# Calculate peer correlations
correlation_df, peer_data_dict = process_dict_calculate_peer_correlation(prices_dict, target_column='close')

```



## Plot Utilities
**plot_candlestick_chart**
Plots a candlestick chart with optional additional columns and themes.

**Parameters**
df (pd.DataFrame): DataFrame with columns 'Open', 'High', 'Low', 'Close', and optionally 'Volume'.
volume (bool): Flag to add a volume histogram. Default is False.
extra_cols (list of str, optional): List of additional columns to chart.
extra_cols_in_main_chart (list of bool, optional): List of booleans specifying if the extra columns should be plotted in the main chart.
title (str): Title of the chart. Default is "Candlestick Chart".
fig_size (tuple, optional): Size of the plot. Default is (10, 6).
dpi (int, optional): DPI for the saved figure. Default is 300.
path (str, optional): Path to save the chart. Default is None.
file_name (str, optional): File name to save the chart. Default is None.
theme_class (class, optional): Theme class with color palette. Default is LightTheme.

**Returns**
None

**Example**
```
import pandas as pd
from botrading.utils.plot_utils import plot_candlestick_chart
from botrading.themes.light_theme import LightTheme

# Create a sample DataFrame
data = {
    'open': [100, 102, 101, 105, 107],
    'high': [105, 103, 106, 108, 110],
    'low': [99, 101, 100, 104, 106],
    'close': [104, 102, 105, 107, 109],
    'volume': [1000, 1500, 1200, 1300, 1400]
}
df = pd.DataFrame(data, index=pd.date_range(start='2023-01-01', periods=5))

# Plot candlestick chart
plot_candlestick_chart(df, volume=True, title="Sample Candlestick Chart", fig_size=(10, 6), dpi=300, path='charts', file_name='candlestick_chart.png', theme_class=LightTheme))
```

**plot_line_chart**
Plots a line chart for specified columns using a given theme.

**Parameters**
df (pd.DataFrame): DataFrame containing the data to be plotted.
column_list (list of str): List of columns to plot. Default is ['close'].
title (str): Title of the chart. Default is "Line Chart".
fig_size (tuple, optional): Size of the plot. Default is (10, 6).
dpi (int, optional): DPI for the saved figure. Default is 300.
path (str, optional): Path to save the chart. Default is None.
file_name (str, optional): File name to save the chart. Default is None.
theme_class (class, optional): Theme class with color palette. Default is LightTheme.

**Returns**
None

**Example**
```commandline
import pandas as pd
from botrading.utils.plot_utils import plot_line_chart
from botrading.themes.light_theme import LightTheme

```
# Create a sample DataFrame
data = {
    'close': [100, 102, 101, 105, 107],
    'volume': [1000, 1500, 1200, 1300, 1400]
}
df = pd.DataFrame(data, index=pd.date_range(start='2023-01-01', periods=5))

# Plot line chart
plot_line_chart(df, column_list=['close', 'volume'], title="Sample Line Chart", fig_size=(10, 6), dpi=300, path='charts', file_name='line_chart.png', theme_class=LightTheme)
```







# Run all tests
```commandline
cd tests

python -m unittest discover -s tests

```