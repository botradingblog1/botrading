import uuid
from typing import Optional, Union
from botrading.base.order import Order


class Trade:
    def __init__(self, trade_id=str(uuid.uuid4()), order: Optional[Union[dict, Order]] = None):
        self.trade_id = trade_id
        self.open_order: Optional[Order] = None
        self.close_order: Optional[Order] = None
        self.is_closed = False

        if order:
            if isinstance(order, dict):
                self.update_open_order(Order.from_dict(order))
            else:
                self.update_open_order(order)

    def update_open_order(self, order: Order):
        self.open_order = order
        self.is_closed = False

    def update_close_order(self, order: Order, is_closed: bool):
        self.close_order = order
        self.is_closed = is_closed

    def to_dict(self) -> dict:
        return {
            'trade_id': self.trade_id,
            'open_order': self.open_order.to_dict() if self.open_order else None,
            'close_order': self.close_order.to_dict() if self.close_order else None,
            'is_closed': self.is_closed
        }

    @classmethod
    def from_dict(cls, data: dict):
        trade = cls()
        trade.trade_id = data.get('trade_id')
        if data.get('open_order'):
            trade.open_order = Order.from_dict(data['open_order'])
        if data.get('close_order'):
            trade.close_order = Order.from_dict(data['close_order'])
        trade.is_closed = data.get('is_closed', False)
        return trade
