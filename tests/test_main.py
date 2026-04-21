import unittest
import io
import contextlib

from main import (
    CustomerManager,
    calculate_shipping_fee_for_fragile_items,
    calculate_shipping_fee_for_heavy_items,
)

class TestCustomerManager(unittest.TestCase):

    def test_add_customer(self):
        cm = CustomerManager()
        name = "Alice"
        purchases = [{'price': 50, 'item': 'banana'}, {'price': 80, 'item': 'apple'}]
        cm.add_customer(name, purchases)

        self.assertEqual(
            {name: purchases},
            cm.customers
        )

    def test_add_purchase(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase]},
            cm.customers
        )

    def test_add_purchase_multiple(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase, purchase]},
            cm.customers
        )

    def test_add_purchases(self):
        cm = CustomerManager()
        name = "Alice"
        purchases = [{'price': 50, 'item': 'banana'}, {'price': 80, 'item': 'apple'}]
        cm.add_purchases(name, purchases)

        self.assertEqual(
            {name: purchases},
            cm.customers
        )

    def test_discount_eligibility(self):
        cm = CustomerManager()
        cm.add_customer("Bob", [{'price': 600}])

        # Capture printed output
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()

        self.assertIn("Bob", output)
        self.assertIn("Eligible for discount", output)

    def test_no_tax_applied_when_price_at_or_below_threshold(self):
        cm = CustomerManager()
        # price == 100 should NOT be taxed (threshold is strictly > 100)
        cm.add_customer("Grace", [{'price': 100}])

        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()
        self.assertIn("Grace", output)
        self.assertIn("No discount", output)

    def test_potential_future_discount_customer(self):
        cm = CustomerManager()
        cm.add_customer("Carol", [{'price': 350}])

        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()
        self.assertIn("Carol", output)
        self.assertIn("Potential future discount customer", output)

    def test_no_discount_customer(self):
        cm = CustomerManager()
        cm.add_customer("Dave", [{'price': 200}])

        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()
        self.assertIn("Dave", output)
        self.assertIn("No discount", output)

    def test_priority_customer_label(self):
        cm = CustomerManager()
        cm.add_customer("Eve", [{'price': 700}])  # taxed to 840 -> Priority Customer

        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()
        self.assertIn("Eve", output)
        self.assertIn("Eligible for discount", output)
        self.assertIn("Priority Customer", output)

    def test_vip_customer_label(self):
        cm = CustomerManager()
        cm.add_customer("Frank", [{'price': 900}])  # taxed to 1080 -> VIP Customer!

        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()
        self.assertIn("Frank", output)
        self.assertIn("VIP Customer!", output)

    def test_heavy_item_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 100, 'weight': 25}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 50)

    def test_heavy_items_shipping_fee_function(self):
        purchases = [{'price': 10, 'weight': 21}]
        self.assertEqual(calculate_shipping_fee_for_heavy_items(purchases), 50)

        purchases = [{'price': 10, 'weight': 20}]
        self.assertEqual(calculate_shipping_fee_for_heavy_items(purchases), 20)

    def test_fragile_item_shipping_fee(self):
        purchases = [{'price': 70, 'fragile': True}]

        fee = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee, 60)

    def test_no_special_items_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 40, 'weight': 5, 'fragile': False}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 20)

        fee_fragile = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee_fragile, 25)

if __name__ == "__main__":
    unittest.main()
