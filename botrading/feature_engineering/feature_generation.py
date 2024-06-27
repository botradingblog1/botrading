import numpy as np
import pandas as pd
import pandas_ta as ta
import talib
from botrading.base.enums import *
from botrading.base.indicator import Indicator
from ..utils.df_utils import check_ohlc_dataframe
from sklearn.cluster import AgglomerativeClustering
from typing import List


def SMA(timeperiod=200):
    return Indicator(name=IndicatorType.SMA, indicator_type=IndicatorType.SMA, params={'timeperiod': timeperiod}, is_price_based=True)

def EMA(timeperiod=3):
    return Indicator(name=IndicatorType.EMA, indicator_type=IndicatorType.EMA, params={'timeperiod': timeperiod}, is_price_based=True)

def DM(timeperiod=14):
    return Indicator(name=IndicatorType.DM, indicator_type=IndicatorType.DM, params={'timeperiod': timeperiod}, is_price_based=False)

def FisherTransform(length=9):
    return Indicator(name=IndicatorType.FISHER_TRANSFORM, indicator_type=IndicatorType.FISHER_TRANSFORM, params={'length': length}, is_price_based=False)

def WilliamsR(timeperiod=14):
    return Indicator(name=IndicatorType.WILLIAMSR, indicator_type=IndicatorType.WILLIAMSR, params={'timeperiod': timeperiod}, is_price_based=False)

def RSI(timeperiod=14):
    return Indicator(name=IndicatorType.RSI, indicator_type=IndicatorType.RSI, params={'timeperiod': timeperiod}, is_price_based=False)

def MACD(fastperiod=12, slowperiod=26, signalperiod=9):
    return Indicator(name=IndicatorType.MACD, indicator_type=IndicatorType.MACD, params={'fastperiod': fastperiod, 'slowperiod': slowperiod, 'signalperiod': signalperiod}, is_price_based=True)

def BBANDS(timeperiod=20, nbdevup=2, nbdevdn=2):
    return Indicator(name=IndicatorType.BBANDS, indicator_type=IndicatorType.BBANDS, params={'timeperiod': timeperiod, 'nbdevup': nbdevup, 'nbdevdn': nbdevdn}, is_price_based=True)

def BBANDS_LOWER(timeperiod=20, nbdevup=2, nbdevdn=2):
    return Indicator(name=IndicatorType.BBANDS_LOWER, indicator_type=IndicatorType.BBANDS_LOWER, params={'timeperiod': timeperiod, 'nbdevup': nbdevup, 'nbdevdn': nbdevdn}, is_price_based=True)

def BBANDS_MIDDLE(timeperiod=20, nbdevup=2, nbdevdn=2):
    return Indicator(name=IndicatorType.BBANDS_MIDDLE, indicator_type=IndicatorType.BBANDS_MIDDLE, params={'timeperiod': timeperiod, 'nbdevup': nbdevup, 'nbdevdn': nbdevdn}, is_price_based=True)

def BBANDS_UPPER(timeperiod=20, nbdevup=2, nbdevdn=2):
    return Indicator(name=IndicatorType.BBANDS_UPPER, indicator_type=IndicatorType.BBANDS_UPPER, params={'timeperiod': timeperiod, 'nbdevup': nbdevup, 'nbdevdn': nbdevdn}, is_price_based=True)

def ATR(timeperiod=14):
    return Indicator(name=IndicatorType.ATR, indicator_type=IndicatorType.ATR, params={'timeperiod': timeperiod}, is_price_based=True)

def OBV():
    return Indicator(name=IndicatorType.OBV, indicator_type=IndicatorType.OBV, params={}, is_price_based=False)

def LAG(period=1):
    return Indicator(name=IndicatorType.LAG, indicator_type=IndicatorType.LAG, params={'period': period}, is_price_based=False)

def DELTA(period=1):
    return Indicator(name=IndicatorType.DELTA, indicator_type=IndicatorType.DELTA, params={'period': period}, is_price_based=False)


def add_future_returns(df: pd.DataFrame, num_periods: int) -> pd.DataFrame:
    """
    Adds future returns to the OHLC data frame based on the close price.

    Parameters:
        df (pd.DataFrame): The OHLC data frame (columns: date, open, high, low, close, volume).
        num_periods (int): The number of forward-looking periods for calculating future returns.

    Returns:
        pd.DataFrame: The data frame with added future returns column.
    """
    if not check_ohlc_dataframe(df):
        raise Exception("Dataframe has incorrect format. Should be (columns: date, open, high, low, close, volume)")

    # Calculate future returns
    df[f'future_return_{num_periods}p'] = df['close'].shift(-num_periods) / df['close'] - 1

    return df


def add_indicators(df: pd.DataFrame, indicators: List[Indicator]) -> pd.DataFrame:
    """
    Adds features to the OHLC data frame.

    Parameters:
        df (pd.DataFrame): The OHLC data frame (columns: date, open, high, low, close, volume).

    Returns:
        pd.DataFrame: The data frame with added features.
    """
    if not check_ohlc_dataframe(df, min_length=20):
        raise Exception("Dataframe has incorrect format. Should be (columns: date, open, high, low, close, volume), min_length=20")

    for indicator in indicators:
        df = _apply_indicator(df, indicator)
    return df


def _apply_indicator(df: pd.DataFrame, indicator: Indicator) -> pd.DataFrame:
    func_name = f"add_{indicator.name.lower()}"
    func = globals().get(func_name, None)
    if func:
        return func(df, indicator.column_name, **indicator.params)
    else:
        raise ValueError(f"Indicator {indicator.name} not supported.")

def add_lag(df: pd.DataFrame, column_name: str, period: int) -> pd.DataFrame:
    df[column_name] = df['close'].shift(period)
    return df

def add_delta(df: pd.DataFrame, column_name: str, period: int) -> pd.DataFrame:
    df[column_name] = df['close'].pct_change(periods=period)
    return df

def add_apo(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = talib.APO(df['close'], **params)
    return df

def add_macd(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    macd, macd_signal, macd_hist = talib.MACD(df['close'], **params)
    df[column_name] = macd
    df[f'{column_name}_signal'] = macd_signal
    df[f'{column_name}_hist'] = macd_hist
    return df

def add_rsi(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = talib.RSI(df['close'], **params)
    return df

def add_bbands(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    upper, middle, lower = talib.BBANDS(df['close'], **params)
    df[f"{column_name}_upper"] = upper
    df[f"{column_name}_middle"] = middle
    df[f"{column_name}_lower"] = lower
    return df

def add_bbands_lower(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    upper, middle, lower = talib.BBANDS(df['close'], **params)
    df[column_name] = lower
    return df

def add_bbands_middle(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    upper, middle, lower = talib.BBANDS(df['close'], **params)
    df[column_name] = middle
    return df

def add_bbands_upper(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    upper, middle, lower = talib.BBANDS(df['close'], **params)
    df[column_name] = upper
    return df

def add_sma(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = talib.SMA(df['close'], **params)
    return df

def add_ema(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = talib.EMA(df['close'], **params)
    return df

def add_cci(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = talib.CCI(df['high'], df['low'], df['close'], **params)
    return df

def add_cmo(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = talib.CMO(df['close'], **params)
    return df

def add_dm(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[f'{column_name}_pos'] = talib.PLUS_DM(df['high'], df['low'], **params)
    df[f'{column_name}_neg'] = talib.MINUS_DM(df['high'], df['low'], **params)
    return df

def add_mom(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = talib.MOM(df['close'], **params)
    return df

def add_ppo(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = talib.PPO(df['close'], **params)
    return df

def add_roc(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = talib.ROC(df['close'], **params)
    return df

def add_trix(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = talib.TRIX(df['close'], **params)
    return df

def add_uo(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = talib.ULTOSC(df['high'], df['low'], df['close'], **params)
    return df

def add_williamsr(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = talib.WILLR(df['high'], df['low'], df['close'], **params)
    return df

def add_fisher_transform(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    length = params.get('length', 9)
    temp_df = ta.fisher(high=df['high'], low=df['low'], **params)
    df[column_name] = temp_df[f'FISHERT_{length}_1']
    df[f'{column_name}_signal'] = temp_df[f'FISHERTs_{length}_1']
    return df

def add_adx(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = talib.ADX(df['high'], df['low'], df['close'], **params)
    return df

def add_aroon(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[f'{column_name}_down'], df[f'{column_name}_up'] = talib.AROON(df['high'], df['low'], **params)
    return df

def add_psar(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = talib.SAR(df['high'], df['low'], **params)
    return df

def add_low_bband(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name], _, _ = talib.BBANDS(df['close'], **params)
    return df

def add_high_bband(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    _, _, df[column_name] = talib.BBANDS(df['close'], **params)
    return df

def add_low_donchian(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = ta.donchian(df['high'], df['low'], lower=True, **params)
    return df

def add_high_donchian(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = ta.donchian(df['high'], df['low'], upper=True, **params)
    return df

def add_low_kc(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = ta.kc(df['high'], df['low'], df['close'], lower=True, **params)
    return df

def add_high_kc(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = ta.kc(df['high'], df['low'], df['close'], upper=True, **params)
    return df

def add_ad(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = ta.ad(df['high'], df['low'], df['close'], df['volume'])
    return df

def add_obv(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = talib.OBV(df['close'], df['volume'])
    return df

def add_cmf(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = ta.cmf(df['high'], df['low'], df['close'], df['volume'], **params)
    return df

def add_mfi(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = talib.MFI(df['high'], df['low'], df['close'], df['volume'], **params)
    return df

def add_atr(df: pd.DataFrame, column_name: str, **params) -> pd.DataFrame:
    df[column_name] = talib.ATR(df['high'], df['low'], df['close'], **params)
    return df


def add_candlestick_patterns(df: pd.DataFrame, candlestick_patterns ) -> pd.DataFrame:
    """
    Adds candlestick patterns to the data frame.

    Parameters:
        df (pd.DataFrame): The OHLC data frame.

    Returns:
        pd.DataFrame: The data frame with added candlestick patterns.
    """
    if not check_ohlc_dataframe(df):
        raise Exception("Dataframe has incorrect format. Should be (columns: date, open, high, low, close, volume)")

    for pattern in candlestick_patterns:
        df = _apply_candlestick_pattern(df, pattern.value)
    return df


def _apply_candlestick_pattern(df: pd.DataFrame, pattern: CandlestickPattern) -> pd.DataFrame:
    """
    Applies the specified candlestick pattern to the data frame.

    Parameters:
        df (pd.DataFrame): The OHLC data frame.
        pattern (CandlestickPattern): The candlestick pattern to apply.

    Returns:
        pd.DataFrame: The data frame with the added candlestick pattern.
    """
    func = getattr(talib, pattern)
    df[f'{pattern}_CANDLE_PATTERN'] = func(df['open'], df['high'], df['low'], df['close'])
    return df



def add_future_returns(df: pd.DataFrame, lookahead_period: int, source_column='close', target_column="future_returns") -> pd.DataFrame:
    """
    Generates future returns for the specified period.

    Parameters:
        df (pd.DataFrame): The OHLC data frame.
        lookahead_period (int): Number of forward-looking periods
        source_column (str): Name of the source column, e.g. close
        target_column (str): Name of the target column to create

    Returns:
        pd.DataFrame: Data frame with added future return column.
    """
    df[target_column] = df[source_column].pct_change(periods=lookahead_period).shift(-lookahead_period)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    return df


def add_support_resistance_levels(df: pd.DataFrame, window_size: int, num_clusters: int) -> pd.DataFrame:
    """
    Adds support and resistance levels to the data frame using agglomerative clustering.

    Parameters:
        df (pd.DataFrame): The OHLC data frame.
        window_size (int): The rolling window size to calculate support and resistance levels.
        num_clusters (int): The number of clusters for agglomerative clustering.

    Returns:
        pd.DataFrame: Data frame with added support and resistance levels.

    Usage:
    # OHLC data frame
    ohlc_data = ... # DataFrame with columns: date, open, high, low, close, volume

    # Add support and resistance levels
    window_size = 20
    num_clusters = 5
    enhanced_df = analyzer.add_support_resistance_levels(ohlc_data, window_size, num_clusters)
    """
    if not check_ohlc_dataframe(df):
        raise Exception("Dataframe has incorrect format. Should be (columns: date, open, high, low, close, volume)")

    support_levels = []
    resistance_levels = []

    for i in range(window_size, len(df)):
        window_data = df.iloc[:i]
        max_price = window_data['high'].rolling(window=window_size).max()
        min_price = window_data['low'].rolling(window=window_size).min()

        # Drop NaNs
        max_price = max_price.dropna()
        min_price = min_price.dropna()

        # Prepare data for clustering
        levels = pd.concat([max_price, min_price])
        levels = levels.values.reshape(-1, 1)

        # Check if we have enough levels to form the specified number of clusters
        if len(levels) >= num_clusters:
            # Perform agglomerative clustering
            clustering = AgglomerativeClustering(n_clusters=num_clusters)
            clusters = clustering.fit_predict(levels)

            # Identify support and resistance levels
            cluster_centers = []
            for cluster in np.unique(clusters):
                cluster_center = levels[clusters == cluster].mean()
                cluster_centers.append(cluster_center)

            support_level = min(cluster_centers)
            resistance_level = max(cluster_centers)
        else:
            support_level = np.nan
            resistance_level = np.nan

        support_levels.append(support_level)
        resistance_levels.append(resistance_level)

    # Append NaNs for the initial window size
    support_levels = [np.nan] * window_size + support_levels
    resistance_levels = [np.nan] * window_size + resistance_levels

    df['support_level'] = support_levels
    df['resistance_level'] = resistance_levels

    return df



def get_common_indicators() -> list:
    """
    Returns a list of common indicators.

    Returns:
        list: A list of Indicator objects for common indicators.
    """
    common_indicators = [
        SMA(timeperiod=20),
        SMA(timeperiod=50),
        SMA(timeperiod=200),
        EMA(timeperiod=3),
        EMA(timeperiod=5),
        EMA(timeperiod=8),
        EMA(timeperiod=13),
        DM(timeperiod=14),
        FisherTransform(length=9),
        WilliamsR(timeperiod=14),
        RSI(timeperiod=3),
        RSI(timeperiod=5),
        RSI(timeperiod=8),
        RSI(timeperiod=14),
        MACD(fastperiod=12, slowperiod=26, signalperiod=9),
        BBANDS_LOWER(timeperiod=3, nbdevup=2, nbdevdn=2),
        BBANDS_UPPER(timeperiod=3, nbdevup=2, nbdevdn=2),
        BBANDS_LOWER(timeperiod=5, nbdevup=2, nbdevdn=2),
        BBANDS_UPPER(timeperiod=5, nbdevup=2, nbdevdn=2),
        BBANDS_LOWER(timeperiod=8, nbdevup=2, nbdevdn=2),
        BBANDS_UPPER(timeperiod=8, nbdevup=2, nbdevdn=2),
        BBANDS_LOWER(timeperiod=20, nbdevup=2, nbdevdn=2),
        BBANDS_UPPER(timeperiod=20, nbdevup=2, nbdevdn=2),
        ATR(timeperiod=3),
        ATR(timeperiod=5),
        ATR(timeperiod=8),
        ATR(timeperiod=14),
        OBV(),
        DELTA(period=1),
        DELTA(period=3),
        DELTA(period=5),
        DELTA(period=8),
        DELTA(period=13),
    ]
    return common_indicators


def get_common_candlestick_patterns() -> list:
    """
    Returns a list of common candlestick patterns.

    Returns:
        list: A list of CandlestickPattern enums for common candlestick patterns.
    """
    common_candlestick_patterns = [
        CandlestickPattern.CDL3WHITESOLDIERS,
        CandlestickPattern.CDL3BLACKCROWS,
        CandlestickPattern.CDLIDENTICAL3CROWS,
        CandlestickPattern.CDL3LINESTRIKE,
        CandlestickPattern.CDLMORNINGSTAR,
        CandlestickPattern.CDLEVENINGSTAR,
        CandlestickPattern.CDL3OUTSIDE,
        CandlestickPattern.CDLENGULFING,
        CandlestickPattern.CDLBELTHOLD,
        CandlestickPattern.CDLABANDONEDBABY,
        CandlestickPattern.CDLSEPARATINGLINES,
        CandlestickPattern.CDLDOJISTAR,
    ]
    return common_candlestick_patterns



