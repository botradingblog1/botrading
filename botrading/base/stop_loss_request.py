from botrading.base.order_request import OrderRequest
from typing import Optional


class StopLossRequest(OrderRequest):
    def __init__(self, stop_price: float, limit_price: Optional[float] = None):
        self.stop_price = stop_price
        self.limit_price = limit_price

    def to_dict(self):
        return {
            'stop_price': self.stop_price,
            'limit_price': self.limit_price
        }
