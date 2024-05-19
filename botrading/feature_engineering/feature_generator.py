import pandas as pd
import pandas_ta as ta
import talib
from ..strategy_builder.indicator import Indicator
from ..utils.df_utils import check_ohlc_dataframe
from ..enums import *

class FeatureGenerator:
    """
    FeatureGenerator class to add features to an OHLC data frame using pandas_ta and TA-Lib.

    # Usage:
    # Define a list of indicators, including lags and deltas
    indicators = [
        Indicator(name=IndicatorType.RSI, params={'timeperiod': 14}),
        Indicator(name=IndicatorType.MACD, params={'fastperiod': 12, 'slowperiod': 26, 'signalperiod': 9}),
        Indicator(name=IndicatorType.SMA, params={'timeperiod': 30}),
        Indicator(name=IndicatorType.LAG, params={'period': 1}),
        Indicator(name=IndicatorType.LAG, params={'period': 2}),
        Indicator(name=IndicatorType.DELTA, params={'period': 1}),
        Indicator(name=IndicatorType.DELTA, params={'period': 2})
    ]

    # Initialize FeatureGenerator
    feature_generator = FeatureGenerator(indicators)

    # Add features to the data frame
    enhanced_df = feature_generator.add_features(ohlcv_data)
    """

    def __init__(self):
        pass

    def add_indicators(self, df: pd.DataFrame, indicators) -> pd.DataFrame:
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
            df = self._apply_indicator(df, indicator)
        return df

    def _apply_indicator(self, df: pd.DataFrame, indicator: Indicator) -> pd.DataFrame:
        func = getattr(self, f"_add_{indicator.name.lower()}", None)
        if func:
            return func(df, **indicator.params)
        else:
            raise ValueError(f"Indicator {indicator.name} not supported.")

    def _add_lag(self, df: pd.DataFrame, period: int) -> pd.DataFrame:
        for column in df.columns:
            if column not in ['date', 'open', 'high', 'low', 'close', 'volume']:
                df[f"{column}_lag{period}"] = df[column].shift(period)
        return df

    def _add_delta(self, df: pd.DataFrame, period: int) -> pd.DataFrame:
        for column in df.columns:
            if column not in ['date', 'open', 'high', 'low', 'close', 'volume']:
                df[f"{column}_delta{period}"] = df[column].pct_change(periods=period)
        return df

    def _add_ao(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['AO'] = ta.ao(df['high'], df['low'], **params)
        return df

    def _add_apo(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['APO'] = talib.APO(df['close'], **params)
        return df

    def _add_macd(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['MACD'], df['MACD_signal'], df['MACD_hist'] = talib.MACD(df['close'], **params)
        return df

    def _add_rsi(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['RSI'] = talib.RSI(df['close'], **params)
        return df

    def _add_bop(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['BOP'] = talib.BOP(df['open'], df['high'], df['low'], df['close'])
        return df

    def _add_cci(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['CCI'] = talib.CCI(df['high'], df['low'], df['close'], **params)
        return df

    def _add_cmo(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['CMO'] = talib.CMO(df['close'], **params)
        return df

    def _add_dm(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['+DI'], df['-DI'] = talib.PLUS_DM(df['high'], df['low'], **params), talib.MINUS_DM(df['high'], df['low'], **params)
        return df

    def _add_mom(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['MOM'] = talib.MOM(df['close'], **params)
        return df

    def _add_ppo(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['PPO'] = talib.PPO(df['close'], **params)
        return df

    def _add_roc(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['ROC'] = talib.ROC(df['close'], **params)
        return df

    def _add_trix(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['TRIX'] = talib.TRIX(df['close'], **params)
        return df

    def _add_uo(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['UO'] = talib.ULTOSC(df['high'], df['low'], df['close'], **params)
        return df

    def _add_williamsr(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['WILLIAMSR'] = talib.WILLR(df['high'], df['low'], df['close'], **params)
        return df

    def _add_fisher_transform(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        temp_df = ta.fisher(high=df['high'], low=df['low'], **params)
        length = params.get('length', 9)
        df['FISHER_TRANSFORM'] = temp_df[f'FISHERT_{length}_1']
        df['FISHER_TRANSFORM_SIGNAL'] = temp_df[f'FISHERTs_{length}_1']
        return df

    def _add_adx(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['ADX'] = talib.ADX(df['high'], df['low'], df['close'], **params)
        return df

    def _add_aroon(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['AROON_down'], df['AROON_up'] = talib.AROON(df['high'], df['low'], **params)
        return df

    def _add_psar(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['PSAR'] = talib.SAR(df['high'], df['low'], **params)
        return df

    def _add_low_bband(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['LOW_BBAND'], _, _ = talib.BBANDS(df['close'], **params)
        return df

    def _add_high_bband(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        _, _, df['HIGH_BBAND'] = talib.BBANDS(df['close'], **params)
        return df

    def _add_low_donchian(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['LOW_DONCHIAN'] = ta.donchian(df['high'], df['low'], lower=True, **params)
        return df

    def _add_high_donchian(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['HIGH_DONCHIAN'] = ta.donchian(df['high'], df['low'], upper=True, **params)
        return df

    def _add_low_kc(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['LOW_KC'] = ta.kc(df['high'], df['low'], df['close'], lower=True, **params)
        return df

    def _add_high_kc(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['HIGH_KC'] = ta.kc(df['high'], df['low'], df['close'], upper=True, **params)
        return df

    def _add_ad(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['AD'] = ta.ad(df['high'], df['low'], df['close'], df['volume'])
        return df

    def _add_obv(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['OBV'] = talib.OBV(df['close'], df['volume'])
        return df

    def _add_cmf(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['CMF'] = ta.cmf(df['high'], df['low'], df['close'], df['volume'], **params)
        return df

    def _add_mfi(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['MFI'] = talib.MFI(df['high'], df['low'], df['close'], df['volume'], **params)
        return df

    def _add_sma(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['SMA'] = talib.SMA(df['close'], **params)
        return df

    def _add_ema(self, df: pd.DataFrame, **params) -> pd.DataFrame:
        df['EMA'] = talib.EMA(df['close'], **params)
        return df


    def _add_candlestick_patterns(self, df: pd.DataFrame, candlestick_patterns ) -> pd.DataFrame:
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
            df = self._apply_candlestick_pattern(df, pattern)
        return df


    def _apply_candlestick_pattern(self, df: pd.DataFrame, pattern: CandlestickPattern) -> pd.DataFrame:
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

    def get_common_indicators(self) -> list:
        """
        Returns a list of common indicators.

        Returns:
            list: A list of Indicator objects for common indicators.
        """
        common_indicators = [
            Indicator(name=IndicatorType.SMA, params={'timeperiod': 20}),
            Indicator(name=IndicatorType.SMA, params={'timeperiod': 50}),
            Indicator(name=IndicatorType.SMA, params={'timeperiod': 200}),
            Indicator(name=IndicatorType.EMA, params={'timeperiod': 3}),
            Indicator(name=IndicatorType.EMA, params={'timeperiod': 5}),
            Indicator(name=IndicatorType.EMA, params={'timeperiod': 8}),
            Indicator(name=IndicatorType.EMA, params={'timeperiod': 13}),
            Indicator(name=IndicatorType.DM, params={'length': 14}),
            Indicator(name=IndicatorType.FISHER_TRANSFORM, params={'length': 9}),
            Indicator(name=IndicatorType.WILLIAMSR, params={'lbp': 5}),
            Indicator(name=IndicatorType.RSI, params={'timeperiod': 3}),
            Indicator(name=IndicatorType.RSI, params={'timeperiod': 5}),
            Indicator(name=IndicatorType.RSI, params={'timeperiod': 8}),
            Indicator(name=IndicatorType.RSI, params={'timeperiod': 14}),
            Indicator(name=IndicatorType.MACD, params={'fastperiod': 12, 'slowperiod': 26, 'signalperiod': 9}),
            Indicator(name=IndicatorType.BBANDS, params={'timeperiod': 3, 'nbdevup': 2, 'nbdevdn': 2}),
            Indicator(name=IndicatorType.BBANDS, params={'timeperiod': 5, 'nbdevup': 2, 'nbdevdn': 2}),
            Indicator(name=IndicatorType.BBANDS, params={'timeperiod': 8, 'nbdevup': 2, 'nbdevdn': 2}),
            Indicator(name=IndicatorType.BBANDS, params={'timeperiod': 20, 'nbdevup': 2, 'nbdevdn': 2}),
            Indicator(name=IndicatorType.ATR, params={'timeperiod': 3}),
            Indicator(name=IndicatorType.ATR, params={'timeperiod': 5}),
            Indicator(name=IndicatorType.ATR, params={'timeperiod': 8}),
            Indicator(name=IndicatorType.ATR, params={'timeperiod': 14}),
            Indicator(name=IndicatorType.OBV, params={}),
            Indicator(name=IndicatorType.LAG, params={'period: 1'}),
            Indicator(name=IndicatorType.LAG, params={'period: 3'}),
            Indicator(name=IndicatorType.LAG, params={'period: 5'}),
            Indicator(name=IndicatorType.LAG, params={'period: 8'}),
            Indicator(name=IndicatorType.LAG, params={'period: 13'}),
            Indicator(name=IndicatorType.DELTA, params={'period: 1'}),
            Indicator(name=IndicatorType.DELTA, params={'period: 3'}),
            Indicator(name=IndicatorType.DELTA, params={'period: 5'}),
            Indicator(name=IndicatorType.DELTA, params={'period: 8'}),
            Indicator(name=IndicatorType.DELTA, params={'period: 13'}),
        ]
        return common_indicators

    def get_common_candlestick_patterns(self) -> list:
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

    def add_support_resistance_levels(self, df: pd.DataFrame, window_size: int, num_clusters: int) -> pd.DataFrame:
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

            support_levels.append(support_level)
            resistance_levels.append(resistance_level)

        # Append NaNs for the initial window size
        support_levels = [np.nan] * window_size + support_levels
        resistance_levels = [np.nan] * window_size + resistance_levels

        df['support_level'] = support_levels
        df['resistance_level'] = resistance_levels

        return df