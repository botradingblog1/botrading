class Security:
    def __init__(self, symbol, name="", sector="", market_price=0, funds_available=0):
        self.symbol = symbol
        self.name = name
        self.sector = sector
        self.market_price = market_price
        self.funds_available = funds_available

    def __repr__(self):
        return (f"Security(symbol={self.symbol}, name={self.name}, sector={self.sector}, "
                f"market_price={self.market_price}, funds_available={self.funds_available})")

    def update_market_price(self, new_price):
        self.market_price = new_price

    def get_market_value(self, quantity):
        return self.market_price * quantity

    def set_funds_available(self, funds):
        self.funds_available = funds

    def get_funds_available(self):
        return self.funds_available
