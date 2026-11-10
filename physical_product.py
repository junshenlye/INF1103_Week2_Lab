"""PhysicalProduct specialization."""
import math
from product import Product
from can_be_shipped import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if (isinstance(weight, bool) or not isinstance(weight, (int, float))
                or not math.isfinite(weight) or weight <= 0):
            raise ValueError("weight must be finite and positive.")
        self.__weight = weight

    @property
    def weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Weight: {self.weight:g} kg")
        print(f"Shipping cost: ${self.calculate_shipping_cost():.2f}")

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        """Simple lab rule: $5 per kilogram, rounded to cents."""
        return round(self.weight * 5.0, 2)
