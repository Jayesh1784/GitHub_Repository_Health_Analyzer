from git import Repo
import os
import shutil
import tempfile

class GitClient:
    def __init__(self, repo_url, local_path=None):
        self.repo_url = repo_url
        # Use /tmp so it works both locally and on Streamlit Cloud
        self.local_path = local_path or os.path.join(tempfile.gettempdir(), "repo_health_analyzer")

    def clone(self, branch=None):
        if os.path.exists(self.local_path):
            shutil.rmtree(self.local_path)

        print("Cloning repository...")
        kwargs = {}
        if branch:
            kwargs["branch"] = branch
        repo = Repo.clone_from(self.repo_url, self.local_path, **kwargs)
        print("Clone completed")
        return repo
