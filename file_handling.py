"""Translate JSON records to inventory objects at the file boundary."""
from __future__ import annotations
import json
from pathlib import Path
from inventory import Inventory
from product_catalog import product_from_record, product_to_record
from supplier import Supplier


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
