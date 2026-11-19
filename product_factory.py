from __future__ import annotations

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from subscription_product import SubscriptionProduct
from supplier import Supplier


PRODUCT_TYPES = ("physical", "digital", "subscription")


class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier,
               extra: int | float | None = None) -> Product:
        """extra is the weight, download size or subscription duration."""
        # The lab CSV does not include these extra fields.
        if product_type == "physical":
            weight = 1.0 if extra is None else extra
            return PhysicalProduct(product_id, name, price, stock_quantity,
                                   supplier, weight)
        elif product_type == "digital":
            download_size = 1.0 if extra is None else extra
            return DigitalProduct(product_id, name, price, stock_quantity,
                                  supplier, download_size)
        elif product_type == "subscription":
            duration = 12 if extra is None else extra
            return SubscriptionProduct(product_id, name, price, stock_quantity,
                                       supplier, duration)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
