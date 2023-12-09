import json
import os
from http import HTTPStatus
from typing import Any, Dict

import requests

from .errors import ClientDataFetchError


class GithubClient:
    def __init__(self, user: str) -> None:
        self.__url = "https://api.github.com"
        self.__user = user
        self.__token = os.getenv("GITHUB_TOKEN")

    def __make_request(self, method, endpoint, params=None, data=None, headers=None):
        url = f"{self.__url}/{endpoint}"
        response = requests.request(
            method, url, params=params, data=data, headers=headers
        )

        if response.status_code == HTTPStatus.OK:
            return response.json()

        else:
            response.raise_for_status()

    def get_user_info(self) -> Dict[str, Any]:
        endpoint = f"users/{self.__user}"
        return self.__make_request("GET", endpoint)

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
        return self.__make_request("GET", endpoint)
