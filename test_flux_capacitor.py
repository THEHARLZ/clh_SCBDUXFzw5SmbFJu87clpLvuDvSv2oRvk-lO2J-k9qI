#!/usr/bin/env python3
"""Tests for the Flux Capacitor Calculator."""

import unittest
from flux_capacitor import calculate_power_status, GIGAWATTS_REQUIRED


class TestFluxCapacitor(unittest.TestCase):
    """Test cases for flux capacitor calculations."""

    def test_sufficient_power(self):
        """Test when we have enough power (1.21 gigawatts or more)."""
        result = calculate_power_status(1.21)
        self.assertTrue(result["ready"])
        self.assertEqual(result["surplus_gigawatts"], 0.0)

    def test_excess_power(self):
        """Test when we have more than enough power."""
        result = calculate_power_status(2.0)
        self.assertTrue(result["ready"])
        self.assertEqual(result["surplus_gigawatts"], 0.79)
        self.assertIn("Great Scott", result["message"])

    def test_insufficient_power(self):
        """Test when we don't have enough power."""
        result = calculate_power_status(1.0)
        self.assertFalse(result["ready"])
        self.assertEqual(result["deficit_gigawatts"], 0.21)
        self.assertIn("need more power", result["message"])

    def test_no_power(self):
        """Test when we have no power."""
        result = calculate_power_status(0)
        self.assertFalse(result["ready"])
        self.assertEqual(result["deficit_gigawatts"], GIGAWATTS_REQUIRED)

    def test_gigawatts_constant(self):
        """Test that the required gigawatts is the iconic 1.21."""
        self.assertEqual(GIGAWATTS_REQUIRED, 1.21)


if __name__ == "__main__":
    unittest.main()
