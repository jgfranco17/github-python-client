import pytest

from gitclient import GithubClient


@pytest.fixture
def github_client():
    return GithubClient(user="test_user", version="2022-11-28")
