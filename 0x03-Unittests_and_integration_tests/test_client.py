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
from fixtures import TEST_PAYLOAD
import unittest
from unittest.mock import (
    patch,
    PropertyMock,
)
from parameterized import (parameterized, parameterized_class)


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

    @patch('client.get_json')
    def test_public_repos(self, mock_get: Callable) -> None:
        """to unit-test GithubOrgClient.public_repos.
        """
        repos_url = "https://api.github.com/orgs/google/repos"
        mock_get.return_value = [
            {'name': 'hi'}, {'name': 'hello'}, {'name': 'world'}
        ]
        with patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock
        ) as mock_public:
            mock_public.return_value = repos_url
            a_client = GithubOrgClient('google')
            self.assertEqual(
                a_client.public_repos(),
                ['hi', 'hello', 'world']
            )
            mock_get.assert_called_once_with(repos_url)
            mock_public.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(
        self, repo: Dict[str, Dict], license_key: str, expected: bool
    ) -> None:
        """to unit-test GithubOrgClient.has_license.
        """
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    [
        TEST_PAYLOAD[0][0],
        TEST_PAYLOAD[0][1],
        TEST_PAYLOAD[0][2],
        TEST_PAYLOAD[0][3]
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ to test the GithubOrgClient.public_repos method
    in an integration test.
    """
    def setUpClass(self):
        """mock requests.get to return example payloads
        """
        get_patcher = patch('utils.requests.get')
        get_mock = get_patcher.start()
        my_client = GithubOrgClient('google')

        def side_effect(url: str) -> Any:
            """to make sure the mock of requests.get(url).json()
            returns the correct fixtures for the various values
            of url that you anticipate to receive.
            """
            org_url = "https://api.github.com/orgs/google"
            repos_url = self.org_payload['repos_url']
            respond = {
                org_url: self.org_payload,
                repos_url: self.repos_payload
            }
            return respond[url]

        get_mock.return_value.json.side_effect = side_effect

    def tearDownClass(self):
        """to stop the patcher.
        """
        get_patcher.stop()

    def test_public_repos(self)
