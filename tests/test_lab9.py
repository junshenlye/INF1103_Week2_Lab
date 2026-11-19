import contextlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from discount_strategy import (
    BulkDiscount, DiscountStrategy, NoDiscount, PercentageDiscount, StudentDiscount,
)
from file_handling import load_inventory, load_products
from input_helpers import get_positive_float
from inventory import Inventory
from order import Order
from product import Product
from product_factory import ProductFactory
from supplier import Supplier


class Lab9Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("SUP9", "Lab Supplies", "lab@example.com")

    def product(self, kind="physical", product_id="P1", price=125, stock=10):
        return ProductFactory.create(kind, product_id, "Lab Kit", price, stock,
                                     self.supplier)

    def order(self, discount=None):
        order = Order("O9", discount)
        order.add_order_line(self.product(), 2)
        return order

    def test_discount_base_is_abstract(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_default_no_discount_and_empty_order(self):
        self.assertIsInstance(Order("EMPTY").discount, NoDiscount)
        self.assertEqual(Order("EMPTY").calculate_total(), 0.0)
        self.assertEqual(self.order().calculate_total(), 250)

    def test_switch_strategy_on_same_order(self):
        order = self.order(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)
        lines = order.get_order_lines()
        order.set_discount(PercentageDiscount(10))
        self.assertEqual(order.calculate_total(), 225)
        self.assertEqual(order.get_order_lines(), lines)
        order.set_discount(StudentDiscount())
        self.assertEqual(order.calculate_total(), 237.5)

    def test_bulk_threshold_boundaries_and_floor(self):
        discount = BulkDiscount(200, 20)
        self.assertEqual(discount.apply(199.99), 199.99)
        self.assertEqual(discount.apply(200), 180)
        self.assertEqual(BulkDiscount(1, 20).apply(5), 0)

    def test_percentage_boundaries(self):
        self.assertEqual(PercentageDiscount(0).apply(250), 250)
        self.assertEqual(PercentageDiscount(100).apply(250), 0)
        self.assertEqual(StudentDiscount().apply(250), 237.5)

    def test_invalid_discount_parameters(self):
        for bad in (-1, 101, float("nan"), float("inf"), True, "10"):
            with self.subTest(percentage=bad), self.assertRaises(ValueError):
                PercentageDiscount(bad)
        for threshold, amount in ((0, 20), (-1, 20), (200, -1),
                                  (float("inf"), 1), (1, float("nan"))):
            with self.subTest(threshold=threshold, amount=amount):
                with self.assertRaises(ValueError):
                    BulkDiscount(threshold, amount)

    def test_new_strategy_without_changing_order(self):
        class FiveOff(DiscountStrategy):
            def apply(self, total: float) -> float:
                return max(0.0, total - 5)
        self.assertEqual(self.order(FiveOff()).calculate_total(), 245)

    def test_shared_strategy_is_association(self):
        shared = PercentageDiscount(10)
        first, second = self.order(shared), self.order(shared)
        self.assertIs(first.discount, second.discount)
        first.set_discount(NoDiscount())
        self.assertEqual(first.calculate_total(), 250)
        self.assertEqual(second.calculate_total(), 225)

    def test_order_rejects_invalid_strategy(self):
        with self.assertRaises(TypeError):
            self.order("percentage")
        order = self.order()
        with self.assertRaises(TypeError):
            order.set_discount(None)
        self.assertEqual(order.calculate_total(), 250)

    def test_order_uses_selected_discount(self):
        strategy = NoDiscount()
        with patch.object(strategy, "apply", return_value=123) as apply:
            self.assertEqual(self.order(strategy).calculate_total(), 123)
            apply.assert_called_once_with(250.0)

    def test_factory_types_defaults_and_explicit_extra(self):
        for kind, field, value in (("physical", "weight", 1.0),
                                   ("digital", "download_size", 1.0),
                                   ("subscription", "duration_months", 12)):
            with self.subTest(kind=kind):
                product = self.product(kind)
                self.assertIsInstance(product, Product)
                self.assertEqual(getattr(product, field), value)
                self.assertIs(product.supplier, self.supplier)
        explicit = ProductFactory.create("physical", "P2", "Lamp", 25, 1,
                                         self.supplier, 3.5)
        self.assertEqual(explicit.weight, 3.5)

    def test_factory_unknown_type_error(self):
        with self.assertRaisesRegex(ValueError, "Unknown product type: service"):
            self.product("service")

    def test_product_price_must_be_strictly_positive(self):
        for kind in ("physical", "digital", "subscription"):
            for bad in (0, -1, float("nan"), float("inf"), True, "5"):
                with self.subTest(kind=kind, price=bad), self.assertRaises(ValueError):
                    self.product(kind, price=bad)

    def test_stock_contract_preserved_by_all_subclasses(self):
        for kind in ("physical", "digital", "subscription"):
            with self.subTest(kind=kind):
                product = self.product(kind, stock=0)
                product.update_stock(5)
                with self.assertRaises(ValueError):
                    product.update_stock(-1)
                self.assertEqual(product.stock, 5)
                with self.assertRaises(ValueError):
                    self.product(kind, stock=-1)

    def test_order_line_quantity_validation(self):
        order = Order("O9")
        for bad in (0, -1, 1.5, True):
            with self.subTest(quantity=bad), self.assertRaises(ValueError):
                order.add_order_line(self.product(), bad)
        self.assertEqual(order.get_order_lines(), ())

    def test_positive_float_retries_exact_messages(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]) as ask:
            with contextlib.redirect_stdout(output):
                value = get_positive_float("Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(ask.call_count, 3)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_positive_float_rejects_zero_and_nonfinite_values(self):
        with patch("builtins.input", side_effect=["0", "nan", "inf", "2.5"]):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(get_positive_float("Price: "), 2.5)

    def test_supplied_csv_skips_bad_rows_and_counts_valid_rows(self):
        inventory = Inventory()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            load_products(Path(__file__).resolve().parents[1] / "products.csv",
                          inventory, self.supplier)
        self.assertEqual([p.product_id for p in inventory.get_products()],
                         ["P001", "D001", "P003"])
        self.assertTrue(all(p.supplier is self.supplier for p in inventory.get_products()))
        lines = output.getvalue().splitlines()
        self.assertIn("Row 4 skipped: Unknown product type: service", lines[0])
        self.assertTrue(lines[1].startswith("Row 5 skipped:"))
        self.assertEqual(lines[2:], ["3 products loaded.", "Load attempt finished."])

    def test_missing_csv_handled_and_finally_runs(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "products.csv"
            inventory, output = Inventory(), io.StringIO()
            with contextlib.redirect_stdout(output):
                load_products(path, inventory, self.supplier)
            self.assertEqual(output.getvalue().splitlines(), [
                f"Products file not found: {path}", "Load attempt finished.",
            ])
            self.assertEqual(inventory.get_products(), ())

    def test_csv_invalid_values_shapes_and_duplicates_do_not_stop_import(self):
        rows = ("product_type,product_id,name,price,stock_quantity\n"
                "physical,ZERO,Zero,0,1\nphysical,NEG,Negative,10,-1\n"
                "physical,NAN,NotFinite,nan,1\nphysical,BADSTOCK,Bad,10,abc\n"
                "too,few,columns\nphysical,P1,Valid,10,1\n"
                "digital,P1,Duplicate,20,2\ndigital,D1,Valid,20,2\n")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "products.csv"
            path.write_text(rows, encoding="utf-8")
            inventory, output = Inventory(), io.StringIO()
            with contextlib.redirect_stdout(output):
                load_products(path, inventory, self.supplier)
        self.assertEqual([p.product_id for p in inventory.get_products()], ["P1", "D1"])
        self.assertEqual(output.getvalue().count("skipped:"), 6)
        self.assertTrue(output.getvalue().endswith("2 products loaded.\nLoad attempt finished.\n"))

    def test_empty_and_header_only_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "products.csv"
            for content in ("", "product_type,product_id,name,price,stock_quantity\n"):
                path.write_text(content, encoding="utf-8")
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    load_products(path, Inventory(), self.supplier)
                self.assertEqual(output.getvalue(),
                                 "0 products loaded.\nLoad attempt finished.\n")

    def test_renamed_csv_runs_missing_file_handler(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "products.csv"
            path.write_text("product_type,product_id,name,price,stock_quantity\n")
            renamed = path.with_suffix(".bak")
            path.rename(renamed)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                load_products(path, Inventory(), self.supplier)
            self.assertIn(f"Products file not found: {path}", output.getvalue())
            self.assertNotIn("products loaded.", output.getvalue())
            self.assertTrue(output.getvalue().endswith("Load attempt finished.\n"))
            self.assertTrue(renamed.exists())

    def test_csv_creation_uses_factory(self):
        with patch.object(ProductFactory, "create", wraps=ProductFactory.create) as create:
            with contextlib.redirect_stdout(io.StringIO()):
                load_products(Path(__file__).resolve().parents[1] / "products.csv",
                              Inventory(), self.supplier)
        self.assertEqual(create.call_count, 4)  # Invalid float fails before creation.

    def test_uncaught_factory_error_exits_program(self):
        result = subprocess.run([
            sys.executable, "-c",
            "from product_factory import ProductFactory; "
            "from supplier import Supplier; "
            "ProductFactory.create('service','S','Install',30,5,"
            "Supplier('SUP','Lab','lab@example.com'))",
        ], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ValueError: Unknown product type: service", result.stderr)

    def test_menu_retries_price_without_losing_product_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            environment = dict(os.environ, INVENTORY_FILE=str(Path(directory) / "inventory.json"))
            result = subprocess.run(
                [sys.executable, "inventory_manager.py"],
                input=("2\nphysical\nP9\nLamp\nabc\n-5\n12.50\n2\nSUP9\n"
                       "Lab\nlab@example.com\n1\n1\n7\n"),
                capture_output=True, text=True, env=environment, check=True,
            )
        self.assertEqual(result.stdout.count("Please enter a valid number, e.g. 12.50"), 1)
        self.assertEqual(result.stdout.count("Please enter a number greater than zero."), 1)
        self.assertIn("Product added successfully!", result.stdout)
        self.assertIn("Price: $12.50", result.stdout)
        self.assertNotIn("Could not complete action", result.stdout)

    def test_menu_csv_import_and_save(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "inventory.json"
            environment = dict(os.environ, INVENTORY_FILE=str(path))
            result = subprocess.run(
                [sys.executable, "inventory_manager.py"],
                input="8\nproducts.csv\nSUP9\nLab\nlab@example.com\n1\n7\n",
                capture_output=True, text=True, env=environment, check=True,
            )
            with contextlib.redirect_stdout(io.StringIO()):
                restored = load_inventory(path)
            self.assertEqual(len(restored.get_products()), 3)
        self.assertIn("3 products loaded.", result.stdout)
        self.assertIn("Desk Lamp", result.stdout)
        self.assertIn("Load attempt finished.", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
