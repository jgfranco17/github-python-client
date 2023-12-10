from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class License(BaseModel):
    key: str
    name: str


class GitHubRepo(BaseModel):
    id: int
    name: str
    full_name: str
    owner: dict  # You might want to create a Pydantic model for owner too
    private: bool
    html_url: str
    description: Optional[str] = None
    fork: bool
    url: str
    created_at: str
    updated_at: str
    pushed_at: str
    size: int
    stargazers_count: int
    watchers_count: int
    language: Optional[str] = None
    forks_count: int
    open_issues_count: int
    master_branch: Optional[str] = None
    default_branch: str
    score: Optional[float] = None
    archived: Optional[bool] = None
    disabled: Optional[bool] = None
    license: Optional[License] = None
    topics: List[str] = []

    def __str__(self) -> str:
        return f"<GithubRepo id={self.id} name={self.name}>"


class Commit(BaseModel):
    author: Dict[str, Any]
    committer: Dict[str, Any]
    message: str
    tree: dict
    url: str


class GitHubCommit(BaseModel):
    sha: str
    node_id: str
    commit: Commit
    url: str
    html_url: str
    comments_url: str
    author: Dict[str, Any]
    committer: Dict[str, Any]
    parents: List[dict]

    def __str__(self) -> str:
        return f"<GithubCommit SHA={self.sha} url={self.url}>"
