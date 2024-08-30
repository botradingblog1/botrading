import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from statsmodels.nonparametric.kernel_regression import KernelReg

# Disable SettingWithCopyWarning globally
pd.options.mode.chained_assignment = None  # default='warn'


def normalize_dataframe_columns(df: pd.DataFrame, column_list: list = ['close'], scaler_type: str = 'minmax', keep_original: bool = True) -> pd.DataFrame:
    """
    Normalizes specific columns of a DataFrame and adds new columns with a '_norm' suffix.

    Parameters:
        df (pd.DataFrame): DataFrame containing the columns to normalize.
        column_list (list): List of column names to normalize.
        scaler_type (str): The type of scaler to use ('minmax' or 'standard').
        keep_original (bool): Flag to keep the original columns. If False, original columns will be dropped.

    Returns:
        pd.DataFrame: DataFrame with the normalized columns added.
    """
    df_copy = df.copy()

    if scaler_type == 'minmax':
        scaler = MinMaxScaler()
    elif scaler_type == 'standard':
        scaler = StandardScaler()
    else:
        raise ValueError("Invalid scaler_type. Use 'minmax' or 'standard'.")

    for column in column_list:
        norm_col_name = f"{column}_norm"
        df_copy[norm_col_name] = scaler.fit_transform(df[[column]])

    if not keep_original:
        df_copy = df_copy.drop(columns=column_list)

    return df_copy


def normalize_dataframe(df: pd.DataFrame, scaler_type: str = 'minmax', keep_original: bool = True) -> pd.DataFrame:
    """
    Normalizes all columns of a DataFrame independently and adds new columns with a '_norm' suffix.

    Parameters:
        df (pd.DataFrame): DataFrame to normalize.
        scaler_type (str): The type of scaler to use ('minmax' or 'standard').
        keep_original (bool): Flag to keep the original columns. If False, original columns will be dropped.

    Returns:
        pd.DataFrame: DataFrame with all normalized columns added.
    """
    df_copy = df.copy()

    if scaler_type == 'minmax':
        scaler = MinMaxScaler()
    elif scaler_type == 'standard':
        scaler = StandardScaler()
    else:
        raise ValueError("Invalid scaler_type. Use 'minmax' or 'standard'.")

    norm_columns = []
    for column in df_copy.columns:
        norm_col_name = f"{column}_norm"
        df_copy[norm_col_name] = scaler.fit_transform(df[[column]])
        norm_columns.append(norm_col_name)

    if not keep_original:
        df_copy = df_copy[norm_columns]

    return df_copy


def add_kernel_reg_smoothed_line(df, column_list=['close'], output_cols=None, bandwidth=2, var_type='c'):
    """
    Adds smoothed lines to the dataframe using kernel regression for multiple columns.

    Parameters:
    df (pd.DataFrame): The input dataframe containing the data.
    column_list (list of str): A list of column names containing the data to be smoothed. Default is ['Close'].
    output_cols (list of str, optional): A list of output column names where the smoothed data will be stored.
                                         If None, the output column names will be the input column names with '_Smoothed' appended.
    bandwidth (float or list of floats): The bandwidth parameter for kernel regression. Default is 10.
    var_type (str): A string of length equal to the number of variables in exog, containing a code for each variable.
                    Default is 'c' for continuous variables.

    Returns:
    pd.DataFrame: The dataframe with additional columns containing the smoothed values.
    """

    if output_cols is None:
        output_cols = [f"{col}_smoothed" for col in column_list]
    elif len(column_list) != len(output_cols):
        raise "ERROR: Number of input columns have to equal the number of output columns"

    if not isinstance(bandwidth, list):
        bandwidth = [bandwidth] * len(column_list)

    for input_col, output_col, bw in zip(column_list, output_cols, bandwidth):
        data_list = df[input_col].values
        index_list = np.arange(0, len(data_list))

        kernel_regression = KernelReg(endog=np.array(data_list), exog=index_list, var_type=var_type, bw=[bw])
        smoothed_values, _ = kernel_regression.fit(index_list)

        df[output_col] = smoothed_values

    return df

def compute_slope(df: pd.DataFrame, target_col: str, slope_col: str, window_size: int) -> pd.DataFrame:
    """
    Computes the slope of a time series for the specified target column and adds it as a new column.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        target_col (str): The name of the column containing the target price data.
        slope_col (str): The name of the column to store the computed slopes.
        window_size (int): The rolling window size to compute the slopes.

    Returns:
        pd.DataFrame: The DataFrame with the computed slopes added as a new column.
    """

    def compute_slope_internal(y_values):
        x_values = np.arange(len(y_values))
        m, _ = np.polyfit(x_values, y_values, 1)
        return m

    # Ensure the target column exists in the DataFrame
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' does not exist in the DataFrame.")

    # Make a copy of the DataFrame to avoid SettingWithCopyWarning
    df = df.copy()

    # Compute the rolling slope and add it as a new column
    df.loc[:, slope_col] = df[target_col].rolling(window=window_size).apply(compute_slope_internal, raw=True)

    return df
