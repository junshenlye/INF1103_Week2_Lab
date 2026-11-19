from __future__ import annotations
import json
import csv
from pathlib import Path
from inventory import Inventory
from product_records import product_from_record, product_to_record
from supplier import Supplier
from product_factory import ProductFactory


def load_products(path: str | Path, inventory: Inventory,
                  supplier: Supplier) -> None:
    """Import valid CSV rows, reporting each rejected row without aborting."""
    loaded = 0
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            rows = csv.reader(file)
            next(rows, None)  # Skip the header.
            for row in rows:
                try:
                    kind, product_id, name, price, stock = row
                    product = ProductFactory.create(
                        kind, product_id, name, float(price), int(stock), supplier
                    )
                    inventory.add_product(product)
                except ValueError as error:
                    print(f"Row {rows.line_num} skipped: {error}")
                else:
                    loaded += 1
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def load_inventory(file_path: str | Path) -> Inventory:
    path = Path(file_path)
    inventory = Inventory()
    if not path.exists():
        print(f"{path.name} not found. Starting with an empty inventory.")
        return inventory
    records = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise ValueError("Inventory JSON must contain a list.")
    suppliers: dict[str, Supplier] = {}
    for record in records:
        inventory.add_product(product_from_record(record, suppliers))
    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory: Inventory, file_path: str | Path) -> None:
    path = Path(file_path)
    records = [product_to_record(p) for p in inventory.get_products()]
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(records, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    temporary.replace(path)
    print(f"Inventory saved successfully to {path.name}.")
