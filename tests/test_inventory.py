import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from subscription_product import SubscriptionProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from file_handling import save_inventory, load_inventory

class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.physical = PhysicalProduct('p1', 'Guitar', 100, 2, 3)
        self.digital = DigitalProduct('d1', 'App', 20, 10, 512)

    def test_abstract_contracts(self):
        with self.assertRaises(TypeError):
            Product('x', 'Generic', 1, 1)
        with self.assertRaises(TypeError):
            CanBeShipped()
        class Incomplete(Product):
            pass
        with self.assertRaises(TypeError):
            Incomplete('x', 'Incomplete', 1, 1)

    def test_overrides_and_fulfilment(self):
        for product, extra in [(self.physical, 'Weight: 3 kg'), (self.digital, 'Download Size: 512 MB')]:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                product.display_information()
            for expected in [product.product_id, product.name, 'Price:', 'Stock:', extra, product.get_fulfilment_info()]:
                self.assertIn(expected, out.getvalue())

    def test_shipping_capability(self):
        self.assertIsInstance(self.physical, CanBeShipped)
        self.assertEqual(self.physical.calculate_shipping_cost(), 15)
        self.assertEqual(PhysicalProduct('p2', 'Cable', 1, 1, .5).calculate_shipping_cost(), 2.5)
        self.assertNotIsInstance(self.digital, CanBeShipped)
        self.assertFalse(hasattr(self.digital, 'calculate_shipping_cost'))

    def test_inventory_operations(self):
        inventory = Inventory()
        inventory.add_product(self.physical)
        inventory.add_product(self.digital)
        self.assertIs(inventory.search_product(' P1 '), self.physical)
        self.assertIsNone(inventory.search_product('absent'))
        with self.assertRaises(ValueError):
            inventory.add_product(self.physical)
        with self.assertRaises(TypeError):
            inventory.add_product({})
        self.physical.update_stock(20)
        self.assertEqual(self.physical.stock, 20)
        with self.assertRaises(AttributeError):
            self.physical.weight = 5

    def test_invalid_values(self):
        for bad in [-1, 0, float('nan'), float('inf'), True, '3']:
            for cls in [PhysicalProduct, DigitalProduct]:
                with self.assertRaises(ValueError):
                    cls('a', 'A', 1, 1, bad)
        for bad in [-1, 1.5, True]:
            with self.assertRaises(ValueError):
                self.physical.update_stock(bad)
        with self.assertRaises(ValueError):
            SubscriptionProduct('s', 'S', 1, 1, 1.5)

    def test_json_roundtrip_and_errors(self):
        inventory = Inventory()
        for p in [self.physical, self.digital, SubscriptionProduct('s1', 'Music', 60, 5, 12)]:
            inventory.add_product(p)
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'inventory.json'
            save_inventory(inventory, path)
            restored = load_inventory(path).get_products()
            self.assertEqual([type(p) for p in restored], [PhysicalProduct, DigitalProduct, SubscriptionProduct])
            self.assertEqual(restored[0].weight, 3)
            self.assertEqual(restored[1].download_size, 512)
            self.assertEqual(restored[2].duration_months, 12)
            for bad in ['{}', '[{}]', '[{"type":"other"}]', 'invalid']:
                path.write_text(bad)
                with self.assertRaises(ValueError):
                    load_inventory(path)
                self.assertEqual(path.read_text(), bad)

    def test_cli_and_restart(self):
        with tempfile.TemporaryDirectory() as d:
            env = dict(os.environ, INVENTORY_FILE=str(Path(d)/'inventory.json'))
            commands = '2\nphysical\nP9\nGuitar\n100\n2\n3\n2\ndigital\nD9\nApp\n20\n10\n512\n3\nP9\n25\n4\np9\n1\n5\n6\n'
            first = subprocess.run([sys.executable, 'inventory_manager.py'], input=commands, text=True, capture_output=True, env=env, check=True)
            self.assertIn('Stock updated successfully!', first.stdout)
            second = subprocess.run([sys.executable, 'inventory_manager.py'], input='1\n6\n', text=True, capture_output=True, env=env, check=True)
            for expected in ['Stock: 25', 'Weight: 3 kg', 'Download Size: 512 MB']:
                self.assertIn(expected, second.stdout)

if __name__ == '__main__':
    unittest.main(verbosity=2)
