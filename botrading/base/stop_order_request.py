from botrading.base.order_request import OrderRequest
from botrading.base.enums import OrderSide, TimeInForce
from typing import Optional
import uuid


class StopOrderRequest(OrderRequest):
    def __init__(self, symbol: str, quantity: float, side: OrderSide, stop_price: float, time_in_force: TimeInForce, limit_price: Optional[float] = None):
        self.client_order_id = str(uuid.uuid4())
        self.symbol = symbol
        self.quantity = quantity
        self.side = side
        self.stop_price = stop_price
        self.time_in_force = time_in_force
        self.limit_price = limit_price

    def to_dict(self):
        return {
            'client_order_id': self.client_order_id,
            'symbol': self.symbol,
            'quantity': self.quantity,
            'side': self.side.value,
            'stop_price': self.stop_price,
            'time_in_force': self.time_in_force.value,
            'limit_price': self.limit_price
        }