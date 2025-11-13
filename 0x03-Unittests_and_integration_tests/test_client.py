#!/usr/bin/env python3
"""
Unit tests for client.GithubOrgClient
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch
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
        # Configure the mock to return a sample payload
        mock_get_json.return_value = {"login": org_name}

        # Create client instance
        client_instance = GithubOrgClient(org_name)

        # Call the org property
        result = client_instance.org

        # Assert get_json was called once with the expected URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        # Assert the result is the mocked return value
        self.assertEqual(result, {"login": org_name})


if __name__ == "__main__":
    unittest.main()
    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL from org property"""
        org_name = "holberton"
        expected_url = "https://api.github.com/orgs/holberton/repos"
        payload = {"repos_url": expected_url}

        client_instance = GithubOrgClient(org_name)

        # Patch the 'org' property of the instance
        with patch.object(
            GithubOrgClient, "org", new_callable=property
        ) as mock_org:
            mock_org.return_value = payload

            result = client_instance._public_repos_url

            self.assertEqual(result, expected_url)
