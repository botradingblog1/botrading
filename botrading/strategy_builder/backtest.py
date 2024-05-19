class Backtest:
    """
    Represents a backtesting engine for evaluating strategies on historical data.
    """

    def __init__(self, strategy, data):
        """
        Initializes a new backtest with a strategy and historical data.

        Parameters:
            strategy (Strategy): The strategy to be tested.
            data (pd.DataFrame): The historical market data for backtesting.
        """
        self.strategy = strategy
        self.data = data

    def run(self):
        """
        Runs the backtest by executing the strategy on the historical data.
        """
        # Execute the strategy on the historical data
        self.strategy.execute(self.data)
        # Generate performance metrics
        pass
