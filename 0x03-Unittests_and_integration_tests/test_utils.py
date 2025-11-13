#!/usr/bin/env python3
"""
Unit tests for utils.access_nested_map
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for utils.access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns the expected result"""
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == "__main__":
    unittest.main()

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b")
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_key):
        """Test that KeyError is raised with the correct message"""
        with self.assertRaises(KeyError) as error:
            access_nested_map(nested_map, path)

        self.assertEqual(str(error.exception), f"'{expected_key}'")
