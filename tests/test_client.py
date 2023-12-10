from unittest.mock import Mock, patch

import pytest

from gitclient.errors import ClientDataFetchError
from gitclient.models import GitHubCommit, GitHubRepo


def test_make_base_request(github_client):
    with patch("requests.request") as mock_request:
        mock_response = Mock(
            status_code=200, json=Mock(return_value={"mock_key": "mock_value"})
        )
        mock_request.return_value = mock_response

        response = github_client._GithubClient__make_base_request(
            method="GET",
            endpoint="test_endpoint",
            params={"param": "value"},
            data={"data_param": "data_value"},
            headers={"header_param": "header_value"},
        )

        assert response == {"mock_key": "mock_value"}

        mock_request.assert_called_once_with(
            "GET",
            "https://api.github.com/test_endpoint",
            params={"param": "value"},
            data={"data_param": "data_value"},
            headers={"header_param": "header_value"},
        )


def test_make_authenticated_request(github_client):
    with patch(
        "gitclient.GithubClient._GithubClient__make_base_request"
    ) as mock_base_request:
        mock_response = Mock(
            status_code=200, json=Mock(return_value={"mock_key": "mock_value"})
        )
        mock_base_request.return_value = mock_response

        response = github_client._GithubClient__make_authenticated_request(
            method="GET",
            endpoint="test_endpoint",
        )

        assert response == {"mock_key": "mock_value"}

        mock_base_request.assert_called_once_with(
            method="GET",
            endpoint="test_endpoint",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": "Bearer None",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )


def test_get_user_info(github_client):
    with patch(
        "gitclient.GithubClient._GithubClient__make_base_request"
    ) as mock_base_request:
        mock_response = Mock(
            status_code=200, json=Mock(return_value={"mock_key": "mock_value"})
        )
        mock_base_request.return_value = mock_response

        response = github_client.get_user_info()

        assert response == {"mock_key": "mock_value"}

        mock_base_request.assert_called_once_with(
            method="GET",
            endpoint="users/test_user",
        )


def test_get_user_repo_info(github_client):
    with patch(
        "gitclient.GithubClient._GithubClient__make_base_request"
    ) as mock_base_request:
        mock_response = Mock(
            status_code=200, json=Mock(return_value=[{"mock_key": "mock_value"}])
        )
        mock_base_request.return_value = mock_response

        response = github_client.get_user_repo_info()

        assert response == [GitHubRepo(mock_key="mock_value")]

        mock_base_request.assert_called_once_with(
            method="GET",
            endpoint="users/test_user/repos",
        )


def test_get_repo_commits(github_client):
    with patch(
        "gitclient.GithubClient._GithubClient__make_authenticated_request"
    ) as mock_authenticated_request:
        mock_response = Mock(
            status_code=200, json=Mock(return_value=[{"mock_key": "mock_value"}])
        )
        mock_authenticated_request.return_value = mock_response

        response = github_client.get_repo_commits("test_repo")

        assert response == [GitHubCommit(mock_key="mock_value")]

        mock_authenticated_request.assert_called_once_with(
            method="GET",
            endpoint="repos/test_user/test_repo/commits",
        )


def test_get_repo_commits_error(github_client):
    with patch(
        "gitclient.GithubClient._GithubClient__make_authenticated_request"
    ) as mock_authenticated_request:
        mock_response = Mock(status_code=404)
        mock_authenticated_request.return_value = mock_response

        with pytest.raises(ClientDataFetchError):
            github_client.get_repo_commits("test_repo")
