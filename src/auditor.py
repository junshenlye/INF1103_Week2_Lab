"""Smart Inventory Auditor
Accept stock deliveries until the operator quits or inventory exceeds capacity.
"""

MAX_INVENTORY = 500


def run_auditor() -> None:
    """Run the interactive inventory auditing loop."""
    inventory = 0
    failed_entries = 0

    print("Smart Inventory Auditor")
    print("Enter a stock quantity, or type 'quit' to finish.")

    while True:
        entry = input("Stock quantity: ").strip()

        if entry.lower() == "quit":
            break

        # Check negatives separately so the operator receives a useful error.
        if entry.startswith("-") and entry[1:].isdigit():
            failed_entries += 1
            print("Error: Stock quantity cannot be negative.")
            continue

        if not entry.isdigit():
            failed_entries += 1
            print("Error: Please enter a whole number or 'quit'.")
            continue

        inventory += int(entry)
        print(f"Current inventory: {inventory} units")

        if inventory > MAX_INVENTORY:
            print("OVERSTOCK ALERT: Total inventory exceeds 500 units.")
            break

    print("\nAudit Summary")
    print(f"Total Units Processed: {inventory}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")

if __name__ == "__main__":
    run_auditor()
