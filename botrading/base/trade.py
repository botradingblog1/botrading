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
        if str(data.get('open_order_id')) and str(data.get('open_order_id')) != 'nan':
            order_dict = {
                'id': str(data.get('open_order_id')),
                'created_at': data.get('open_created_at'),
                'side': data.get('open_side'),
                'order_type': data.get('open_order_type'),
                'symbol': str(data.get('open_symbol')),
                'quantity': data.get('open_quantity'),
                'status': data.get('open_status'),
                'filled_quantity': data.get('open_filled_quantity'),
                'filled_avg_price': data.get('open_filled_avg_price'),
                'extended_hours': data.get('open_extended_hours')
            }

            trade.open_order = Order.from_dict(order_dict)

        if str(data.get('close_order_id')) and str(data.get('close_order_id')) != 'nan':
            order_dict = {
                'id': str(data.get('close_order_id')),
                'created_at': data.get('close_created_at'),
                'side': data.get('close_side'),
                'order_type': data.get('close_order_type'),
                'symbol': str(data.get('close_symbol')),
                'quantity': data.get('close_quantity'),
                'status': data.get('close_status'),
                'filled_quantity': data.get('close_filled_quantity'),
                'filled_avg_price': data.get('close_filled_avg_price'),
                'extended_hours': data.get('close_extended_hours')
            }

            trade.close_order = Order.from_dict(order_dict)
        trade.is_closed = bool(data.get('is_closed', False))
        return trade
