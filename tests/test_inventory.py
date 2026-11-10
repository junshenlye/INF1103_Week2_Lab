import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import get_type_hints
import unittest

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from file_handling import load_inventory, save_inventory
from inventory import Inventory
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from product import Product
from subscription_product import SubscriptionProduct
from supplier import Supplier


def show_product_details(product: Product) -> str:
    """Use only behaviour guaranteed by the Product abstraction."""
    product.display_information()
    return product.get_fulfilment_info()


class InventoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("sup1", "Learning Supplies", "sales@example.com")
        self.physical = PhysicalProduct(
            "p1", "Guitar", 100, 2, self.supplier, 3
        )
        self.digital = DigitalProduct(
            "d1", "App", 20, 10, self.supplier, 512
        )

    def test_abstract_contracts(self) -> None:
        with self.assertRaises(TypeError):
            Product("x", "Generic", 1, 1, self.supplier)
        with self.assertRaises(TypeError):
            CanBeShipped()

        class Incomplete(Product):
            pass

        with self.assertRaises(TypeError):
            Incomplete("x", "Incomplete", 1, 1, self.supplier)

    def test_supplier_association_survives_deleted_local_name(self) -> None:
        supplier = Supplier("sup2", "Shared Supplier", "shared@example.com")
        physical = PhysicalProduct("p2", "Cable", 10, 5, supplier, 0.5)
        digital = DigitalProduct("d2", "Guide", 5, 100, supplier, 20)
        del supplier

        self.assertIs(physical.supplier, digital.supplier)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            physical.display_supplier_information()
            digital.display_supplier_information()
        self.assertEqual(output.getvalue().count("Shared Supplier"), 2)

    def test_overrides_and_polymorphism(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.physical)
        inventory.add_product(self.digital)

        with contextlib.redirect_stdout(io.StringIO()):
            fulfilment = [
                show_product_details(product)
                for product in inventory.get_products()
            ]
        self.assertEqual(fulfilment, [
            "Requires physical shipping.",
            "Delivered digitally by download.",
        ])
        for product in inventory.get_products():
            product.update_stock(7)
            self.assertEqual(product.stock, 7)

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            inventory.display_all()
        for expected in [
                "Weight: 3 kg", "Download Size: 512 MB",
                "Requires physical shipping.", "Delivered digitally by download."]:
            self.assertIn(expected, output.getvalue())

    def test_shipping_capability(self) -> None:
        self.assertIsInstance(self.physical, CanBeShipped)
        self.assertEqual(self.physical.calculate_shipping_cost(), 15)
        cable = PhysicalProduct("p2", "Cable", 1, 1, self.supplier, 0.5)
        self.assertEqual(cable.calculate_shipping_cost(), 2.5)
        self.assertNotIsInstance(self.digital, CanBeShipped)
        self.assertFalse(hasattr(self.digital, "calculate_shipping_cost"))

    def test_inventory_aggregation_and_transfer(self) -> None:
        inventory_a = Inventory()
        inventory_b = Inventory()
        inventory_a.add_product(self.physical)
        inventory_a.add_product(self.digital)

        self.assertIs(inventory_a.find_product(" P1 "), self.physical)
        self.assertIs(inventory_a.search_product("p1"), self.physical)
        self.assertIsNone(inventory_a.find_product("absent"))
        with self.assertRaises(ValueError):
            inventory_a.add_product(self.physical)
        with self.assertRaises(TypeError):
            inventory_a.add_product({})

        removed = inventory_a.remove_product("p1")
        self.assertIs(removed, self.physical)
        self.assertIsNone(inventory_a.find_product("p1"))
        self.physical.update_stock(20)
        inventory_b.add_product(self.physical)
        self.assertIs(inventory_b.find_product("p1"), self.physical)
        self.assertEqual(self.physical.stock, 20)

    def test_order_composition_and_totals(self) -> None:
        first_order = Order("o1")
        second_order = Order("o2")
        first_order.add_order_line(self.physical, 2)
        first_order.add_order_line(self.digital, 1)
        second_order.add_order_line(self.physical, 1)

        first_lines = first_order.get_order_lines()
        second_line = second_order.get_order_lines()[0]
        self.assertEqual(first_order.calculate_total(), 220)
        self.assertIsNot(first_lines[0], second_line)
        self.assertIs(first_lines[0].product, second_line.product)
        self.assertIs(first_lines[0].product, self.physical)

        removed = first_order.remove_order_line("p1")
        self.assertIs(removed, first_lines[0])
        self.assertEqual(first_order.calculate_total(), 20)
        self.assertEqual(self.physical.price, 100)
        with self.assertRaises(ValueError):
            first_order.add_order_line(self.digital, 0)

    def test_invalid_values(self) -> None:
        for bad in [-1, 0, float("nan"), float("inf"), True, "3"]:
            for cls in [PhysicalProduct, DigitalProduct]:
                with self.assertRaises(ValueError):
                    cls("a", "A", 1, 1, self.supplier, bad)
        for bad in [-1, 1.5, True]:
            with self.assertRaises(ValueError):
                self.physical.update_stock(bad)
        with self.assertRaises(ValueError):
            SubscriptionProduct("s", "S", 1, 1, self.supplier, 1.5)
        with self.assertRaises(ValueError):
            Supplier("s", "Supplier", "not-an-email")

    def test_json_roundtrip_preserves_types_and_shared_supplier(self) -> None:
        inventory = Inventory()
        subscription = SubscriptionProduct(
            "s1", "Music", 60, 5, self.supplier, 12
        )
        for product in [self.physical, self.digital, subscription]:
            inventory.add_product(product)

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "inventory.json"
            save_inventory(inventory, path)
            restored = load_inventory(path).get_products()
            self.assertEqual(
                [type(product) for product in restored],
                [PhysicalProduct, DigitalProduct, SubscriptionProduct],
            )
            self.assertIs(restored[0].supplier, restored[1].supplier)
            self.assertIs(restored[1].supplier, restored[2].supplier)
            self.assertEqual(restored[0].weight, 3)
            self.assertEqual(restored[1].download_size, 512)
            self.assertEqual(restored[2].duration_months, 12)

            for bad in ["{}", "[{}]", '[{"type":"other"}]', "invalid"]:
                path.write_text(bad)
                with self.assertRaises(ValueError):
                    load_inventory(path)
                self.assertEqual(path.read_text(), bad)

    def test_type_hints_match_design(self) -> None:
        self.assertIs(get_type_hints(Inventory.add_product)["product"], Product)
        self.assertEqual(
            Inventory.find_product.__annotations__["return"], "Product | None"
        )
        self.assertIs(get_type_hints(Order.add_order_line)["product"], Product)
        self.assertIs(get_type_hints(OrderLine.__init__)["product"], Product)
        self.assertIs(get_type_hints(OrderLine.calculate_subtotal)["return"], float)

    def test_cli_and_restart(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "inventory.json"
            environment = dict(os.environ, INVENTORY_FILE=str(path))
            commands = (
                "2\nphysical\nP9\nGuitar\n100\n2\nSUP9\nMusic Supply\n"
                "sales@example.com\n3\n"
                "2\ndigital\nD9\nApp\n20\n10\nSUP9\n512\n"
                "3\nP9\n25\n4\np9\n1\n6\n7\n"
            )
            first = subprocess.run(
                [sys.executable, "inventory_manager.py"],
                input=commands,
                text=True,
                capture_output=True,
                env=environment,
                check=True,
            )
            self.assertIn("Using existing supplier: Music Supply", first.stdout)
            self.assertIn("Stock updated successfully!", first.stdout)

            second = subprocess.run(
                [sys.executable, "inventory_manager.py"],
                input="1\n7\n",
                text=True,
                capture_output=True,
                env=environment,
                check=True,
            )
            for expected in [
                    "Stock: 25", "Weight: 3 kg", "Download Size: 512 MB",
                    "Music Supply"]:
                self.assertIn(expected, second.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
