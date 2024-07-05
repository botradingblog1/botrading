from uuid import UUID
from datetime import datetime
from typing import Optional
from botrading.base.enums import OrderSide, OrderType, OrderStatus


class Order:
    def __init__(self, id: UUID, client_order_id: str, created_at: datetime, side: OrderSide, order_type: OrderType,
                 symbol: str, quantity: float, status: OrderStatus, filled_quantity: float = 0.0, filled_avg_price: Optional[float] = None,
                 stop_price: Optional[float] = None, limit_price: Optional[float] = None, extended_hours: bool = False):
        self.id = id
        self.client_order_id = client_order_id
        self.created_at = created_at
        self.side = side
        self.order_type = order_type
        self.symbol = symbol
        self.quantity = quantity
        self.status = status
        self.filled_quantity = filled_quantity
        self.filled_avg_price = filled_avg_price
        self.stop_price = stop_price
        self.limit_price = limit_price
        self.extended_hours = extended_hours

    def to_dict(self):
        return {
            'id': str(self.id) if self.id else None,
            'client_order_id': self.client_order_id if self.client_order_id else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'side': self.side.value if self.side else None,
            'order_type': self.order_type.value if self.order_type else None,
            'symbol': self.symbol if self.symbol else None,
            'quantity': self.quantity if self.quantity else 0.0,
            'status': self.status.value if self.status else None,
            'filled_quantity': self.filled_quantity if self.filled_quantity else 0.0,
            'filled_avg_price': self.filled_avg_price if self.filled_avg_price else 0.0,
            'stop_price': self.stop_price if self.stop_price else 0.0,
            'limit_price': self.limit_price if self.limit_price else 0.0,
            'extended_hours': self.extended_hours if self.extended_hours else False
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=str(data['id']) if 'id' in data and data['id'] is not None else None,
            client_order_id=data['client_order_id'] if 'client_order_id' in data and data['client_order_id'] is not None else None,
            created_at=data['created_at'] if 'created_at' in data and data['created_at'] is not None else None,
            side=OrderSide(data['side'].lower()) if 'side' in data and data['side'] is not None else None,
            order_type=OrderType(data['order_type'].lower()) if 'order_type' in data and data['order_type'] is not None else None,
            symbol=data['symbol'] if 'symbol' in data and data['symbol'] is not None else None,
            quantity=data['quantity'] if 'quantity' in data and data['quantity'] is not None else 0.0,
            status=OrderStatus(data['status'].lower()) if 'status' in data and data['status'] is not None else None,
            filled_quantity=data['filled_quantity'] if 'filled_quantity' in data and data['filled_quantity'] is not None else 0.0,
            filled_avg_price=data['filled_avg_price'] if 'filled_avg_price' in data and data['filled_avg_price'] is not None else 0.0,
            stop_price=data['stop_price'] if 'stop_price' in data and data[
                'stop_price'] is not None else 0.0,
            limit_price=data['limit_price'] if 'limit_price' in data and data[
                'limit_price'] is not None else 0.0,
            extended_hours=data['extended_hours'] if 'extended_hours' in data and data['extended_hours'] is not None else 0.0,
        )


def is_final_status(status: OrderStatus) -> bool:
    final_statuses = {
        OrderStatus.FILLED,
        OrderStatus.DONE_FOR_DAY,
        OrderStatus.CANCELED,
        OrderStatus.EXPIRED,
        OrderStatus.REPLACED,
        OrderStatus.REJECTED
    }
    return status in final_statuses


def is_pending_status(status: OrderStatus) -> bool:
    pending_statuses = {
        OrderStatus.NEW,
        OrderStatus.PARTIALLY_FILLED,
        OrderStatus.PENDING_CANCEL,
        OrderStatus.PENDING_REPLACE,
        OrderStatus.PENDING_REVIEW,
        OrderStatus.PENDING_NEW,
        OrderStatus.ACCEPTED,
        OrderStatus.ACCEPTED_FOR_BIDDING,
        OrderStatus.STOPPED,
        OrderStatus.SUSPENDED,
        OrderStatus.CALCULATED,
        OrderStatus.HELD
    }
    return status in pending_statuses