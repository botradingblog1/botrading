from botrading.base.order_request import OrderRequest
from botrading.base.enums import OrderSide, TimeInForce
from typing import Optional


class MarketOrderRequest(OrderRequest):
    def __init__(self,
                 symbol: str,
                 quantity: int,
                 side: OrderSide,
                 time_in_force: TimeInForce,
                 stop_loss_request: Optional[float] = None):
        self.symbol = symbol
        self.quantity = quantity
        self.side = side
        self.time_in_force = time_in_force
        self.stop_loss_request = stop_loss_request

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'quantity': self.quantity,
            'side': self.side,
            'time_in_force': self.time_in_force,
            'stop_loss_request': self.stop_loss_request.to_dict()
        }