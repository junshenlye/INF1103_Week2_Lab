"""One product and quantity belonging to an Order."""
from product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(product, Product):
            raise TypeError("product must be a Product object.")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Order quantity must be a positive whole number.")
        self.__product = product
        self.__quantity = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

    def display_information(self) -> None:
        print(f"{self.product.name} x {self.quantity}: "
              f"${self.calculate_subtotal():.2f}")
