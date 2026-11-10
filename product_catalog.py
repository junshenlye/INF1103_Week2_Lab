"""One extension point for constructors, CLI prompts and JSON fields.

Add a registration here to support a new type without changing the base,
menu, inventory or persistence algorithms.
"""
from __future__ import annotations
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from product import Product
from subscription_product import SubscriptionProduct
from supplier import Supplier

PRODUCT_TYPES = {
    "physical": (PhysicalProduct, "weight", "Weight (kg): ", float),
    "digital": (DigitalProduct, "download_size", "Download size (MB): ", float),
    "subscription": (SubscriptionProduct, "duration_months", "Duration (months): ", int),
}

def create_product(kind: str, product_id: str, name: str, price: float,
                   stock: int, supplier: Supplier,
                   extra: int | float) -> Product:
    if kind not in PRODUCT_TYPES:
        raise ValueError("Unknown product type. Choose " + ", ".join(PRODUCT_TYPES))
    cls, _, _, _ = PRODUCT_TYPES[kind]
    return cls(product_id, name, price, stock, supplier, extra)


def supplier_to_record(supplier: Supplier) -> dict[str, str]:
    return {
        "id": supplier.supplier_id,
        "name": supplier.name,
        "contact_email": supplier.contact_email,
    }


def product_to_record(product: Product) -> dict[str, object]:
    for kind, (cls, field, _, _) in PRODUCT_TYPES.items():
        if type(product) is cls:
            return {"type": kind, "id": product.product_id, "name": product.name,
                    "price": product.price, "stock": product.stock,
                    "supplier": supplier_to_record(product.supplier),
                    field: getattr(product, field)}
    raise ValueError("Unregistered product class.")


def supplier_from_record(record: object,
                         suppliers: dict[str, Supplier]) -> Supplier:
    if not isinstance(record, dict):
        raise ValueError("Each supplier must be a JSON object.")
    if not {"id", "name", "contact_email"} <= record.keys():
        raise ValueError("Missing required supplier fields.")

    supplier = Supplier(record["id"], record["name"], record["contact_email"])
    existing = suppliers.get(supplier.supplier_id)
    if existing is not None:
        if (existing.name != supplier.name
                or existing.contact_email != supplier.contact_email):
            raise ValueError("Supplier details conflict for the same supplier ID.")
        return existing

    suppliers[supplier.supplier_id] = supplier
    return supplier


def product_from_record(record: object,
                        suppliers: dict[str, Supplier] | None = None) -> Product:
    if not isinstance(record, dict):
        raise ValueError("Each product must be a JSON object.")
    kind = record.get("type")
    if not isinstance(kind, str) or kind not in PRODUCT_TYPES:
        raise ValueError("Missing or unknown product type.")
    field = PRODUCT_TYPES[kind][1]
    if not {"id", "name", "price", "stock", "supplier", field} <= record.keys():
        raise ValueError("Missing required product fields.")
    supplier_cache = suppliers if suppliers is not None else {}
    supplier = supplier_from_record(record["supplier"], supplier_cache)
    return create_product(kind, record["id"], record["name"], record["price"],
                          record["stock"], supplier, record[field])
