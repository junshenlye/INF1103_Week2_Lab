"""JSON-backed inventory management system for INF1103 Week 5."""

import json
import os
from pathlib import Path

INVENTORY_FILE = Path(os.environ.get("INVENTORY_FILE", "inventory.json"))


def validate_inventory(data):
    """Return normalized product dictionaries or raise ``ValueError``."""
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

        product_id = product_id.strip().upper()
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
                "id": product_id,
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


def save_inventory(inventory, file_path=INVENTORY_FILE):
    """Validate and atomically save inventory as formatted JSON."""
    path = Path(file_path)
    validated = validate_inventory(inventory)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    temporary_path.write_text(
        json.dumps(validated, indent=2) + "\n", encoding="utf-8"
    )
    temporary_path.replace(path)
    print(f"Inventory saved successfully to {path.name}.")


def find_product(inventory, product_id):
    """Return the product matching ``product_id``, or ``None``."""
    target_id = product_id.strip().upper()
    return next(
        (product for product in inventory if product["id"] == target_id), None
    )


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


def add_product(inventory):
    """Prompt for and append one product dictionary."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Product ID cannot be empty.")
        return False
    if find_product(inventory, product_id):
        print("A product with that ID already exists.")
        return False

    name = input("Product Name: ").strip()
    if not name:
        print("Product name cannot be empty.")
        return False

    try:
        price = float(input("Price: ").strip())
        stock = int(input("Stock Quantity: ").strip())
    except ValueError:
        print("Price must be a number and stock must be a whole number.")
        return False
    if price < 0 or stock < 0:
        print("Price and stock cannot be negative.")
        return False

    inventory.append(
        {"id": product_id, "name": name, "price": price, "stock": stock}
    )
    print("\nProduct added successfully!")
    return True


def update_stock(inventory):
    """Prompt for a product and replace its stock quantity."""
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)
    if product is None:
        print("\nProduct not found.")
        return False

    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    try:
        new_stock = int(input("\nNew Stock Quantity: ").strip())
    except ValueError:
        print("Stock must be a whole number.")
        return False
    if new_stock < 0:
        print("Stock cannot be negative.")
        return False

    product["stock"] = new_stock
    print("\nStock updated successfully!")
    return True


def search_product(inventory):
    """Prompt for an ID and display the matching product."""
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)
    if product is None:
        print("\nProduct not found.")
        return None

    print("\nProduct Found")
    print("-" * 48)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 48)
    return product


def display_menu():
    """Display the six available inventory actions."""
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def run_inventory_manager():
    """Load inventory and process menu choices until the user exits."""
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()
    inventory = load_inventory()

    while True:
        display_menu()
        option = input("\nEnter option: ").strip()

        if option == "1":
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            return
        else:
            print("\nInvalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    run_inventory_manager()
