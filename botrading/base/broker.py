from abc import ABC, abstractmethod
from typing import List, Optional


class Broker(ABC):
    # Broker interface for broker implementations
    @abstractmethod
    def get_positions(self) -> list:
        pass

    @abstractmethod
    def get_positions_by_symbol(self, symbol: str):
        pass

    @abstractmethod
    def get_available_cash(self) -> float:
        pass

    @abstractmethod
    def submit_order(self, request: dict):
        pass

    @abstractmethod
    def get_current_ask_price(self, symbol: str) -> float:
        pass

    @abstractmethod
    def get_bid_ask_spread(self, symbol: str) -> float:
        pass

    @abstractmethod
    def get_open_orders_by_symbol(self, symbol: str) -> bool:
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: str):
        pass
