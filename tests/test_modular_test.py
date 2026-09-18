"""Tests for every input path and calculation in the modular auditor."""

import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

import modular_auditor  # noqa: E402


class GetValidInputTests(unittest.TestCase):
    def call_with(self, entry):
        output = io.StringIO()
        with patch("builtins.input", return_value=entry), redirect_stdout(output):
            result = modular_auditor.get_valid_input()
        return result, output.getvalue()

    def test_accepts_positive_integer(self):
        result, output = self.call_with("25")
        self.assertEqual(result, 25)
        self.assertEqual(output, "")

    def test_accepts_zero_and_surrounding_whitespace(self):
        result, _ = self.call_with("  0  ")
        self.assertEqual(result, 0)

    def test_quit_is_case_insensitive(self):
        result, output = self.call_with("  QuIt ")
        self.assertEqual(result, modular_auditor.QUIT)
        self.assertEqual(output, "")

    def test_rejects_negative_integer(self):
        result, output = self.call_with("-5")
        self.assertIsNone(result)
        self.assertIn("cannot be negative", output)

    def test_rejects_non_integer_entries(self):
        for entry in ("abc", "1.5", "+3", "", "5 units", "--2"):
            with self.subTest(entry=entry):
                result, output = self.call_with(entry)
                self.assertIsNone(result)
                self.assertIn("whole number", output)


class BusinessLogicTests(unittest.TestCase):
    def test_process_delivery_adds_to_total(self):
        self.assertEqual(modular_auditor.process_delivery(120, 30), 150)

    def test_process_delivery_handles_zero(self):
        self.assertEqual(modular_auditor.process_delivery(120, 0), 120)

    def test_calculate_tax_returns_ten_percent(self):
        self.assertAlmostEqual(modular_auditor.calculate_tax(125), 12.5)
        self.assertAlmostEqual(modular_auditor.calculate_tax(0), 0.0)

    def test_generate_report_prints_both_totals(self):
        output = io.StringIO()
        with redirect_stdout(output):
            modular_auditor.generate_report(75, 2)

        report = output.getvalue()
        self.assertIn("Total Units Processed: 75", report)
        self.assertIn("Number of Failed/Rejected Entries: 2", report)


class AuditorIntegrationTests(unittest.TestCase):
    def run_with(self, entries):
        output = io.StringIO()
        with patch("builtins.input", side_effect=entries), redirect_stdout(output):
            modular_auditor.run_auditor()
        return output.getvalue()

    def test_complete_session_counts_failures_and_calculates_tax(self):
        output = self.run_with(["10", "bad", "-4", "20", "quit"])

        self.assertIn("Tax for this delivery: 1.00", output)
        self.assertIn("Tax for this delivery: 2.00", output)
        self.assertIn("Current inventory: 30 units", output)
        self.assertIn("Total Units Processed: 30", output)
        self.assertIn("Number of Failed/Rejected Entries: 2", output)

    def test_overstock_alert_does_not_prevent_quit(self):
        output = self.run_with(["501", "1", "quit"])

        self.assertIn("OVERSTOCK ALERT", output)
        self.assertIn("Total Units Processed: 502", output)
        self.assertIn("Number of Failed/Rejected Entries: 0", output)

    def test_immediate_quit_produces_zero_summary(self):
        output = self.run_with(["quit"])

        self.assertIn("Total Units Processed: 0", output)
        self.assertIn("Number of Failed/Rejected Entries: 0", output)


if __name__ == "__main__":
    unittest.main()
