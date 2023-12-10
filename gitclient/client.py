import json
import logging
import os
from typing import Any, Dict, List, Optional

import requests

from .errors import ClientDataFetchError, ClientRequestError
from .models import GitHubCommit, GitHubRepo

logger = logging.getLogger(__name__)


class GithubClient:
    def __init__(self, user: str, version: str = "2022-11-28") -> None:
        self.__url = "https://api.github.com"
        self.__user = user
        self.__token = os.getenv("GITHUB_TOKEN")
        self.__api_version = version
        logger.debug(f"GithubClient created for user {self.__user}")

    def __make_base_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """Base request method for interacting with Github API.

        Args:
            method (str): request method
            endpoint (str): URL endpoint for API
            params (Dict[str, Any], optional): Additional request params, defaults to None
            data (Dict[str, Any], optional): Additional request data, defaults to None
            headers (Dict[str, Any], optional): Additional request headers, defaults to None

        Returns:
            requests.Response: Request response data
        """
        url = f"{self.__url}/{endpoint}"
        response = requests.request(
            method, url, params=params, data=data, headers=headers
        )
        return response

    def __make_authenticated_request(
        self, method: str, endpoint: str
    ) -> Dict[str, Any]:
        """Make an authenticated request to the API.

        Args:
            method (str): request method
            endpoint (str): URL endpoint for API

        Raises:
            Exception: If the response status code is 400 and up
            ClientRequestError: If any error is propagated

        Returns:
            Dict[str, Any]: JSON data
        """
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.__token}",
            "X-GitHub-Api-Version": self.__api_version,
        }

        try:
            response = self.__make_base_request(
                method=method.upper(), endpoint=endpoint, headers=headers
            )

            if response.status_code >= 400:
                raise Exception(f"{response.status_code} - {response.text}")

            return response.json()

        except Exception as error:
            raise ClientRequestError(
                f"Failed to make authenticated request: {error}"
            ) from error

    def get_user_info(self) -> Dict[str, Any]:
        """Fetch user information.

        Returns:
            Dict[str, Any]: JSON data about the user
        """
        endpoint = f"users/{self.__user}"
        return self.__make_base_request("GET", endpoint).json()

    def get_user_repo_info(self) -> List[GitHubRepo]:
        """Retrieve repository information.

        Raises:
            ClientDataFetchError: if any request error occurs

        Returns:
            List[GitHubRepo]: List of repositories for user
        """
        endpoint = f"users/{self.__user}/repos"
        response = self.__make_base_request("GET", endpoint)
        data = response.json()
        repositories = []

        try:
            repositories = [GitHubRepo(**repo) for repo in data]
            logger.debug(f"Found {len(repositories)} repositories")

        except Exception as error:
            raise ClientDataFetchError("Failed to fetch list of repos") from error

        return repositories

    def get_repo_commits(self, repository: str) -> List[GitHubCommit]:
        """Get a list of commits for a given repository.

        Args:
            repository (str): repository to fetch commits from

        Returns:
            List[GitHubCommit]: List of commits for the given repository
        """
        endpoint = f"repos/{self.__user}/{repository}/commits"
        data = self.__make_authenticated_request("GET", endpoint)
        commits_list = [GitHubCommit(**repo) for repo in data]
        logger.debug(f"Found {len(commits_list)} commits in '{repository}'")
        return commits_list
