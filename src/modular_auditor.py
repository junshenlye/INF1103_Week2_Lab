"""Modular smart inventory auditor.

The program accepts stock deliveries until the operator enters ``quit``. Each
piece of business logic is kept in a small function so it can be reused and
tested independently.
"""

MAX_INVENTORY = 500
QUIT = "quit"


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


def generate_report(total_units, failed_attempts):
    """Print the final inventory audit summary."""
    print("\nAudit Summary")
    print(f"Total Units Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def run_auditor():
    """Run the interactive inventory auditing loop."""
    inventory = 0
    failed_entries = 0

    print("Smart Inventory Auditor")
    print("Enter a stock quantity, or type 'quit' to finish.")

    while True:
        delivery = get_valid_input()

        if delivery == QUIT:
            break

        if delivery is None:
            failed_entries += 1
            continue

        inventory = process_delivery(inventory, delivery)
        tax = calculate_tax(delivery)
        print(f"Tax for this delivery: {tax:.2f}")
        print(f"Current inventory: {inventory} units")

        if inventory > MAX_INVENTORY:
            print("OVERSTOCK ALERT: Total inventory exceeds 500 units.")

    generate_report(inventory, failed_entries)


if __name__ == "__main__":
    run_auditor()
