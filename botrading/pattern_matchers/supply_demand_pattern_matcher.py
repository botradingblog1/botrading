import pandas as pd
import numpy as np
import talib as ta
import scipy.signal as signal
from enum import Enum

"""
Identifies Supply/Demand Zones based on the book 'Supply and Demand Trading' by Frank Miller

"""


class SupplyDemandZoneType(Enum):
    SUPPLY_TYPE = "supply"
    DEMAND_TYPE = "demand"


# Container class for supply or demand pattern
class SupplyDemandZone:
    def __init__(self,
                 zone_type: SupplyDemandZoneType,
                 start_index: int,
                 end_index: int,
                 distal_level: float,
                 proxima_level: float,
                 is_continuation_zone: bool = False):
        self.zone_type = zone_type  # 'supply' or 'demand'
        self.start_index = start_index
        self.end_index = end_index
        self.distal_level = distal_level
        self.proxima_level = proxima_level
        self.is_continuation_zone = is_continuation_zone


def find_local_extrema(df: pd.DataFrame, extrema_window: int):
    # Identify local minima and maxima
    local_minima = signal.argrelextrema(df['low'].values, np.less, order=extrema_window)[0]
    local_maxima = signal.argrelextrema(df['high'].values, np.greater, order=extrema_window)[0]
    return local_minima, local_maxima


def has_several_long_tailed_candlesticks(base_candles):
    # Check for several long-tailed candlesticks
    long_tail_count = ((base_candles['high'] - base_candles['low']) > 2.5 * abs(
        base_candles['open'] - base_candles['close'])).sum()
    return long_tail_count > 1


def is_staircase_pattern(base_candles, zone_type):
    # Check for staircase candlesticks
    if zone_type == SupplyDemandZoneType.DEMAND_TYPE:
        return (base_candles['close'] > base_candles['close'].shift(1)).all()
    elif zone_type == SupplyDemandZoneType.SUPPLY_TYPE:
        return (base_candles['close'] < base_candles['close'].shift(1)).all()
    return False


def has_doji_pattern(base_candles):
    # Check for Doji candlesticks only
    doji_count = ta.CDLDOJI(base_candles['open'], base_candles['high'], base_candles['low'], base_candles['close']).sum()
    return doji_count > 1


def is_low_probability_trading_zone(base_candles, zone_type):
    #if has_several_long_tailed_candlesticks(base_candles):
    #    return True
    if is_staircase_pattern(base_candles, zone_type):
        return True
    if has_doji_pattern(base_candles):
        return True
    return False


def has_several_momentum_candles(df: pd.DataFrame, start_index: int, zone_type: SupplyDemandZoneType, min_momentum_candles: int):
    # Check for several momentum candles leading out of the zone
    momentum_count = 0
    for i in range(start_index + 1, len(df)):
        body_length = abs(df['close'].iloc[i] - df['open'].iloc[i])
        candle_length = df['high'].iloc[i] - df['low'].iloc[i]
        if body_length > 0.5 * candle_length:
            momentum_count += 1
        if zone_type == SupplyDemandZoneType.DEMAND_TYPE and df['close'].iloc[i] < df['close'].iloc[start_index]:
            break
        if zone_type == SupplyDemandZoneType.SUPPLY_TYPE and df['close'].iloc[i] > df['close'].iloc[start_index]:
            break
    return momentum_count >= min_momentum_candles


def price_violates_distal_line(df, end_index, distal_level, zone_type):
    if zone_type == SupplyDemandZoneType.DEMAND_TYPE:
        return (df['low'].iloc[end_index:] < distal_level).any()
    elif zone_type == SupplyDemandZoneType.SUPPLY_TYPE:
        return (df['high'].iloc[end_index:] > distal_level).any()
    return False


def find_demand_zones(df, local_minima, min_base_rally_ratio, extrema_window, min_momentum_candles):
    demand_zones = []
    for min_index in local_minima:
        if min_index < extrema_window or min_index > len(df) - extrema_window:
            continue

        base_length = df['close'].iloc[min_index] - df['low'].iloc[min_index]
        rally_length = df['close'].iloc[min_index + extrema_window] - df['close'].iloc[min_index]

        if rally_length > base_length * min_base_rally_ratio:
            base_candles = df.iloc[min_index:min_index + extrema_window + 1]
            # Identify distal and proxima levels using the base candle
            base_candle = df.iloc[min_index]
            distal_level = base_candle['low']
            proxima_level = max(base_candle['open'], base_candle['close'])

            # Check low probability trading zone
            if is_low_probability_trading_zone(base_candles, SupplyDemandZoneType.DEMAND_TYPE):
                continue

            # Check for momentum candles leading out of the zone
            if not has_several_momentum_candles(df, min_index, SupplyDemandZoneType.DEMAND_TYPE, min_momentum_candles):
                continue
                
            # Check for distal level violation
            end_index = min_index + extrema_window
            if price_violates_distal_line(df, end_index, distal_level, SupplyDemandZoneType.DEMAND_TYPE):
                continue

            # Create a Demand zone
            zone = SupplyDemandZone(
                zone_type=SupplyDemandZoneType.DEMAND_TYPE,
                start_index=min_index,
                end_index=end_index,
                distal_level=distal_level,
                proxima_level=proxima_level
            )
            demand_zones.append(zone)
    return demand_zones


def find_supply_zones(df, local_maxima, min_base_rally_ratio, extrema_window, min_momentum_candles):
    supply_zones = []
    for max_index in local_maxima:
        if max_index < extrema_window or max_index > len(df) - extrema_window:
            continue

        base_length = df['high'].iloc[max_index] - df['close'].iloc[max_index]
        rally_length = df['close'].iloc[max_index] - df['close'].iloc[max_index - extrema_window]

        if rally_length > base_length * min_base_rally_ratio:
            base_candles = df.iloc[max_index:max_index + extrema_window + 1]
            # Find distal and proxima levels
            base_candle = df.iloc[max_index]
            distal_level = base_candle['high']
            proxima_level = min(base_candle['open'], base_candle['close'])

            # Check low probably trading zone criteria
            if is_low_probability_trading_zone(base_candles, SupplyDemandZoneType.SUPPLY_TYPE):
                continue

            # Check for momentum candles leading out of the zone
            if not has_several_momentum_candles(df, max_index, SupplyDemandZoneType.SUPPLY_TYPE, min_momentum_candles):
                continue
                
            # Check for distal level violation
            end_index = max_index + extrema_window
            if price_violates_distal_line(df, end_index, distal_level, SupplyDemandZoneType.SUPPLY_TYPE):
                continue

            # Create a Supply zone
            zone = SupplyDemandZone(
                zone_type=SupplyDemandZoneType.SUPPLY_TYPE,
                start_index=max_index,
                end_index=max_index + extrema_window,
                distal_level=distal_level,
                proxima_level=proxima_level
            )
            supply_zones.append(zone)
    return supply_zones


def find_demand_continuation_zones(df, local_minima, local_maxima, min_base_rally_ratio, min_momentum_candles):
    demand_zones = []
    for min_index in local_minima:
        # Find the corresponding previous maximum by iterating backwards through local_maxima
        prev_maxima = [idx for idx in reversed(local_maxima) if idx < min_index]
        if not prev_maxima:
            continue
        max_index = prev_maxima[-1]

        # Analyze the price data between the local maximum and the local minimum
        for i in range(max_index + 1, min_index):
            # Check for disruptions in the trend when a candle closes higher than the previous one
            if df['close'].iloc[i] > df['close'].iloc[i - 1] and df['close'].iloc[i] > df['open'].iloc[i]:
                base_length = df['high'].iloc[i] - df['low'].iloc[i]
                rally_length_down_before = abs(df['close'].iloc[i] - df['close'].iloc[max_index])
                rally_length_up_after = abs(df['close'].iloc[min_index] - df['close'].iloc[i])

                # Check that we have a strong rally before and after the continuation base
                if rally_length_down_before > base_length * min_base_rally_ratio and \
                    rally_length_up_after > base_length * min_base_rally_ratio:
                    base_candle = df.iloc[i]
                    distal_level = base_candle['low']
                    proxima_level = max(base_candle['open'], base_candle['close'])

                    # Check for momentum candles leading out of the zone
                    #if not has_several_momentum_candles(df, min_index, SupplyDemandZoneType.DEMAND_TYPE, 1):
                    #    continue

                    # Check for distal level violation
                    if price_violates_distal_line(df, i, distal_level, SupplyDemandZoneType.DEMAND_TYPE):
                        continue

                    # Create a Demand zone
                    zone = SupplyDemandZone(
                        zone_type=SupplyDemandZoneType.DEMAND_TYPE,
                        start_index=i,
                        end_index=i,
                        distal_level=distal_level,
                        proxima_level=proxima_level,
                        is_continuation_zone=True
                    )
                    demand_zones.append(zone)
    return demand_zones


def find_supply_continuation_zones(df, local_minima, local_maxima, min_base_rally_ratio, min_momentum_candles):
    supply_zones = []
    for max_index in local_maxima:
        # Find the corresponding next minimum by iterating forward through local_minima
        next_minima = [idx for idx in reversed(local_minima) if idx > max_index]
        if not next_minima:
            continue
        min_index = next_minima[-1]

        # Analyze the price data between the local maximum and the local minimum
        for i in range(max_index + 1, min_index):
            # Check for disruptions in the trend when a candle closes lower than the previous one
            if df['close'].iloc[i] < df['close'].iloc[i - 1] and df['close'].iloc[i] < df['open'].iloc[i]:
                base_length = df['high'].iloc[i] - df['low'].iloc[i]
                rally_length_up_before = abs(df['close'].iloc[max_index] - df['close'].iloc[i])
                rally_length_down_after = abs(df['close'].iloc[i] - df['close'].iloc[min_index])

                # Check that we have a strong rally before and after the continuation base
                if rally_length_up_before > base_length * min_base_rally_ratio and \
                    rally_length_down_after > base_length * min_base_rally_ratio:
                    base_candle = df.iloc[i]
                    distal_level = base_candle['high']
                    proxima_level = min(base_candle['open'], base_candle['close'])

                    # Check for momentum candles leading out of the zone
                    #if not has_several_momentum_candles(df, min_index, SupplyDemandZoneType.SUPPLY_TYPE, 1):
                    #    continue

                    # Check for distal level violation
                    if price_violates_distal_line(df, i, distal_level, SupplyDemandZoneType.SUPPLY_TYPE):
                        continue

                    # Create a Supply zone
                    zone = SupplyDemandZone(
                        zone_type=SupplyDemandZoneType.SUPPLY_TYPE,
                        start_index=i,
                        end_index=i,
                        distal_level=distal_level,
                        proxima_level=proxima_level,
                        is_continuation_zone=True
                    )
                    supply_zones.append(zone)
    return supply_zones


class SupplyDemandPatternMatcher:
    def __init__(self,
                 min_base_rally_ratio: float = 1.5,
                 extrema_window: int = 4,
                 min_momentum_candles=2,
                 detect_continuation_patterns: bool = False):
        self.min_base_rally_ratio = min_base_rally_ratio
        self.extrema_window = extrema_window
        self.min_momentum_candles = min_momentum_candles
        self.detect_continuation_patterns = detect_continuation_patterns
        self.supply_zones = []
        self.demand_zones = []

    def detect_supply_demand_zones(self, df):
        self.supply_zones = []
        self.demand_zones = []

        local_minima, local_maxima = find_local_extrema(df, self.extrema_window)

        self.supply_zones = find_supply_zones(df,
                                              local_maxima,
                                              self.min_base_rally_ratio,
                                              self.extrema_window,
                                              self.min_momentum_candles)
        self.demand_zones = find_demand_zones(df,
                                              local_minima,
                                              self.min_base_rally_ratio,
                                              self.extrema_window,
                                              self.min_momentum_candles)

        if self.detect_continuation_patterns:
            supply_continuation_zones = find_supply_continuation_zones(
                                                  df,
                                                  local_minima,
                                                  local_maxima,
                                                  self.min_base_rally_ratio,
                                                  self.min_momentum_candles)
            self.supply_zones = self.supply_zones + supply_continuation_zones

            demand_continuation_zones = find_demand_continuation_zones(
                                                  df,
                                                  local_minima,
                                                  local_maxima,
                                                  self.min_base_rally_ratio,
                                                  self.min_momentum_candles)
            self.demand_zones = self.demand_zones + demand_continuation_zones

        return self.supply_zones, self.demand_zones
