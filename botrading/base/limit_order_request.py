from botrading.base.order_request import OrderRequest
from botrading.base.enums import OrderSide, TimeInForce


class LimitOrderRequest(OrderRequest):
    def __init__(self, symbol: str, quantity: int, side: OrderSide, limit_price: float, time_in_force: TimeInForce):
        self.symbol = symbol
        self.quantity = quantity
        self.side = side
        self.limit_price = limit_price
        self.time_in_force = time_in_force

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'quantity': self.quantity,
            'side': self.side,
            'limit_price': self.limit_price,
            'time_in_force': self.time_in_force
        }

