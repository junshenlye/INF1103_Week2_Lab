"""Menu and input handling for the Week 10 OOP inventory system."""
from __future__ import annotations
import os
from pathlib import Path
from file_handling import load_inventory, save_inventory
from inventory import Inventory
from product_catalog import PRODUCT_TYPES, create_product
from supplier import Supplier

INVENTORY_FILE = Path(os.environ.get("INVENTORY_FILE", "inventory.json"))


def display_menu() -> None:
    print("\n----------- MENU -----------\n"
          "1. Display All Products\n2. Add Product\n3. Update Stock\n"
          "4. Search Product\n5. Remove Product\n6. Save Inventory\n7. Exit")


def find_supplier(inventory: Inventory, supplier_id: str) -> Supplier | None:
    target = supplier_id.strip().upper()
    return next((product.supplier for product in inventory.get_products()
                 if product.supplier.supplier_id == target), None)


def run_inventory_manager() -> None:
    print("INVENTORY MANAGEMENT SYSTEM")
    try:
        inventory = load_inventory(INVENTORY_FILE)
    except (OSError, ValueError) as error:
        print(f"Could not load inventory: {error}. Source file was left unchanged.")
        return
    while True:
        display_menu()
        try:
            option = input("Enter option: ").strip()
            if option == "1":
                inventory.display_all()
            elif option == "2":
                kind = input("Product type (" + ", ".join(PRODUCT_TYPES) + "): ").strip().lower()
                if kind not in PRODUCT_TYPES:
                    raise ValueError("Unknown product type.")
                product_id = input("Product ID: ")
                name = input("Product Name: ")
                price = float(input("Price: "))
                stock = int(input("Stock Quantity: "))
                supplier_id = input("Supplier ID: ")
                supplier = find_supplier(inventory, supplier_id)
                if supplier is None:
                    supplier = Supplier(
                        supplier_id,
                        input("Supplier Name: "),
                        input("Supplier Contact Email: "),
                    )
                else:
                    print(f"Using existing supplier: {supplier.name}")
                _, _, prompt, converter = PRODUCT_TYPES[kind]
                extra = converter(input(prompt))
                inventory.add_product(create_product(
                    kind, product_id, name, price, stock, supplier, extra
                ))
                print("Product added successfully!")
            elif option in ("3", "4"):
                product = inventory.search_product(input("Enter Product ID: "))
                if product is None:
                    print("Product not found.")
                else:
                    product.display_information()
                    if option == "3":
                        product.update_stock(int(input("New Stock Quantity: ")))
                        print("Stock updated successfully!")
            elif option == "5":
                removed = inventory.remove_product(input("Enter Product ID: "))
                if removed is None:
                    print("Product not found.")
                else:
                    print(f"{removed.name} removed from inventory.")
            elif option in ("6", "7"):
                save_inventory(inventory, INVENTORY_FILE)
                if option == "7":
                    print("Thank you for using Inventory Management System.")
                    return
            else:
                print("Invalid option. Please enter a number from 1 to 7.")
        except (ValueError, OSError) as error:
            print(f"Could not complete action: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nInput ended. Use option 6 or 7 to save changes before quitting.")
            return


if __name__ == "__main__":
    run_inventory_manager()
