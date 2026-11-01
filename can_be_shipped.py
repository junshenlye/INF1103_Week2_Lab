"""Capability contract independent of any product implementation."""
from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Return the shipping cost in dollars."""
        pass
