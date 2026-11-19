"""Central product construction for the menu, JSON and CSV loaders."""
from __future__ import annotations
from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from subscription_product import SubscriptionProduct
from supplier import Supplier


PRODUCT_TYPES = {
    "physical": (PhysicalProduct, "weight", "Weight (kg): ", float, 1.0),
    "digital": (DigitalProduct, "download_size", "Download size (MB): ", float, 1.0),
    "subscription": (SubscriptionProduct, "duration_months", "Duration (months): ", int, 12),
}


class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier,
               extra: int | float | None = None) -> Product:
        if not isinstance(product_type, str) or product_type not in PRODUCT_TYPES:
            raise ValueError(f"Unknown product type: {product_type}")
        cls, _, _, _, default = PRODUCT_TYPES[product_type]
        # The supplied five-column CSV omits subtype-specific data. These
        # documented lab defaults keep the existing constructors intact.
        return cls(product_id, name, price, stock_quantity, supplier,
                   default if extra is None else extra)
