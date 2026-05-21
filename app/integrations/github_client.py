import requests

class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, token=None):
        self.headers = {
            "Authorization": f"token {token}"
        } if token else {}

    def get_contributors(self, owner, repo):
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/contributors"
        return requests.get(url, headers=self.headers).json()

    def get_pulls(self, owner, repo):
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/pulls?state=all"
        return requests.get(url, headers=self.headers).json()

    def get_issues(self, owner, repo):
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/issues?state=all"
        return requests.get(url, headers=self.headers).json()

