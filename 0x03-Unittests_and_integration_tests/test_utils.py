#!/usr/bin/env python3
""" unit testing for utiles.py """


import unittest
from unittest.mock import patch
from parameterized import parameterized
from utils import (
    access_nested_map,
    get_json,
)
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)


class TestAccessNestedMap(unittest.TestCase):
    """To test utils.access_nested_map function
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(
        self, nested_map: Mapping, path: Sequence, expected: Any
    ) -> None:
        """Test Access nested map with key path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(
            self, nested_map: Mapping, path: Sequence
    ) -> None:
        """Test that a KeyError is raised
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """To test utils.get_json
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(
        self, url: str, expected: Dict, mock_get: Callable
    ) -> None:
        """to test that utils.get_json returns the expected result.
        """
        mock_get.return_value.json.return_value = expected
        self.assertEqual(get_json(url), expected)
        mock_get.assert_called_once_with(url)