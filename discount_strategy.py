"""Interchangeable order discounts; Order depends only on DiscountStrategy."""
from abc import ABC, abstractmethod
import math


def _number(value: float, name: str) -> None:
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value)):
        raise ValueError(f"{name} must be a finite number.")


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        """Return the discounted total."""
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        _number(percentage, "Percentage")
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage = float(percentage)

    @property
    def percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float) -> None:
        _number(threshold, "Threshold")
        _number(amount, "Amount")
        if threshold <= 0 or amount < 0:
            raise ValueError("Threshold must be positive and amount non-negative.")
        self.__threshold = float(threshold)
        self.__amount = float(amount)

    @property
    def threshold(self) -> float:
        return self.__threshold

    @property
    def amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        return max(0.0, total - self.amount) if total >= self.threshold else total


class StudentDiscount(PercentageDiscount):
    """Fourth strategy: fixed 5 percent off, without changing Order."""
    def __init__(self) -> None:
        super().__init__(5)
