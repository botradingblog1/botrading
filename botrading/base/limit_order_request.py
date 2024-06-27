from botrading.base.order_request import OrderRequest
from botrading.base.enums import OrderSide, TimeInForce


class LimitOrderRequest(OrderRequest):
    def __init__(self, client_order_id: str, symbol: str, quantity: int, side: OrderSide, limit_price: float, time_in_force: TimeInForce):
        self.client_order_id = client_order_id
        self.symbol = symbol
        self.quantity = quantity
        self.side = side
        self.limit_price = limit_price
        self.time_in_force = time_in_force

    def to_dict(self):
        return {
            'client_order_id': client_order_id,
            'symbol': self.symbol,
            'quantity': self.quantity,
            'side': self.side,
            'limit_price': self.limit_price,
            'time_in_force': self.time_in_force
        }

