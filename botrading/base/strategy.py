import json
from typing import List


class Strategy:
    """
    Represents a trading strategy composed of multiple indicators and rules.
    """

    def __init__(self, name: str):
        """
        Initializes a new strategy with a given name.

        Parameters:
            name (str): The name of the strategy.
        """
        self.name = name
        self.indicators = []
        self.risk_management_methods = []
        self.rules = []

    def add_indicator(self, indicator):
        """
        Adds an indicator to the strategy.

        Parameters:
            indicator (Indicator): The indicator to add.
        """
        self.indicators.append(indicator)

    def add_risk_management_method(self, risk_management_method):
        """
        Adds an indicator to the strategy.

        Parameters:
            risk_management_method (RiskManagementMethod): The RiskManagementMethod to add.
        """
        self.risk_management_methods.append(risk_management_method)

    def add_rule(self, rule):
        """
        Adds a rule to the strategy.

        Parameters:
            rule (Rule): The rule to add.
        """
        self.rules.append(rule)

    def execute(self, data):
        """
        Executes the strategy on the provided data.

        Parameters:
            data (pd.DataFrame): The market data to execute the strategy on.
        """
        # Execute the strategy logic on the provided data
        pass

    def to_dict(self):
        """
        Converts the strategy to a dictionary.

        Returns:
            dict: A dictionary representation of the strategy.
        """
        return {
            'name': self.name,
            'indicators': [indicator.to_dict() for indicator in self.indicators],
            'rules': [rule.to_dict() for rule in self.rules],
        }

    def save(self, filepath: str):
        """
        Saves the strategy to a JSON file.

        Parameters:
            filepath (str): The path to the JSON file.
        """
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f)

    @staticmethod
    def load(filepath: str):
        """
        Loads a strategy from a JSON file.

        Parameters:
            filepath (str): The path to the JSON file.

        Returns:
            Strategy: The loaded strategy.
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        strategy = Strategy(data['name'])
        for ind_data in data['indicators']:
            strategy.add_indicator(Indicator.from_dict(ind_data))
        for rule_data in data['rules']:
            strategy.add_rule(Rule.from_dict(rule_data))
        return strategy
