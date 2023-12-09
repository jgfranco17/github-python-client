import requests


class GithubClient:
    def __init__(self, user: str) -> None:
        self.__url = "https://api.github.com/"
        self.__user = user
    
    def __make_request(self, method, endpoint, params=None, data=None, headers=None):
        url = f"{self.__url}/{endpoint}"
        response = requests.request(method, url, params=params, data=data, headers=headers)

        if response.status_code == 200:
            return response.json()

        else:
            response.raise_for_status()
