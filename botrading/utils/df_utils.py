import pandas as pd
import numpy as np

"""
Dataframe utils
"""

#  Remove abnormal outlier data points using scipy.stats z-score
def remove_outliers_zscore(df, column_name, z_threshold=3):
    df[column_name] = df[column_name].fillna(df[column_name].median())
    # Calculate z-scores
    df['z_score'] = zscore(df[column_name])
    # Filter rows based on z score
    df = df[(df['z_score'] < z_threshold) & (df['z_score'] > -z_threshold)]
    df.drop(columns=['z_score'], inplace=True)
    return df


def standardize_ohlcv_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes an OHLCV dataframe by renaming columns, handling infinites, dropping NaNs, and converting date column to datetime.

    Parameters:
        df (pd.DataFrame): The OHLCV data frame.

    Returns:
        pd.DataFrame: The standardized data frame.
    """
    # Define a mapping for renaming columns
    rename_mapping = {
        'Date': 'date',
        'Datetime': 'date',
        'DateTime': 'date',
        'Time': 'time',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'AdjClose': 'adj_close',
        'Adj Close': 'adj_close',
        'Volume': 'volume'
    }

    # Rename columns
    df = df.rename(columns=str.lower)
    df = df.rename(columns=rename_mapping)

    # Convert date column to datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Replace infinite values with NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Drop rows with NaN values
    df.dropna(inplace=True)

    # Forward fill and then fill remaining NaNs with 0
    df.fillna(method='ffill', inplace=True)
    df.fillna(0, inplace=True)

    # Ensure numeric columns have a numeric format
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = pd.to_numeric(df[column], errors='coerce')

    return df


def check_ohlc_dataframe(df: pd.DataFrame, min_length: int = 10) -> bool:
    """
    Checks the validity of an OHLC dataframe.

    Parameters:
        df (pd.DataFrame): The OHLC data frame.
        min_length (int): The minimum length the dataframe should have.

    Returns:
        bool: True if the dataframe is valid, False otherwise.
    """
    required_columns = ['open', 'high', 'low', 'close', 'volume']

    # Check if dataframe is None
    if df is None:
        print("Dataframe is None.")
        return False

    # Check if dataframe has the required minimum length
    if len(df) < min_length:
        print(f"Dataframe does not have the required minimum length of {min_length}.")
        return False

    # Check if all required columns are present
    for column in required_columns:
        if column not in df.columns:
            print(f"Missing required column: {column}")
            return False

    # Convert date column to datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Ensure numeric columns have a numeric format
    for column in ['open', 'high', 'low', 'close', 'volume']:
        df[column] = pd.to_numeric(df[column], errors='coerce')

    # Check for any missing values
    if df[required_columns].isnull().any().any():
        print("Dataframe contains missing values.")
        return False

    # Check for any infinite values - todo
    #if np.isinf(df[required_columns].values).any():
    #    print("Dataframe contains infinite values.")
    #    return False

    # Check if high >= low
    if (df['high'] < df['low']).any():
        print("High values are less than low values in the dataframe.")
        return False

    # Check if close/open/high/low/volume are positive
    if (df[['open', 'high', 'low', 'close', 'volume']] < 0).any().any():
        print("Negative values found in open, high, low, close, or volume columns.")
        return False

    print("Dataframe is valid.")
    return True
