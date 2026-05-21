import os
from pathlib import Path


class DevOpsAnalyzer:
    """
    Analyzes DevOps readiness by inspecting the repository file structure.

    Scoring (100 pts total):
      CI/CD config       : 30 pts
      Containerisation   : 20 pts
      README             : 15 pts
      Dependency manifest: 15 pts
      Test suite         : 10 pts
      .gitignore         : 10 pts
    """

    CI_PATHS = [
        ".github/workflows",
        ".gitlab-ci.yml",
        "Jenkinsfile",
        ".circleci/config.yml",
        ".travis.yml",
        "azure-pipelines.yml",
        ".buildkite",
        "bitbucket-pipelines.yml",
    ]
    DOCKER_FILES = ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"]
    README_FILES = ["README.md", "README.rst", "README.txt", "README", "readme.md"]
    DEPENDENCY_FILES = [
        "requirements.txt", "Pipfile", "pyproject.toml", "setup.py",
        "package.json", "pom.xml", "build.gradle", "go.mod", "Cargo.toml", "Gemfile",
    ]
    TEST_DIRS = ["tests", "test", "spec", "__tests__", "e2e"]

    def __init__(self, repo_path: str):
        self.root = Path(repo_path)

    def analyze(self) -> dict:
        ci_score,      ci_info      = self._check_ci()
        docker_score,  docker_info  = self._check_docker()
        readme_score,  readme_info  = self._check_readme()
        dep_score,     dep_info     = self._check_dependencies()
        test_score,    test_info    = self._check_tests()
        ignore_score,  ignore_info  = self._check_gitignore()

        total = ci_score + docker_score + readme_score + dep_score + test_score + ignore_score

        return {
            "score": min(round(total, 2), 100),
            "details": {
                "ci_cd":          ci_info,
                "containerised":  docker_info,
                "documentation":  readme_info,
                "dependencies":   dep_info,
                "testing":        test_info,
                "gitignore":      ignore_info,
                "subscores": {
                    "ci_cd": ci_score, "docker": docker_score,
                    "readme": readme_score, "dependencies": dep_score,
                    "tests": test_score, "gitignore": ignore_score,
                },
            },
        }

    def _check_ci(self):
        found = [p for p in self.CI_PATHS if (self.root / p).exists()]
        workflows = 0
        wf_dir = self.root / ".github" / "workflows"
        if wf_dir.is_dir():
            workflows = sum(1 for f in wf_dir.iterdir() if f.suffix in {".yml", ".yaml"})
        return (30.0 if found else 0.0), {"configs_found": found, "workflow_count": workflows}

    def _check_docker(self):
        found = [f for f in self.DOCKER_FILES if (self.root / f).exists()]
        return (20.0 if found else 0.0), {"files_found": found}

    def _check_readme(self):
        found = next((f for f in self.README_FILES if (self.root / f).exists()), None)
        size = (self.root / found).stat().st_size if found else 0
        return (15.0 if found else 0.0), {"file": found, "size_bytes": size}

    def _check_dependencies(self):
        found = [f for f in self.DEPENDENCY_FILES if (self.root / f).exists()]
        return (15.0 if found else 0.0), {"files_found": found}

    def _check_tests(self):
        found_dirs = [d for d in self.TEST_DIRS if (self.root / d).is_dir()]
        test_files = []
        if not found_dirs:
            for p in list(self.root.rglob("test_*.py"))[:10] + list(self.root.rglob("*.test.js"))[:10]:
                test_files.append(str(p.relative_to(self.root)))
        has_tests = bool(found_dirs or test_files)
        return (10.0 if has_tests else 0.0), {"test_dirs": found_dirs, "test_files": test_files}

    def _check_gitignore(self):
        path = self.root / ".gitignore"
        lines = 0
        if path.exists():
            lines = sum(1 for l in path.read_text(errors="ignore").splitlines()
                        if l.strip() and not l.startswith("#"))
        return (10.0 if path.exists() else 0.0), {"exists": path.exists(), "active_rules": lines}
