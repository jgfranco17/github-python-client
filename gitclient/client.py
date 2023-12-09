from http import HTTPStatus

import requests


class GithubClient:
    def __init__(self, user: str) -> None:
        self.__url = "https://api.github.com/"
        self.__user = user

    def __make_request(self, method, endpoint, params=None, data=None, headers=None):
        url = f"{self.__url}/{endpoint}"
        response = requests.request(
            method, url, params=params, data=data, headers=headers
        )

        if response.status_code == HTTPStatus.OK:
            return response.json()

        else:
            response.raise_for_status()

    def get_user_info(self):
        endpoint = f"users/{self.__user}"
        return self.__make_request("GET", endpoint)

    def get_repo_info(self, owner, repo):
        endpoint = f"repos/{owner}/{repo}"
        return self.__make_request("GET", endpoint)
