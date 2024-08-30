import pandas as pd


class CandleSentimentAnalyzer:
    def __init__(self, lookback_period=100, weights=None):
        self.lookback_period = lookback_period
        self.weights = weights if weights else {
            'gap_deviation': 4,
            'body_to_range_deviation': 4,
            'upper_shadow_deviation': 1,
            'lower_shadow_deviation': 1,
            'close_greater_than_open': 3
        }

    def analyze_dataframe(self, df):
        df = df.copy()  # Ensure we are working with a copy of the DataFrame

        # Calculate various percentages and ratios
        df['gap_percent'] = (df['open'] - df['close'].shift(1)) / df['close'].shift(1)
        df['body_to_range_ratio'] = (df['close'] - df['open']).abs() / (df['high'] - df['low'])
        df['upper_shadow_to_range_ratio'] = (df['high'] - df[['open', 'close']].max(axis=1)) / (df['high'] - df['low'])
        df['lower_shadow_to_range_ratio'] = (df[['open', 'close']].min(axis=1) - df['low']) / (df['high'] - df['low'])

        # Close greater than open sentiment
        df['close_greater_than_open'] = df.apply(lambda row: 1 if row['close'] > row['open'] else -1, axis=1)

        # Calculate rolling averages for the lookback period
        df['avg_gap_percent'] = df['gap_percent'].rolling(window=self.lookback_period).mean()
        df['avg_body_to_range_ratio'] = df['body_to_range_ratio'].rolling(window=self.lookback_period).mean()
        df['avg_upper_shadow_to_range_ratio'] = df['upper_shadow_to_range_ratio'].rolling(window=self.lookback_period).mean()
        df['avg_lower_shadow_to_range_ratio'] = df['lower_shadow_to_range_ratio'].rolling(window=self.lookback_period).mean()

        # Fill NaN values with zeros or other appropriate placeholder to maintain DataFrame length
        df['avg_gap_percent'].fillna(0, inplace=True)
        df['avg_body_to_range_ratio'].fillna(0, inplace=True)
        df['avg_upper_shadow_to_range_ratio'].fillna(0, inplace=True)
        df['avg_lower_shadow_to_range_ratio'].fillna(0, inplace=True)

        # Calculate deviations from average
        df['gap_deviation'] = df['gap_percent'] - df['avg_gap_percent']
        df['body_to_range_deviation'] = df.apply(
            lambda row: (row['body_to_range_ratio'] - row['avg_body_to_range_ratio']) * (
                1 if row['open'] < row['close'] else -1), axis=1)
        df['upper_shadow_deviation'] = df.apply(
            lambda row: (row['upper_shadow_to_range_ratio'] - row['avg_upper_shadow_to_range_ratio']) * (
                -1 if row['open'] > row['close'] else 1), axis=1)
        df['lower_shadow_deviation'] = df.apply(
            lambda row: (row['lower_shadow_to_range_ratio'] - row['avg_lower_shadow_to_range_ratio']) * (
                1 if row['open'] > row['close'] else -1), axis=1)

        # Fill NaN deviations with zero to prevent skewing the results
        df.fillna(0, inplace=True)

        # Apply weights and calculate weighted sum of deviations
        metrics = ['gap_deviation', 'body_to_range_deviation', 'upper_shadow_deviation', 'lower_shadow_deviation', 'close_greater_than_open']

        df['weighted_score'] = df.apply(lambda row: sum(self.weights[metric] * row[metric] for metric in metrics), axis=1)

        # Standardize the sentiment score to a scale of 1 to 100 and round to integers
        min_score = df['weighted_score'].min()
        max_score = df['weighted_score'].max()
        if max_score != min_score:
            df['candle_sentiment'] = df['weighted_score'].apply(lambda x: int(round(1 + 99 * (x - min_score) / (max_score - min_score))))
        else:
            df['candle_sentiment'] = 50  # If all scores are the same, assign a neutral sentiment

        return df
