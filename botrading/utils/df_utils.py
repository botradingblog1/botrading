import pandas as pd

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
