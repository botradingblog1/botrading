import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_regression
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import pearsonr
from ..enums import StatsMethod


class PeerFinder:
    """
    PeerFinder class to find peer stocks based on OHLCV data by comparing stock pairs
    using Pearson correlation, Mutual Information, and Random Forest information score.
    """

    def __init__(self, price_data):
        """
        Initializes the PeerFinder with price data.

        Parameters:
            price_data (dict): Dictionary of stock symbols and their corresponding price dataframes (date, open, high, low, close, volume).
        """
        self.price_data = price_data
        self.return_data = self.calculate_returns()

    def calculate_returns(self):
        """
        Calculates the return percentages for each stock.

        Returns:
            dict: Dictionary of stock symbols and their corresponding return percentages.
        """
        return_data = {}
        for symbol, df in self.price_data.items():
            df['return'] = df['close'].pct_change()
            return_data[symbol] = df['return'].dropna()
        return return_data

    def shift_returns(self, returns, periods):
        """
        Shifts the return series by a given number of periods.

        Parameters:
            returns (pd.Series): The return series.
            periods (int): The number of periods to shift.

        Returns:
            pd.Series: The shifted return series.
        """
        return returns.shift(-periods).dropna()

    def find_peers(self, symbol, method=ComparisonMethod.PEARSON, num_top_peers=5, max_periods=10):
        """
        Finds the top peer stocks for a given symbol using the specified method.

        Parameters:
            symbol (str): The stock symbol to find peers for.
            method (ComparisonMethod): The method to use for comparison (ComparisonMethod.PEARSON, ComparisonMethod.MUTUAL_INFO, ComparisonMethod.RANDOM_FOREST). Defaults to ComparisonMethod.PEARSON.
            num_top_peers (int): The number of top peers to return. Defaults to 5.
            max_periods (int): The maximum number of periods to analyze. Defaults to 10.

        Returns:
            pd.DataFrame: DataFrame with top peers for each shift period.
        """
        if method == ComparisonMethod.PEARSON:
            return self._find_peers_by_pearson(symbol, num_top_peers, max_periods)
        elif method == ComparisonMethod.MUTUAL_INFO:
            return self._find_peers_by_mutual_info(symbol, num_top_peers, max_periods)
        elif method == ComparisonMethod.RANDOM_FOREST:
            return self._find_peers_by_random_forest(symbol, num_top_peers, max_periods)
        else:
            raise ValueError("Invalid method. Choose from ComparisonMethod.PEARSON, ComparisonMethod.MUTUAL_INFO, ComparisonMethod.RANDOM_FOREST.")

    def _find_peers_by_pearson(self, symbol, num_top_peers, max_periods):
        """
        Finds peers using Pearson correlation.

        Parameters:
            symbol (str): The stock symbol to find peers for.
            num_top_peers (int): The number of top peers to return.
            max_periods (int): The maximum number of periods to analyze.

        Returns:
            pd.DataFrame: DataFrame with top peers for each shift period using Pearson correlation.
        """
        target_returns = self.return_data[symbol]
        results = []

        for period in range(1, max_periods + 1):
            future_returns = self.shift_returns(target_returns, period)
            scores = []

            for peer_symbol, peer_returns in self.return_data.items():
                if peer_symbol != symbol:
                    score = self._pearson_correlation(peer_returns, future_returns)
                    scores.append((period, peer_symbol, score))

            scores.sort(key=lambda x: x[2], reverse=True)
            results.extend(scores[:num_top_peers])

        return pd.DataFrame(results, columns=['period', 'symbol', 'score'])

    def _find_peers_by_mutual_info(self, symbol, num_top_peers, max_periods):
        """
        Finds peers using Mutual Information.

        Parameters:
            symbol (str): The stock symbol to find peers for.
            num_top_peers (int): The number of top peers to return.
            max_periods (int): The maximum number of periods to analyze.

        Returns:
            pd.DataFrame: DataFrame with top peers for each shift period using Mutual Information.
        """
        target_returns = self.return_data[symbol]
        results = []

        for period in range(1, max_periods + 1):
            future_returns = self.shift_returns(target_returns, period)
            scores = []

            for peer_symbol, peer_returns in self.return_data.items():
                if peer_symbol != symbol:
                    score = self._mutual_information(peer_returns, future_returns)
                    scores.append((period, peer_symbol, score))

            scores.sort(key=lambda x: x[2], reverse=True)
            results.extend(scores[:num_top_peers])

        return pd.DataFrame(results, columns=['period', 'symbol', 'score'])

    def _find_peers_by_random_forest(self, symbol, num_top_peers, max_periods, num_estimators=100):
        """
        Finds peers using Random Forest information score.

        Parameters:
            symbol (str): The stock symbol to find peers for.
            num_top_peers (int): The number of top peers to return.
            max_periods (int): The maximum number of periods to analyze.
            num_estimators (int): The number of estimators for the Random Forest regressor. Defaults to 100.

        Returns:
            pd.DataFrame: DataFrame with top peers for each shift period using Random Forest information score.
        """
        target_returns = self.return_data[symbol]
        results = []

        for period in range(1, max_periods + 1):
            future_returns = self.shift_returns(target_returns, period)
            scores = []

            for peer_symbol, peer_returns in self.return_data.items():
                if peer_symbol != symbol:
                    score = self._random_forest_information(peer_returns, future_returns, num_estimators)
                    scores.append((period, peer_symbol, score))

            scores.sort(key=lambda x: x[2], reverse=True)
            results.extend(scores[:num_top_peers])

        return pd.DataFrame(results, columns=['period', 'symbol', 'score'])

    def _pearson_correlation(self, returns1, returns2):
        """
        Calculates the Pearson correlation between two return series.

        Parameters:
            returns1 (pd.Series): The first return series.
            returns2 (pd.Series): The second return series.

        Returns:
            float: The Pearson correlation coefficient.
        """
        common_index = returns1.index.intersection(returns2.index)
        if len(common_index) > 0:
            return pearsonr(returns1.loc[common_index], returns2.loc[common_index])[0]
        return -1

    def _mutual_information(self, returns1, returns2):
        """
        Calculates the mutual information between two return series.

        Parameters:
            returns1 (pd.Series): The first return series.
            returns2 (pd.Series): The second return series.

        Returns:
            float: The mutual information score.
        """
        common_index = returns1.index.intersection(returns2.index)
        if len(common_index) > 0:
            return mutual_info_regression(returns1.loc[common_index].values.reshape(-1, 1), returns2.loc[common_index].values)[0]
        return 0

    def _random_forest_information(self, returns1, returns2, num_estimators=100):
        """
        Calculates the importance score using a Random Forest regressor between two return series.

        Parameters:
            returns1 (pd.Series): The first return series.
            returns2 (pd.Series): The second return series.
            num_estimators (int): The number of estimators for the Random Forest regressor. Defaults to 100.

        Returns:
            float: The Random Forest importance score.
        """
        common_index = returns1.index.intersection(returns2.index)
        if len(common_index) > 0:
            rf = RandomForestRegressor(n_estimators=num_estimators)
            rf.fit(returns1.loc[common_index].values.reshape(-1, 1), returns2.loc[common_index].values)
            return rf.feature_importances_[0]
        return 0
