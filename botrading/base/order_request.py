from abc import ABC, abstractmethod


class OrderRequest(ABC):
    @abstractmethod
    def to_dict(self):
        pass



