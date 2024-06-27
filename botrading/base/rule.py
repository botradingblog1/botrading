class Rule:
    """
    Represents a trading rule or condition.
    """

    def __init__(self, description: str, condition):
        """
        Initializes a new rule with a given description and condition.

        Parameters:
            description (str): The description of the rule.
            condition (function): The condition function of the rule.
        """
        self.description = description
        self.condition = condition

    def evaluate(self, data):
        """
        Evaluates the rule condition based on input data.

        Parameters:
            data (pd.DataFrame): The market data to evaluate the rule on.
        """
        # Evaluate the rule condition based on input data
        pass

    def to_dict(self):
        """
        Converts the rule to a dictionary.

        Returns:
            dict: A dictionary representation of the rule.
        """
        return {
            'description': self.description,
            'condition': self.condition
        }

    @staticmethod
    def from_dict(data: dict):
        """
        Creates a rule from a dictionary.

        Parameters:
            data (dict): A dictionary representation of the rule.

        Returns:
            Rule: The created rule.
        """
        return Rule(data['description'], data['condition'])
