"""Persistent smart inventory and order auditor.

The program loads earlier inventory data at startup, associates every valid
quantity with a product order, and saves the total, quantity history, and order
records when the operator enters ``quit``.
"""

import json
import os
from pathlib import Path

MAX_INVENTORY = 500
QUIT = "quit"
INVENTORY_FILE = Path(os.environ.get("INVENTORY_FILE", "inventory.txt"))


def load_inventory(file_path=None, include_orders=False):
    """Return the saved total and history, optionally including order records.

    A missing or unreadable file is treated as an empty inventory so that the
    auditor can always start normally. Files created by the earlier version,
    which do not contain an ``orders`` field, are still supported.
    """
    path = Path(file_path) if file_path is not None else INVENTORY_FILE

    try:
        saved_data = json.loads(path.read_text(encoding="utf-8"))
        total = saved_data["total"]
        history = saved_data["history"]
        orders = saved_data.get("orders", [])

        if isinstance(total, bool) or not isinstance(total, int) or total < 0:
            raise ValueError("the saved total is invalid")

        if not isinstance(history, list) or any(
            isinstance(amount, bool) or not isinstance(amount, int) or amount < 0
            for amount in history
        ):
            raise ValueError("the saved transaction history is invalid")

        if not isinstance(orders, list) or any(
            not isinstance(order, list)
            or len(order) != 3
            or isinstance(order[0], bool)
            or not isinstance(order[0], int)
            or order[0] < 1
            or not isinstance(order[1], str)
            or not order[1].strip()
            or isinstance(order[2], bool)
            or not isinstance(order[2], int)
            or order[2] < 0
            for order in orders
        ):
            raise ValueError("the saved orders are invalid")

        if include_orders:
            return total, history, orders
        return total, history
    except FileNotFoundError:
        return (0, [], []) if include_orders else (0, [])
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        print(f"Warning: Could not read {path}; starting with an empty inventory.")
        return (0, [], []) if include_orders else (0, [])


def save_inventory(total, history, orders=None, file_path=None):
    """Save the final total, quantity history, and order records as JSON."""
    # Preserve compatibility with save_inventory(total, history, file_path).
    if file_path is None and isinstance(orders, (str, os.PathLike)):
        file_path = orders
        orders = None

    path = Path(file_path) if file_path is not None else INVENTORY_FILE
    saved_data = {"total": total, "history": history, "orders": orders or []}
    path.write_text(json.dumps(saved_data, indent=2) + "\n", encoding="utf-8")


def get_product_name():
    """Prompt once and return a product name, ``QUIT``, or ``None``."""
    product_name = input("Enter Product Name (or 'quit' to finish): ").strip()

    if product_name.lower() == QUIT:
        return QUIT

    if not product_name:
        print("Error: Product name cannot be empty.")
        return None

    return product_name


def get_valid_input():
    """Prompt once and return an integer, ``QUIT``, or ``None`` if rejected."""
    entry = input("Enter Quantity (or 'quit' to finish): ").strip()

    if entry.lower() == QUIT:
        return QUIT

    if entry.startswith("-") and entry[1:].isdigit():
        print("Error: Quantity cannot be negative.")
        return None

    if not entry.isdigit():
        print("Error: Please enter a whole number or 'quit'.")
        return None

    return int(entry)


def get_next_order_id(orders):
    """Return the next sequential order ID, beginning at 1001."""
    if not orders:
        return 1001
    return max(order[0] for order in orders) + 1


def display_orders(orders):
    """Display every saved order in ID, product, quantity format."""
    print("\nCurrent Orders:")
    if not orders:
        print("No orders recorded.")
        return

    for order_id, product_name, quantity in orders:
        print(f"{order_id}, {product_name}, {quantity}")


def process_delivery(current_total, new_value):
    """Return the inventory total after adding a valid delivery."""
    return current_total + new_value


def calculate_tax(amount):
    """Return the 10% tax for one delivery amount."""
    return amount * 0.10


def generate_report(total_units, failed_attempts, transaction_history, orders=None):
    """Print the final inventory audit summary."""
    print("\nAudit Summary")
    print(f"Total Units Processed: {total_units}")
    print(f"Transaction History: {transaction_history}")
    if orders is not None:
        print(f"Number of Orders: {len(orders)}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def run_auditor():
    """Run the interactive inventory auditing loop."""
    inventory, transaction_history, orders = load_inventory(include_orders=True)
    failed_entries = 0
    quit_requested = False

    print("Smart Inventory Auditor")
    print(f"Loaded inventory: {inventory} units")
    print(f"Previous transactions: {transaction_history}")
    display_orders(orders)

    while True:
        product_name = get_product_name()

        if product_name == QUIT:
            break

        if product_name is None:
            failed_entries += 1
            continue

        while True:
            quantity = get_valid_input()

            if quantity == QUIT:
                quit_requested = True
                break

            if quantity is None:
                failed_entries += 1
                continue

            break

        if quit_requested:
            break

        order_id = get_next_order_id(orders)
        order = [order_id, product_name, quantity]
        orders.append(order)
        inventory = process_delivery(inventory, quantity)
        transaction_history.append(quantity)

        print("\nNew Order Added:")
        print(f"{order_id}, {product_name}, {quantity}")

        tax = calculate_tax(quantity)
        print(f"Tax for this delivery: {tax:.2f}")
        print(f"Current inventory: {inventory} units")

        if inventory > MAX_INVENTORY:
            print("OVERSTOCK ALERT: Total inventory exceeds 500 units.")

    save_inventory(inventory, transaction_history, orders)
    print(f"Inventory and orders saved to {INVENTORY_FILE}.")
    generate_report(inventory, failed_entries, transaction_history, orders)


if __name__ == "__main__":
    run_auditor()
