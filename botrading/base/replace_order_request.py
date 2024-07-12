from botrading.base.order_request import OrderRequest
from typing import Optional
from botrading.base.enums import TimeInForce


class ReplaceOrderRequest(OrderRequest):
    def __init__(self,
                 quantity: Optional[int] = None,
                 time_in_force: Optional[TimeInForce] = None,
                 limit_price: Optional[float] = None,
                 stop_price: Optional[float] = None,
                 trail: Optional[float] = None,
                 client_order_id: Optional[str] = None):
        self.quantity = quantity
        self.time_in_force = time_in_force
        self.stop_price = stop_price
        self.limit_price = limit_price
        self.trail = trail
        self.client_order_id = client_order_id

    def to_dict(self):
        return {
            'quantity': self.quantity,
            'time_in_force': self.time_in_force,
            'stop_price': self.stop_price,
            'limit_price': self.limit_price,
            'trail': self.trail,
            'client_order_id': self.client_order_id
        }
