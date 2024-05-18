import numpy as np
import pandas as pd
import pywt


class PriceDataProcessor:
    """
    Performs data cleanup and denoising.
    """

    def __init__(self):
        self._name = "PriceDataProcessor"

    def denoise_series(self, series_values, wavelet, scale):
        """
        Denoise price data using Discrete Wavelet Transform (DWT).

        Parameters:
            series_values (np.ndarray): Series values to denoise.
            wavelet (str): Wavelet name.
            scale (float): Threshold scale.

        Returns:
            np.ndarray: Denoised series values.
        """
        # Perform DWT: Decompose prices into wavelet coefficients
        coefficients = pywt.wavedec(series_values, wavelet, mode='per')

        # Calculate threshold level based on scale
        threshold = scale * np.max(series_values)

        # Apply soft thresholding to all coefficients except the first approximation coefficient
        coefficients[1:] = [pywt.threshold(i, value=threshold, mode='soft') for i in coefficients[1:]]

        # Reconstruct prices from the thresholded wavelet coefficients
        denoised_prices = pywt.waverec(coefficients, wavelet, mode='per')

        # Ensure the length of the denoised prices matches the original series length
        if len(denoised_prices) > len(series_values):
            denoised_prices = denoised_prices[:len(series_values)]
        elif len(denoised_prices) < len(series_values):
            denoised_prices = np.pad(denoised_prices, (0, len(series_values) - len(denoised_prices)), 'edge')

        return denoised_prices

    def perform_denoising(self, prices_df, wavelet="db6", scale=0.02):
        """
        Helper function to denoise numeric columns in the DataFrame.

        Parameters:
            prices_df (pd.DataFrame): DataFrame with price data.
            wavelet (str): PyWavelet wavelet name
            scale (float): Scale for Wavelet Transform

        Returns:
            pd.DataFrame: DataFrame with denoised price data.
        """

        for column in prices_df.columns:
            if pd.api.types.is_numeric_dtype(prices_df[column]):
                prices_df[column] = self.denoise_series(prices_df[column].values, wavelet, scale)

        return prices_df

    def perform_cleanup(self, df):
        """
        Fill missing data and ensure numeric columns are in the correct format.

        Parameters:
            df (pd.DataFrame): DataFrame with price data.

        Returns:
            pd.DataFrame: Cleaned DataFrame.
        """
        # Fill missing data
        df.fillna(method='ffill', inplace=True)
        df.fillna(0, inplace=True)

        # Ensure numeric columns have a numeric format
        for column in df.columns:
            if pd.api.types.is_numeric_dtype(df[column]):
                df[column] = pd.to_numeric(df[column], errors='coerce')

        return df
