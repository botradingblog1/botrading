import numpy as np
import pandas as pd
import pandas_ta as ta
import talib
from ..enums import *
from ..strategy_builder.indicator import Indicator
from ..utils.df_utils import check_ohlc_dataframe
from sklearn.cluster import AgglomerativeClustering
from ..utils.indicator_utils import *


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


def add_indicators(df: pd.DataFrame, indicators) -> pd.DataFrame:
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
        return func(df, **indicator.params)
    else:
        raise ValueError(f"Indicator {indicator.name} not supported.")


def add_lag(df: pd.DataFrame, period: int) -> pd.DataFrame:
    df[f"close_lag{period}"] = df['close'].shift(period)
    return df


def add_delta(df: pd.DataFrame, period: int) -> pd.DataFrame:
    df[f"close_delta{period}"] = df['close'].pct_change(periods=period)
    return df


def add_ao(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['AO'] = ta.ao(df['high'], df['low'], **params)
    return df


def add_apo(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['APO'] = talib.APO(df['close'], **params)
    return df


def add_macd(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['MACD'], df['MACD_signal'], df['MACD_hist'] = talib.MACD(df['close'], **params)
    return df


def add_rsi(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['RSI'] = talib.RSI(df['close'], **params)
    return df


def add_bop(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['BOP'] = talib.BOP(df['open'], df['high'], df['low'], df['close'])
    return df


def add_cci(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['CCI'] = talib.CCI(df['high'], df['low'], df['close'], **params)
    return df


def add_cmo(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['CMO'] = talib.CMO(df['close'], **params)
    return df


def add_dm(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['DI_POS'], df['DI_NEG'] = talib.PLUS_DM(df['high'], df['low'], **params), talib.MINUS_DM(df['high'], df['low'], **params)
    return df


def add_mom(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['MOM'] = talib.MOM(df['close'], **params)
    return df


def add_ppo(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['PPO'] = talib.PPO(df['close'], **params)
    return df


def add_roc(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['ROC'] = talib.ROC(df['close'], **params)
    return df


def add_trix(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['TRIX'] = talib.TRIX(df['close'], **params)
    return df


def add_uo(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['UO'] = talib.ULTOSC(df['high'], df['low'], df['close'], **params)
    return df


def add_williamsr(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['WILLIAMSR'] = talib.WILLR(df['high'], df['low'], df['close'], **params)
    return df


def add_fisher_transform(df: pd.DataFrame, **params) -> pd.DataFrame:
    temp_df = ta.fisher(high=df['high'], low=df['low'], **params)
    length = params.get('length', 9)
    df['FISHER_TRANSFORM'] = temp_df[f'FISHERT_{length}_1']
    df['FISHER_TRANSFORM_SIGNAL'] = temp_df[f'FISHERTs_{length}_1']
    return df


def add_adx(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['ADX'] = talib.ADX(df['high'], df['low'], df['close'], **params)
    return df


def add_aroon(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['AROON_down'], df['AROON_up'] = talib.AROON(df['high'], df['low'], **params)
    return df


def add_psar(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['PSAR'] = talib.SAR(df['high'], df['low'], **params)
    return df


def add_low_bband(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['LOW_BBAND'], _, _ = talib.BBANDS(df['close'], **params)
    return df


def add_high_bband(df: pd.DataFrame, **params) -> pd.DataFrame:
    _, _, df['HIGH_BBAND'] = talib.BBANDS(df['close'], **params)
    return df


def add_low_donchian(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['LOW_DONCHIAN'] = ta.donchian(df['high'], df['low'], lower=True, **params)
    return df


def add_high_donchian(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['HIGH_DONCHIAN'] = ta.donchian(df['high'], df['low'], upper=True, **params)
    return df


def add_low_kc(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['LOW_KC'] = ta.kc(df['high'], df['low'], df['close'], lower=True, **params)
    return df


def add_high_kc(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['HIGH_KC'] = ta.kc(df['high'], df['low'], df['close'], upper=True, **params)
    return df


def add_ad(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['AD'] = ta.ad(df['high'], df['low'], df['close'], df['volume'])
    return df


def add_obv(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['OBV'] = talib.OBV(df['close'], df['volume'])
    return df


def add_cmf(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['CMF'] = ta.cmf(df['high'], df['low'], df['close'], df['volume'], **params)
    return df


def add_mfi(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['MFI'] = talib.MFI(df['high'], df['low'], df['close'], df['volume'], **params)
    return df


def add_sma(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['SMA'] = talib.SMA(df['close'], **params)
    return df


def add_ema(df: pd.DataFrame, **params) -> pd.DataFrame:
    df['EMA'] = talib.EMA(df['close'], **params)
    return df


def add_bbands(df: pd.DataFrame, **params) -> pd.DataFrame:
    upper, middle, lower = talib.BBANDS(
        df['close'],
        **params
    )
    df[f"BBAND_UPPER_{params['timeperiod']}"] = upper
    df[f"BBAND_MIDDLE_{params['timeperiod']}"] = middle
    df[f"BBAND_LOWER_{params['timeperiod']}"] = lower
    return df

def add_atr(df: pd.DataFrame, **params) -> pd.DataFrame:
    df[f"ATR_{params['timeperiod']}"] = talib.ATR(df['high'], df['low'], df['close'], **params)
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
        BBANDS(timeperiod=3, nbdevup=2, nbdevdn=2),
        BBANDS(timeperiod=5, nbdevup=2, nbdevdn=2),
        BBANDS(timeperiod=8, nbdevup=2, nbdevdn=2),
        BBANDS(timeperiod=20, nbdevup=2, nbdevdn=2),
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
