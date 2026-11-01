"""One extension point for constructors, CLI prompts and JSON fields.

Add a registration here to support a new type without changing the base,
menu, inventory or persistence algorithms.
"""
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from subscription_product import SubscriptionProduct

PRODUCT_TYPES = {
    "physical": (PhysicalProduct, "weight", "Weight (kg): ", float),
    "digital": (DigitalProduct, "download_size", "Download size (MB): ", float),
    "subscription": (SubscriptionProduct, "duration_months", "Duration (months): ", int),
}

def create_product(kind, product_id, name, price, stock, extra):
    if kind not in PRODUCT_TYPES:
        raise ValueError("Unknown product type. Choose " + ", ".join(PRODUCT_TYPES))
    cls, _, _, _ = PRODUCT_TYPES[kind]
    return cls(product_id, name, price, stock, extra)

def product_to_record(product):
    for kind, (cls, field, _, _) in PRODUCT_TYPES.items():
        if type(product) is cls:
            return {"type": kind, "id": product.product_id, "name": product.name,
                    "price": product.price, "stock": product.stock,
                    field: getattr(product, field)}
    raise ValueError("Unregistered product class.")

def product_from_record(record):
    if not isinstance(record, dict):
        raise ValueError("Each product must be a JSON object.")
    kind = record.get("type")
    if not isinstance(kind, str) or kind not in PRODUCT_TYPES:
        raise ValueError("Missing or unknown product type.")
    field = PRODUCT_TYPES[kind][1]
    if not {"id", "name", "price", "stock", field} <= record.keys():
        raise ValueError("Missing required product fields.")
    return create_product(kind, record["id"], record["name"], record["price"], record["stock"], record[field])
