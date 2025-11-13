#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        mock_get_json.return_value = {"login": org_name}

        client_instance = GithubOrgClient(org_name)
        result = client_instance.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"login": org_name})

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL from org property"""
        org_name = "holberton"
        expected_url = "https://api.github.com/orgs/holberton/repos"
        payload = {"repos_url": expected_url}

        client_instance = GithubOrgClient(org_name)

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = payload

            result = client_instance._public_repos_url
            self.assertEqual(result, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns expected repo names"""
        org_name = "holberton"
        repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = repos_payload
        expected_repos = ["repo1", "repo2", "repo3"]

        client_instance = GithubOrgClient(org_name)

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "http://fakeurl.com/repos"

            result = client_instance.public_repos()

            self.assertEqual(result, expected_repos)
            self.assertEqual(mock_url.call_count, 1)
            mock_get_json.assert_called_once_with("http://fakeurl.com/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns correct boolean"""
        client_instance = GithubOrgClient("holberton")
        result = client_instance.has_license(repo, license_key)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
