class GithubClientError(BaseException):
    def __init__(self, message: str):
        super().__init__(f"[GITHUB CLIENT ERROR] {message}")
