from __future__ import annotations
from order_line import OrderLine
from product import Product
from discount_strategy import DiscountStrategy, NoDiscount


class Order:
    def __init__(self, order_id: str,
                 discount: DiscountStrategy | None = None) -> None:
        if not isinstance(order_id, str) or not order_id.strip():
            raise ValueError("Order ID must be non-empty text.")
        self.__order_id = order_id.strip().upper()
        self.__order_lines: list[OrderLine] = []
        self.set_discount(NoDiscount() if discount is None else discount)

    @property
    def discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        if not isinstance(discount, DiscountStrategy):
            raise TypeError("discount must be a DiscountStrategy object.")
        self.__discount = discount

    @property
    def order_id(self) -> str:
        return self.__order_id

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        # Order creates and removes its own lines.
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
        total = 0.0
        for line in self.__order_lines:
            total += line.calculate_subtotal()
        return self.discount.apply(total)

    def display_information(self) -> None:
        print(f"\nOrder {self.order_id}")
        if not self.__order_lines:
            print("No order lines.")
        for order_line in self.__order_lines:
            order_line.display_information()
        print(f"Order total: ${self.calculate_total():.2f}")
