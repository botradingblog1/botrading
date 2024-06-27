from uuid import UUID
from datetime import datetime
from typing import Optional
from botrading.base.enums import *


class Order:
    def __init__(self, id: UUID, client_order_id: str, created_at: datetime, side: OrderSide, order_type: OrderType,
                 symbol: str, quantity: float, status: OrderStatus, filled_quantity: float = 0.0, filled_avg_price: Optional[float] = None,
                 extended_hours: bool = False):
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
        self.extended_hours = extended_hours

    def to_dict(self):
        return {
            'id': str(self.id),
            'client_order_id': self.client_order_id,
            'created_at': self.created_at.isoformat(),
            'side': self.side.value,
            'order_type': self.order_type.value,
            'symbol': self.symbol,
            'quantity': self.quantity,
            'status': self.status.value,
            'filled_quantity': self.filled_quantity,
            'filled_avg_price': self.filled_avg_price,
            'extended_hours': self.extended_hours
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=UUID(data['id']),
            client_order_id=data['client_order_id'],
            created_at=datetime.fromisoformat(data['created_at']),
            side=OrderSide(data['side']),
            order_type=OrderType(data['order_type']),
            symbol=data['symbol'],
            quantity=data['quantity'],
            status=OrderStatus(data['status']),
            filled_quantity=data.get('filled_quantity', 0.0),
            filled_avg_price=data.get('filled_avg_price'),
            extended_hours=data.get('extended_hours')
        )
