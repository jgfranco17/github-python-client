class GithubClientError(BaseException):
    def __init__(self, identifier: str, message: str):
        super().__init__(f"[{identifier}] {message}")


class ClientDataFetchError(GithubClientError):
    def __init__(self, message: str):
        super().__init__(identifier="ClientFetchError", message=message)
