from ..enums import IndicatorType


class Indicator:
    """
    Represents a technical indicator.
    """

    def __init__(self, name: str, indicator_type: IndicatorType, params: dict, is_price_based: bool =True):
        """
        Initializes a new indicator with a given name and parameters.

        Parameters:
            name (str): The name of the indicator.
            params (dict): The parameters for the indicator.
        """
        self.name = name
        self.indicator_type = indicator_type
        self.params = params
        self.is_price_based = is_price_based
        self.column_name = self._generate_column_name()

    def _generate_column_name(self):
        """
        Generates a column name for the indicator based on its name and parameters.

        Returns:
            str: The generated column name.
        """
        abbreviations = {
            'timeperiod': 'tp',
            'fastperiod': 'fp',
            'slowperiod': 'sp',
            'signalperiod': 'sigp',
            'length': 'len',
            'period': 'p',
            'nbdevup': 'nbu',
            'nbdevdn': 'nbd'
        }

        params_str = "_".join([f"{abbreviations.get(k, k)}{v}" for k, v in self.params.items()])
        return f"{self.name}_{params_str}" if params_str else self.name

    def calculate(self, data):
        """
        Calculates the indicator values based on input data.

        Parameters:
            data (pd.DataFrame): The market data to calculate the indicator on.
        """
        # Calculate indicator values based on input data
        pass

    def to_dict(self):
        """
        Converts the indicator to a dictionary.

        Returns:
            dict: A dictionary representation of the indicator.
        """
        return {
            'name': self.name,
            'params': self.params
        }

    @staticmethod
    def from_dict(data: dict):
        """
        Creates an indicator from a dictionary.

        Parameters:
            data (dict): A dictionary representation of the indicator.

        Returns:
            Indicator: The created indicator.
        """
        return Indicator(data['name'], data['params'])
