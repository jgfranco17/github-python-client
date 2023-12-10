import json
import os
from http import HTTPStatus
from typing import Any, Dict

import requests

from .errors import ClientDataFetchError, ClientRequestError


class GithubClient:
    def __init__(self, user: str, version: str = "2022-11-28") -> None:
        self.__url = "https://api.github.com"
        self.__user = user
        self.__token = os.getenv("GITHUB_TOKEN")
        self.__api_version = version

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
        return self.__make_base_request("GET", endpoint)

    def print_user_info(self) -> None:
        try:
            data_json = self.get_user_info()
            pretty_json = json.dumps(data_json, indent=2)
            print(pretty_json)

        except ValueError as ve:
            raise ClientDataFetchError(
                f"Unable to parse response as JSON. Content:\n{data_json.text}"
            ) from ve

    def get_repo_info(self, owner, repo) -> Dict[str, Any]:
        endpoint = f"repos/{owner}/{repo}"
        return self.__make_base_request("GET", endpoint)
