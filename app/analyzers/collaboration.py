class CollaborationAnalyzer:
    def __init__(self, github_client, owner, repo):
        self.client = github_client
        self.owner = owner
        self.repo = repo

    def analyze(self):
        contributors = self.client.get_contributors(self.owner, self.repo)
        pulls = self.client.get_pulls(self.owner, self.repo)
        issues = self.client.get_issues(self.owner, self.repo)

        num_contributors = len(contributors)
        num_prs = len(pulls)
        num_issues = len(issues)

        # scoring logic
        score = 0

        score += min(30, num_contributors * 10)   # contributors weight
        score += min(40, num_prs * 2)            # PR activity
        score += min(30, num_issues * 1)         # issue activity

        return {
            "contributors": num_contributors,
            "pull_requests": num_prs,
            "issues": num_issues,
            "score": min(score, 100),
        }

