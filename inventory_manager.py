"""Week 5 inventory manager - phase 2: load product data from JSON."""

import json
import os
from pathlib import Path

INVENTORY_FILE = Path(os.environ.get("INVENTORY_FILE", "inventory.json"))


def validate_inventory(data):
    """Return validated product dictionaries or raise ValueError."""
    if not isinstance(data, list):
        raise ValueError("inventory must be a list")

    validated = []
    seen_ids = set()
    for product in data:
        if not isinstance(product, dict):
            raise ValueError("each product must be a dictionary")

        required = {"id", "name", "price", "stock"}
        if not required.issubset(product):
            raise ValueError("a product is missing a required field")

        product_id = product["id"]
        name = product["name"]
        price = product["price"]
        stock = product["stock"]
        if not isinstance(product_id, str) or not product_id.strip():
            raise ValueError("product ID must be text")
        if product_id in seen_ids:
            raise ValueError("product IDs must be unique")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("product name must be text")
        if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
            raise ValueError("price must be a non-negative number")
        if isinstance(stock, bool) or not isinstance(stock, int) or stock < 0:
            raise ValueError("stock must be a non-negative whole number")

        seen_ids.add(product_id)
        validated.append(
            {
                "id": product_id.strip().upper(),
                "name": name.strip(),
                "price": float(price),
                "stock": stock,
            }
        )
    return validated


def load_inventory(file_path=INVENTORY_FILE):
    """Load inventory JSON, or return an empty list when it does not exist."""
    path = Path(file_path)
    if not path.exists():
        print(f"{path.name} not found. Starting with an empty inventory.")
        return []

    try:
        inventory = validate_inventory(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Could not load {path.name}: {error}. Starting with an empty inventory.")
        return []

    print(f"{path.name} found.")
    print("Inventory loaded successfully.")
    return inventory


def display_all(inventory):
    """Display every product currently in the inventory list."""
    print("\nCurrent Inventory")
    print("-" * 60)
    if not inventory:
        print("No products in inventory.")
    for product in inventory:
        print(
            f"ID: {product['id']} | Name: {product['name']} | "
            f"Price: ${product['price']:.2f} | Stock: {product['stock']}"
        )
    print("-" * 60)


if __name__ == "__main__":
    display_all(load_inventory())
