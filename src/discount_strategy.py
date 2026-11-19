from abc import ABC, abstractmethod
import math


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float) -> None:
        if type(percentage) not in (int, float) or not math.isfinite(percentage):
            raise ValueError("Percentage must be a finite number.")
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
        if type(threshold) not in (int, float) or not math.isfinite(threshold):
            raise ValueError("Threshold must be a finite number.")
        if type(amount) not in (int, float) or not math.isfinite(amount):
            raise ValueError("Amount must be a finite number.")
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
        if total >= self.threshold:
            return max(0.0, total - self.amount)
        return total


class StudentDiscount(PercentageDiscount):
    def __init__(self) -> None:
        super().__init__(5)
