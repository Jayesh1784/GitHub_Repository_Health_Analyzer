import os

class DevOpsAnalyzer:
    def __init__(self, repo_path: str):
        self.path = repo_path

    def analyze(self) -> dict:
        score = 0
        details = {}

        # CI/CD config detection (30 pts)
        ci_files = [
            ".github/workflows",        # GitHub Actions
            ".gitlab-ci.yml",           # GitLab CI
            "Jenkinsfile",              # Jenkins
            ".circleci/config.yml",     # CircleCI
            ".travis.yml",              # Travis CI
            "azure-pipelines.yml",      # Azure DevOps
        ]
        found_ci = [f for f in ci_files if os.path.exists(os.path.join(self.path, f))]
        details["ci_configs_found"] = found_ci
        score += 30 if found_ci else 0

        # Dockerfile / containerization (20 pts)
        has_docker = os.path.exists(os.path.join(self.path, "Dockerfile")) or \
                     os.path.exists(os.path.join(self.path, "docker-compose.yml"))
        details["containerized"] = has_docker
        score += 20 if has_docker else 0

        # README exists (15 pts)
        has_readme = any(
            os.path.exists(os.path.join(self.path, f))
            for f in ["README.md", "README.rst", "README.txt", "README"]
        )
        details["has_readme"] = has_readme
        score += 15 if has_readme else 0

        # .gitignore (10 pts)
        has_gitignore = os.path.exists(os.path.join(self.path, ".gitignore"))
        details["has_gitignore"] = has_gitignore
        score += 10 if has_gitignore else 0

        # Requirements / dependency file (15 pts)
        dep_files = ["requirements.txt", "Pipfile", "pyproject.toml",
                     "package.json", "pom.xml", "build.gradle"]
        found_deps = [f for f in dep_files if os.path.exists(os.path.join(self.path, f))]
        details["dependency_files"] = found_deps
        score += 15 if found_deps else 0

        # Tests directory (10 pts)
        has_tests = os.path.isdir(os.path.join(self.path, "tests")) or \
                    os.path.isdir(os.path.join(self.path, "test"))
        details["has_tests"] = has_tests
        score += 10 if has_tests else 0

        return {"score": min(score, 100), "details": details}
