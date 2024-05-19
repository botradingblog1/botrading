class Portfolio:
    """
    Represents a portfolio of trades.
    """

    def __init__(self):
        """
        Initializes a new portfolio.
        """
        self.trades = []

    def add_trade(self, trade):
        """
        Adds a trade to the portfolio.

        Parameters:
            trade (Trade): The trade to add.
        """
        self.trades.append(trade)

    def equity_curve(self):
        """
        Calculates and returns the equity curve.

        Returns:
            pd.Series: The equity curve.
        """
        # Calculate and return the equity curve
        pass

    def metrics(self):
        """
        Calculates and returns performance metrics like drawdown, Sharpe ratio, etc.

        Returns:
            dict: A dictionary of performance metrics.
        """
        # Calculate and return performance metrics
        pass
