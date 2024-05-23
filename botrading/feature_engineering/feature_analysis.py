import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_regression
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import pearsonr
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from ..utils.df_utils import check_ohlc_dataframe
from ..feature_engineering.feature_generation import add_future_returns


def calculate_mutual_information(df: pd.DataFrame, target_column: str) -> pd.DataFrame:
    """
    Calculates mutual information for each feature against future returns.

    Parameters:
        df (pd.DataFrame): The data frame with features and future returns.
        target_column (str): Target column to analyze
    Returns:
        pd.DataFrame: Data frame with mutual information scores.
    """
    _df = df.copy()
    # Check if target column exists
    if target_column not in _df.columns:
        raise Exception(f"Target column {target_column} does not exist in dataframe!")

    target = df[target_column]
    results = []
    for feature in _df.columns:
        if feature not in ['open', 'high', 'low', 'close', 'volume', target_column]:
            mi_score = mutual_info_regression(_df[[feature]], target, discrete_features=False)[0]
            results.append({'feature': feature, 'info_score': mi_score})

    results_df = pd.DataFrame(results)
    results_df.sort_values(by=['info_score'], ascending=[False], inplace=True)

    return results_df


def calculate_random_forest_importance(df: pd.DataFrame, target_column: str,
                                       num_estimators: int = 100) -> pd.DataFrame:
    """
    Calculates random forest importance for each feature against future returns.

    Parameters:
        df (pd.DataFrame): The data frame with features.
        target_column (str): Target column to analyze
        num_estimators (int): Number of trees in the forest.

    Returns:
        pd.DataFrame: Data frame with random forest importance scores.
    """
    _df = df.copy()
    # Check if target column exists
    if target_column not in _df.columns:
        raise Exception(f"Target column {target_column} does not exist in dataframe!")

    target = _df[target_column]
    _df.drop(columns=target_column, inplace=True)
    # Filter out columns that are not features
    #feature_columns = [col for col in df.columns if
    #                   col not in ['open', 'high', 'low', 'close', 'volume', target_column]]
    feature_columns = _df.columns.tolist()
    features = _df[feature_columns]

    # Fit the Random Forest model on all features
    rf = RandomForestRegressor(n_estimators=num_estimators, random_state=42)
    rf.fit(features, target)

    # Get feature importances
    feature_importances = rf.feature_importances_
    results = [{'feature': feature, 'info_score': score} for feature, score in
               zip(feature_columns, feature_importances)]

    results_df = pd.DataFrame(results)
    results_df.sort_values(by=['info_score'], ascending=[False], inplace=True)

    return results_df


def calculate_pearson_correlation(df: pd.DataFrame, target_column: str) -> pd.DataFrame:
    """
    Calculates Pearson correlation for each feature against future returns.

    Parameters:
        df (pd.DataFrame): The data frame with features and future returns.
        target_column (str): Target column to analyze

    Returns:
        pd.DataFrame: Data frame with Pearson correlation scores.
    """
    _df = df.copy()
    # Check if target column exists
    if target_column not in _df.columns:
        raise Exception(f"Target column {target_column} does not exist in dataframe!")

    target = _df[target_column]
    results = []
    for feature in _df.columns:
        if feature not in ['open', 'high', 'low', 'close', 'volume', target_column]:
            corr, _ = pearsonr(_df[feature], target)
            results.append({'feature': feature, 'info_score': corr})

    results_df = pd.DataFrame(results)
    results_df.sort_values(by=['info_score'], ascending=[False], inplace=True)

    return results_df


def get_top_features_by_percentile(mi_scores: pd.DataFrame = None, rf_scores: pd.DataFrame = None, pearson_scores: pd.DataFrame = None, percentile: float = 0.90) -> pd.DataFrame:
    """
    Combines the scores from mutual information, random forest, and Pearson correlation,
    and returns the features that are in the specified percentile for each method.

    Parameters:
        mi_scores (pd.DataFrame, optional): Data frame with mutual information scores.
        rf_scores (pd.DataFrame, optional): Data frame with random forest importance scores.
        pearson_scores (pd.DataFrame, optional): Data frame with Pearson correlation scores.
        percentile (float): The percentile threshold (e.g., 0.90 for 90th percentile).

    Returns:
        pd.DataFrame: Combined data frame with top features for each method.
    """
    combined_top_features_df = pd.DataFrame()

    if mi_scores is not None and not mi_scores.empty:
        mi_threshold = mi_scores['info_score'].quantile(percentile)
        top_mi_features = mi_scores[mi_scores['info_score'] >= mi_threshold]
        combined_top_features_df = pd.concat([combined_top_features_df, top_mi_features])

    if rf_scores is not None and not rf_scores.empty:
        rf_threshold = rf_scores['info_score'].quantile(percentile)
        top_rf_features = rf_scores[rf_scores['info_score'] >= rf_threshold]
        combined_top_features_df = pd.concat([combined_top_features_df, top_rf_features])

    if pearson_scores is not None and not pearson_scores.empty:
        pearson_threshold = pearson_scores['info_score'].quantile(percentile)
        top_pearson_features = pearson_scores[pearson_scores['info_score'] >= pearson_threshold]
        combined_top_features_df = pd.concat([combined_top_features_df, top_pearson_features])

    combined_top_features_df = combined_top_features_df.drop_duplicates().reset_index(drop=True)
    return combined_top_features_df

def calculate_cluster_returns(df: pd.DataFrame, return_percentile: float, lookahead_period: int, num_clusters: int):
    """
    Calculates the average returns for each cluster over the specified number of lookahead periods and returns cluster details.

    Parameters:
        df (pd.DataFrame): The data frame with feature data.
        return_percentile (float): The percentile of returns that will be used to filter future returns.
        lookahead_period (int): The number of lookahead periods for calculating future returns.
        num_clusters (int): The number of clusters to form.

    Returns:
        tuple: DataFrame with clusters and their corresponding average returns,
               DataFrame with clusters and their corresponding features and feature values.
    """
    # Generate future returns
    df = add_future_returns(df, lookahead_period)

    # Filter by the provided percentile
    return_col = f'future_return_{lookahead_period}p'
    threshold = df[return_col].quantile(return_percentile)
    filtered_df = df[df[return_col] >= threshold]

    # Drop future return columns for clustering
    clustering_df = filtered_df.drop(columns=[return_col])

    # Perform clustering
    tsne_df, clustered_data = perform_clustering(clustering_df, num_clusters)

    # Calculate mean return for each cluster
    cluster_returns = clustered_data.groupby('cluster')[return_col].mean().reset_index()

    return cluster_returns, clustered_data


def perform_clustering(df: pd.DataFrame, num_clusters: int) -> pd.DataFrame:
    """
    Performs clustering on the filtered features and returns the clustered data.

    Parameters:
        df (pd.DataFrame): The data frame with features.
        num_clusters (int): The number of clusters to form.

    Returns:
        tuple: Data frame with t-SNE results and cluster assignments, Data frame with cluster assignments.
    """

    # Normalize the filtered features
    scaler = StandardScaler()
    normalized_features = scaler.fit_transform(df)

    # Perform clustering on the filtered features
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    filtered_clusters = kmeans.fit_predict(normalized_features)

    # Assign clusters back to the original data
    df['cluster'] = filtered_clusters

    # Perform t-SNE for dimensionality reduction
    tsne = TSNE(n_components=2, random_state=42)
    tsne_results = tsne.fit_transform(normalized_features)

    tsne_df = pd.DataFrame(tsne_results, columns=['tsne1', 'tsne2'])
    tsne_df['cluster'] = filtered_clusters
    return tsne_df, df
