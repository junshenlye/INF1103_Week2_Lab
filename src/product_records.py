from __future__ import annotations

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from product_factory import PRODUCT_TYPES, ProductFactory
from subscription_product import SubscriptionProduct
from supplier import Supplier


def supplier_to_record(supplier: Supplier) -> dict[str, str]:
    return {
        "id": supplier.supplier_id,
        "name": supplier.name,
        "contact_email": supplier.contact_email,
    }


def product_to_record(product: Product) -> dict[str, object]:
    record = {
        "id": product.product_id,
        "name": product.name,
        "price": product.price,
        "stock": product.stock,
        "supplier": supplier_to_record(product.supplier),
    }
    if isinstance(product, PhysicalProduct):
        record["type"] = "physical"
        record["weight"] = product.weight
    elif isinstance(product, DigitalProduct):
        record["type"] = "digital"
        record["download_size"] = product.download_size
    elif isinstance(product, SubscriptionProduct):
        record["type"] = "subscription"
        record["duration_months"] = product.duration_months
    else:
        raise ValueError("Unknown product class.")
    return record


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
    if kind == "physical":
        field = "weight"
    elif kind == "digital":
        field = "download_size"
    else:
        field = "duration_months"
    if not {"id", "name", "price", "stock", "supplier", field} <= record.keys():
        raise ValueError("Missing required product fields.")
    supplier_cache = suppliers if suppliers is not None else {}
    supplier = supplier_from_record(record["supplier"], supplier_cache)
    return ProductFactory.create(kind, record["id"], record["name"], record["price"],
                                 record["stock"], supplier, record[field])
