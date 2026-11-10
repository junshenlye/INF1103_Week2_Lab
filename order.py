"""Customer order that owns and manages its OrderLine objects."""
from __future__ import annotations
from order_line import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str) -> None:
        if not isinstance(order_id, str) or not order_id.strip():
            raise ValueError("Order ID must be non-empty text.")
        self.__order_id = order_id.strip().upper()
        self.__order_lines: list[OrderLine] = []

    @property
    def order_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        """Expose a snapshot without allowing direct collection changes."""
        return tuple(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:
        self.__order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, product_id: str) -> OrderLine | None:
        if not isinstance(product_id, str):
            raise TypeError("Product ID must be text.")
        target = product_id.strip().upper()
        for index, order_line in enumerate(self.__order_lines):
            if order_line.product.product_id == target:
                return self.__order_lines.pop(index)
        return None

    def calculate_total(self) -> float:
        return sum(
            (line.calculate_subtotal() for line in self.__order_lines),
            start=0.0,
        )

    def display_information(self) -> None:
        print(f"\nOrder {self.order_id}")
        if not self.__order_lines:
            print("No order lines.")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(f"Order total: ${self.calculate_total():.2f}")
