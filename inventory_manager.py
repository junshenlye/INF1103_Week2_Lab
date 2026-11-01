"""Menu and input handling for the Week 9 OOP inventory system."""
import os
from pathlib import Path
from file_handling import load_inventory, save_inventory
from product_catalog import PRODUCT_TYPES, create_product

INVENTORY_FILE = Path(os.environ.get("INVENTORY_FILE", "inventory.json"))


def display_menu():
    print("\n----------- MENU -----------\n"
          "1. Display All Products\n2. Add Product\n3. Update Stock\n"
          "4. Search Product\n5. Save Inventory\n6. Exit")


def run_inventory_manager():
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
                _, _, prompt, converter = PRODUCT_TYPES[kind]
                extra = converter(input(prompt))
                inventory.add_product(create_product(kind, product_id, name, price, stock, extra))
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
            elif option in ("5", "6"):
                save_inventory(inventory, INVENTORY_FILE)
                if option == "6":
                    print("Thank you for using Inventory Management System.")
                    return
            else:
                print("Invalid option. Please enter a number from 1 to 6.")
        except (ValueError, OSError) as error:
            print(f"Could not complete action: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nInput ended. Use option 5 or 6 to save changes before quitting.")
            return


if __name__ == "__main__":
    run_inventory_manager()
