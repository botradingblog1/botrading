class Indicator:
    """
    Represents a technical indicator.
    """

    def __init__(self, name: str, params: dict):
        """
        Initializes a new indicator with a given name and parameters.

        Parameters:
            name (str): The name of the indicator.
            params (dict): The parameters for the indicator.
        """
        self.name = name
        self.params = params

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
