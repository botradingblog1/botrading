import unittest
from unittest.mock import patch
import pandas as pd
from botrading.data_loaders.fred_economic_data_loader import FredEconomicDataLoader
from botrading.enums import EconomicIndicators


class TestFredEconomicDataLoader(unittest.TestCase):

    def setUp(self):
        self.loader = FredEconomicDataLoader()

    def test_initialization(self):
        self.assertEqual(self.loader._name, "FredEconomicDataLoader")

    @patch('botrading.data_loader.requests.get')
    def test_fetch_fred_data(self, mock_get):
        mock_csv_content = """DATE,GDPC1
2022-01-01,10000
2022-02-01,10100
"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = mock_csv_content

        code_list = ['GDPC1']
        start_date = '2022-01-01'
        end_date = '2022-02-01'

        df = self.loader.fetch_fred_data(code_list, start_date, end_date)

        self.assertEqual(len(df), 2)
        self.assertIn('GDPC1', df.columns)

    def test_translate_symbol_to_name(self):
        symbol = 'GDPC1'
        name = self.loader.translate_symbol_to_name(symbol)
        self.assertEqual(name, 'Gross Domestic Product')

    def test_calculate_deltas(self):
        data = {
            'date': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01'],
            'symbol': ['GDPC1', 'GDPC1', 'GDPC1', 'GDPC1'],
            'value': [10000, 10100, 10200, 10300]
        }
        df = pd.DataFrame(data)
        deltas_df = self.loader.calculate_deltas(df)

        self.assertIn('delta_1m', deltas_df.columns)
        self.assertAlmostEqual(deltas_df.iloc[1]['delta_1m'], 0.01, places=2)

    @patch.object(FredEconomicDataLoader, 'fetch_fred_data')
    def test_fetch_economic_indicators(self, mock_fetch_fred_data):
        mock_data = pd.DataFrame({
            'date': ['2022-01-01', '2022-02-01'],
            'GDPC1': [10000, 10100]
        })
        mock_fetch_fred_data.return_value = mock_data

        start_date = '2022-01-01'
        end_date = '2022-02-01'

        df = self.loader.fetch_economic_indicators(start_date, end_date)

        self.assertEqual(len(df), 2)
        self.assertEqual(df['symbol'][0], 'GDPC1')

    @patch.object(FredEconomicDataLoader, 'fetch_economic_indicators')
    def test_fetch_economic_indicator_deltas(self, mock_fetch_economic_indicators):
        data = {
            'date': ['2022-01-01', '2022-02-01', '2022-03-01', '2022-04-01'],
            'symbol': ['GDPC1', 'GDPC1', 'GDPC1', 'GDPC1'],
            'value': [10000, 10100, 10200, 10300]
        }
        mock_fetch_economic_indicators.return_value = pd.DataFrame(data)

        start_date = '2022-01-01'
        end_date = '2022-04-01'

        deltas_df = self.loader.fetch_economic_indicator_deltas(start_date, end_date)

        self.assertIn('delta_1m', deltas_df.columns)
        self.assertAlmostEqual(deltas_df.iloc[1]['delta_1m'], 0.01, places=2)


if __name__ == '__main__':
    unittest.main()
