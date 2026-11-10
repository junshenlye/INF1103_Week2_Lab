"""Manage a collection of Product objects."""
from __future__ import annotations
from product import Product


class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Inventory accepts Product objects only.")
        if self.find_product(product.product_id) is not None:
            raise ValueError("A product with that ID already exists.")
        self.__products.append(product)

    def find_product(self, product_id: str) -> Product | None:
        if not isinstance(product_id, str):
            raise TypeError("Product ID must be text.")
        target = product_id.strip().upper()
        return next((p for p in self.__products if p.product_id == target), None)

    def search_product(self, product_id: str) -> Product | None:
        """Backward-compatible alias used by the existing menu."""
        return self.find_product(product_id)

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def get_products(self) -> tuple[Product, ...]:
        """Expose a snapshot without allowing changes to the collection."""
        return tuple(self.__products)

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
            print(f"Fulfilment: {product.get_fulfilment_info()}")
            product.display_supplier_information()
