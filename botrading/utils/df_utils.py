import pandas as pd
import numpy as np
import os

"""
Dataframe utils
"""

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
"""

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
        'adjclose': 'adj_close',
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

    # Forward fill
    df.ffill(inplace=True)

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
    return True


def replace_inf_values(df: pd.DataFrame, method: str = 'ffill') -> pd.DataFrame:
    """
    Handles infinite values in a DataFrame by replacing them with NaN and applying the specified method.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        method (str): The method to handle NaN values after replacing infinities. Options are:
                      - 'drop': Drop rows with NaN values.
                      - 'ffill': Forward fill NaN values.
                      - 'bfill': Backward fill NaN values.
                      - 'zero': Fill NaN values with zero.

    Returns:
        pd.DataFrame: The DataFrame with infinite values handled.
    """
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    if method == 'drop':
        df.dropna(inplace=True)
    elif method == 'ffill':
        df.ffill(inplace=True)
        df.fillna(0, inplace=True)
    elif method == 'bfill':
        df.bfill(inplace=True)
        df.fillna(0, inplace=True)
    elif method == 'zero':
        df.fillna(0, inplace=True)
    else:
        raise ValueError("Invalid method. Choose from 'drop', 'ffill', 'bfill', or 'zero'.")

    return df


def load_dataframe_from_csv(directory: str, file_name: str) -> pd.DataFrame:
    """
    Loads a DataFrame from a CSV file in the specified directory.

    Parameters:
        directory (str): The directory where the file is located.
        file_name (str): The name of the file to load the DataFrame from.

    Returns:
        pd.DataFrame: The loaded DataFrame.

    Raises:
        ValueError: If the file_name is not provided or the file does not exist.
        Exception: For any other exceptions that may occur during the loading process.
    """
    # Validate inputs
    if not file_name:
        raise ValueError("The file name must be provided.")

    # Construct the full path
    path = os.path.join(directory, file_name)

    # Check if the path exists
    if not os.path.exists(path):
        print(f"Path {path} does not exist - returning None")
        return None

    # Load the DataFrame from CSV
    try:
        df = pd.read_csv(path)
        #print(f"DataFrame successfully loaded from {path}")
        return df
    except Exception as e:
        print(f"An error occurred while loading the DataFrame: {e}")
        raise


def save_dataframe_to_csv(df: pd.DataFrame, directory: str, file_name: str):
    """
    Saves a DataFrame to a CSV file in the specified directory.

    Parameters:
        df (pd.DataFrame): The DataFrame to be saved.
        directory (str): The directory where the file should be saved.
        file_name (str): The name of the file to save the DataFrame to.

    Raises:
        ValueError: If the DataFrame is empty or the file_name is not provided.
        Exception: For any other exceptions that may occur during the saving process.
    """
    # Validate inputs
    if df.empty:
        raise ValueError("The DataFrame is empty and cannot be saved.")
    if not file_name:
        raise ValueError("The file name must be provided.")

    # Create directory if it does not exist
    try:
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, file_name)

        # Save DataFrame to CSV
        df.to_csv(path, index=False)
        print(f"DataFrame successfully saved to {path}")
    except Exception as e:
        print(f"An error occurred while saving the DataFrame: {e}")
        raise