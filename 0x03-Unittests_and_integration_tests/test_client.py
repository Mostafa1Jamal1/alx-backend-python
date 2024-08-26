#!/usr/bin/env python3
"""Test cases for client module
"""

from typing import (
    List,
    Dict,
    Callable,
)
from utils import (
    get_json,
    access_nested_map,
    memoize,
)
from client import GithubOrgClient
import unittest
from unittest.mock import (
    patch,
    PropertyMock,
)
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """test GithubOrgClient.
    """
    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch('client.get_json')
    def test_org(org_name: str, self, mock_get: Callable) -> None:
        """test that GithubOrgClient.org returns the correct value.
        """
        a_client = GithubOrgClient(org_name)
        a_client.org()
        mock_get.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self) -> None:
        """to unit-test GithubOrgClient._public_repos_url.
        """
        with patch(
            'client.GithubOrgClient.org', new_callable=PropertyMock
        ) as org_mock:
            org_mock.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }
            a_client = GithubOrgClient('google')
            self.assertEqual(
                a_client._public_repos_url,
                "https://api.github.com/orgs/google/repos"
            )
