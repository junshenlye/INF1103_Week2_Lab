"""Persistent smart inventory auditor.

The program loads an earlier inventory session at startup, tracks every valid
delivery, and saves the updated total and transaction history when the operator
enters ``quit``.
"""

import json
import os
from pathlib import Path

MAX_INVENTORY = 500
QUIT = "quit"
INVENTORY_FILE = Path(os.environ.get("INVENTORY_FILE", "inventory.txt"))


def load_inventory(file_path=None):
    """Return the saved inventory total and transaction history.

    A missing or unreadable file is treated as an empty inventory so that the
    auditor can always start normally.
    """
    path = Path(file_path) if file_path is not None else INVENTORY_FILE

    try:
        saved_data = json.loads(path.read_text(encoding="utf-8"))
        total = saved_data["total"]
        history = saved_data["history"]

        if isinstance(total, bool) or not isinstance(total, int) or total < 0:
            raise ValueError("the saved total is invalid")

        if not isinstance(history, list) or any(
            isinstance(amount, bool) or not isinstance(amount, int) or amount < 0
            for amount in history
        ):
            raise ValueError("the saved transaction history is invalid")

        return total, history
    except FileNotFoundError:
        return 0, []
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        print(f"Warning: Could not read {path}; starting with an empty inventory.")
        return 0, []


def get_valid_input():
    """Prompt once and return an integer, ``QUIT``, or ``None`` if rejected."""
    entry = input("Stock quantity: ").strip()

    if entry.lower() == QUIT:
        return QUIT

    if entry.startswith("-") and entry[1:].isdigit():
        print("Error: Stock quantity cannot be negative.")
        return None

    if not entry.isdigit():
        print("Error: Please enter a whole number or 'quit'.")
        return None

    return int(entry)


def process_delivery(current_total, new_value):
    """Return the inventory total after adding a valid delivery."""
    return current_total + new_value


def calculate_tax(amount):
    """Return the 10% tax for one delivery amount."""
    return amount * 0.10


def generate_report(total_units, failed_attempts, transaction_history):
    """Print the final inventory audit summary."""
    print("\nAudit Summary")
    print(f"Total Units Processed: {total_units}")
    print(f"Transaction History: {transaction_history}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def run_auditor():
    """Run the interactive inventory auditing loop."""
    inventory, transaction_history = load_inventory()
    failed_entries = 0

    print("Smart Inventory Auditor")
    print(f"Loaded inventory: {inventory} units")
    print(f"Previous transactions: {transaction_history}")
    print("Enter a stock quantity, or type 'quit' to finish.")

    while True:
        delivery = get_valid_input()

        if delivery == QUIT:
            break

        if delivery is None:
            failed_entries += 1
            continue

        inventory = process_delivery(inventory, delivery)
        transaction_history.append(delivery)
        tax = calculate_tax(delivery)
        print(f"Tax for this delivery: {tax:.2f}")
        print(f"Current inventory: {inventory} units")

        if inventory > MAX_INVENTORY:
            print("OVERSTOCK ALERT: Total inventory exceeds 500 units.")

    generate_report(inventory, failed_entries, transaction_history)


if __name__ == "__main__":
    run_auditor()
