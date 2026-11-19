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
        for product in self.__products:
            if product.product_id == target:
                return product
        return None

    def search_product(self, product_id: str) -> Product | None:
        return self.find_product(product_id)

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def get_products(self) -> tuple[Product, ...]:
        # Return a copy so callers cannot change the inventory list.
        return tuple(self.__products)

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
            print(f"Fulfilment: {product.get_fulfilment_info()}")
            product.display_supplier_information()
