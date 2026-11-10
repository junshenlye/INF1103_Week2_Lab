"""One product and the rules governing its state."""
import math
from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier) -> None:
        if not isinstance(product_id, str) or not product_id.strip():
            raise ValueError("Product ID must be non-empty text.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name must be non-empty text.")
        if (isinstance(price, bool) or not isinstance(price, (int, float))
                or not math.isfinite(price) or price < 0):
            raise ValueError("Price must be a finite non-negative number.")
        if not isinstance(supplier, Supplier):
            raise TypeError("supplier must be a Supplier object.")
        self.__product_id = product_id.strip().upper()
        self.__name = name.strip()
        self.__price = float(price)
        self.__supplier = supplier
        self.update_stock(stock)

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> None:
        """Replace the stock count, matching Week 5 behavior."""
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Stock must be a non-negative whole number.")
        self.__stock = quantity

    def display_information(self) -> None:
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def display_supplier_information(self) -> None:
        self.supplier.display_information()

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Describe how this product is delivered."""
        pass
