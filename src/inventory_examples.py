from pathlib import Path
import tempfile
from unittest.mock import patch

from discount_strategy import BulkDiscount, PercentageDiscount, StudentDiscount
from inventory_storage import load_products
from input_validation import get_positive_float
from inventory import Inventory
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


def main() -> None:
    supplier = Supplier("SUP9", "Lab Supplies", "lab@example.com")
    product = ProductFactory.create("physical", "P250", "Lab Kit", 125, 10, supplier)
    order = Order("O9")
    order.add_order_line(product, 2)
    print(f"No discount: {order.calculate_total():.2f}")
    order.set_discount(BulkDiscount(200, 20))
    print(f"Bulk discount: {order.calculate_total():.2f}")
    order.set_discount(PercentageDiscount(10))
    print(f"Percentage discount: {order.calculate_total():.2f}")
    order.set_discount(StudentDiscount())
    print(f"Student discount: {order.calculate_total():.2f}")

    shared = PercentageDiscount(10)
    first, second = Order("SHARE1", shared), Order("SHARE2", shared)
    print(f"Two orders share one strategy: {first.discount is second.discount}")

    print("\nUnknown product type")
    try:
        ProductFactory.create("service", "S1", "Installation", 30, 5, supplier)
    except ValueError as error:
        print(f"Caught ValueError: {error}")

    print("\nValidation through the Product contract")
    for kind in ("physical", "digital"):
        for price, stock in ((0, 1), (1, -1)):
            try:
                ProductFactory.create(kind, "BAD", "Invalid", price, stock, supplier)
            except ValueError as error:
                print(f"{kind}: {error}")

    print("\nInput sequence: abc, -5, 12.50")
    with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
        value = get_positive_float("Price: ")
    print(f"Returned value: {value:.2f}")

    print("\nCSV import")
    inventory = Inventory()
    load_products(Path(__file__).with_name("products.csv"), inventory, supplier)
    print("Loaded IDs: " + ", ".join(p.product_id for p in inventory.get_products()))
    print("\nMissing CSV")
    # Equivalent to temporarily renaming the CSV, without modifying the source.
    with tempfile.TemporaryDirectory() as directory:
        load_products(Path(directory) / "products.csv", Inventory(), supplier)


if __name__ == "__main__":
    main()
