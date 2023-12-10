import json
import logging
import os
from http import HTTPStatus
from typing import Any, Dict, List

import requests

from .errors import ClientDataFetchError, ClientRequestError
from .models import GitHubRepo

logger = logging.getLogger(__name__)


class GithubClient:
    def __init__(self, user: str, version: str = "2022-11-28") -> None:
        self.__url = "https://api.github.com"
        self.__user = user
        self.__token = os.getenv("GITHUB_TOKEN")
        self.__api_version = version
        logger.debug(f"GithubClient created for user {self.__user}")

    def __make_base_request(
        self, method, endpoint, params=None, data=None, headers=None
    ) -> requests.Response:
        url = f"{self.__url}/{endpoint}"
        response = requests.request(
            method, url, params=params, data=data, headers=headers
        )
        return response

    def __make_authenticated_request(
        self, method: str, endpoint: str
    ) -> Dict[str, Any]:
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.__token}",
            "X-GitHub-Api-Version": self.__api_version,
        }

        response = self.__make_base_request(
            method=method.upper(), endpoint=endpoint, headers=headers
        )
        return response.json()

    def get_user_info(self) -> Dict[str, Any]:
        endpoint = f"users/{self.__user}"
        return self.__make_base_request("GET", endpoint).json()

    def print_user_info(self) -> None:
        try:
            data_json = self.get_user_info()
            pretty_json = json.dumps(data_json, indent=2)
            print(pretty_json)

        except ValueError as ve:
            raise ClientDataFetchError(
                f"Unable to parse response as JSON. Content:\n{data_json.text}"
            ) from ve

    def get_user_repo_info(self) -> List[GitHubRepo]:
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
