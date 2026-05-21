from git import Repo
from collections import defaultdict
from datetime import datetime, timezone

class CollaborationAnalyzer:
    def __init__(self, repo: Repo):
        self.repo = repo

    def analyze(self) -> dict:
        commits = list(self.repo.iter_commits())
        if not commits:
            return {"score": 0, "details": {}}

        # 1. Contributor diversity (more unique authors = better)
        authors = set(c.author.email for c in commits)
        contributor_score = min(len(authors) * 10, 40)  # max 40 pts

        # 2. Commit frequency (commits per week over last 3 months)
        recent = [c for c in commits if (datetime.now(timezone.utc) - c.committed_datetime).days <= 90]
        weekly_avg = len(recent) / 12  # 12 weeks
        frequency_score = min(weekly_avg * 5, 30)  # max 30 pts

        # 3. PR/merge commit ratio (merges indicate code review culture)
        merges = [c for c in commits if len(c.parents) > 1]
        merge_ratio = len(merges) / len(commits) if commits else 0
        review_score = min(merge_ratio * 100, 30)  # max 30 pts

        total = round(contributor_score + frequency_score + review_score, 2)

        return {
            "score": total,
            "details": {
                "unique_contributors": len(authors),
                "recent_commits_90d": len(recent),
                "merge_commits": len(merges),
                "weekly_commit_avg": round(weekly_avg, 2),
            }
        }
