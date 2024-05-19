class Trade:
    """
    Represents a trade executed by the strategy.
    """

    def __init__(self, entry_price: float, quantity: int, exit_price: float = None):
        """
        Initializes a new trade with entry price, quantity, and optional exit price.

        Parameters:
            entry_price (float): The entry price of the trade.
            quantity (int): The quantity of the trade.
            exit_price (float, optional): The exit price of the trade.
        """
        self.entry_price = entry_price
        self.quantity = quantity
        self.exit_price = exit_price

    def close_trade(self, exit_price: float):
        """
        Closes the trade with an exit price.

        Parameters:
            exit_price (float): The exit price of the trade.
        """
        self.exit_price = exit_price

    def profit(self):
        """
        Calculates the profit of the trade.

        Returns:
            float: The profit of the trade.
        """
        if self.exit_price is not None:
            return (self.exit_price - self.entry_price) * self.quantity
        return 0
