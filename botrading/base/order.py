from uuid import UUID
from datetime import datetime
from typing import Optional
from botrading.base.enums import OrderSide, OrderType, OrderStatus


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
            id=str(data['id']) if 'id' in data and data['id'] is not None else None,
            client_order_id=data['client_order_id'] if 'client_order_id' in data and data['client_order_id'] is not None else None,
            created_at=datetime.fromisoformat(data['created_at']) if 'created_at' in data and data['created_at'] is not None else None,
            side=OrderSide(data['side'].lower()) if 'side' in data and data['side'] is not None else None,
            order_type=OrderType(data['order_type'].lower()) if 'order_type' in data and data['order_type'] is not None else None,
            symbol=data['symbol'] if 'symbol' in data and data['symbol'] is not None else None,
            quantity=data['quantity'] if 'quantity' in data and data['quantity'] is not None else 0.0,
            status=OrderStatus(data['status']) if 'status' in data and data['status'] is not None else None,
            filled_quantity=data['filled_quantity'] if 'filled_quantity' in data and data['filled_quantity'] is not None else 0.0,
            filled_avg_price=data['filled_avg_price'] if 'filled_avg_price' in data and data['filled_avg_price'] is not None else 0.0,
            extended_hours=data['extended_hours'] if 'extended_hours' in data and data['extended_hours'] is not None else 0.0,
        )
