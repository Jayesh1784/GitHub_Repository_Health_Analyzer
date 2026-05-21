import argparse
import os
import sys
import time
import datetime

from app.core.logger import setup_logger
from app.core.scoring import HealthScorer
from app.integrations.git_client import GitClient
from app.integrations.github_client import GitHubClient
from app.analyzers.repo_analyzer import RepoAnalyzer
from app.analyzers.code_quality import CodeQualityAnalyzer
from app.analyzers.security import SecurityAnalyzer
from app.analyzers.branch_health import BranchHealthAnalyzer
from app.analyzers.collaboration import CollaborationAnalyzer
from app.analyzers.devops import DevOpsAnalyzer
from app.report.generator import ReportGenerator


def _grade(score: float) -> str:
    if score >= 90: return "A"
    if score >= 75: return "B"
    if score >= 60: return "C"
    if score >= 45: return "D"
    return "F"


def main():
    parser = argparse.ArgumentParser(description="GitHub Repository Health Analyzer")
    parser.add_argument("--repo", required=True, help="GitHub repository URL")
    parser.add_argument("--verbose", action="store_true", help="Show detailed breakdown")
    args = parser.parse_args()

    logger = setup_logger()
    logger.info("=" * 55)
    logger.info("  GitHub Repository Health Analyzer")
    logger.info("=" * 55)
    logger.info(f"  Repository : {args.repo}")
    logger.info("=" * 55)

    # Clone
    logger.info("Cloning repository...")
    repo = GitClient(args.repo).clone()
    repo_path = repo.working_tree_dir

    # GitHub API (collaboration uses this)
    token = os.getenv("GITHUB_TOKEN")
    github = GitHubClient(token)
    parts = args.repo.rstrip("/").split("/")
    owner, repo_name = parts[-2], parts[-1].replace(".git", "")

    # Run all analyzers
    logger.info("\nRunning analyzers...")

    t = time.perf_counter()
    code_metrics = CodeQualityAnalyzer(repo).analyze()
    logger.info(f"  [✓] CodeQuality      score={code_metrics['score']:>6.1f}  ({time.perf_counter()-t:.2f}s)")

    t = time.perf_counter()
    security_metrics = SecurityAnalyzer(repo_path).analyze()
    logger.info(f"  [✓] Security         score={security_metrics['score']:>6.1f}  ({time.perf_counter()-t:.2f}s)")

    t = time.perf_counter()
    branch_metrics = BranchHealthAnalyzer(repo).analyze()
    logger.info(f"  [✓] BranchHealth     score={branch_metrics['score']:>6.1f}  ({time.perf_counter()-t:.2f}s)")

    t = time.perf_counter()
    collab_metrics = CollaborationAnalyzer(github, owner, repo_name).analyze()
    logger.info(f"  [✓] Collaboration    score={collab_metrics['score']:>6.1f}  ({time.perf_counter()-t:.2f}s)")

    t = time.perf_counter()
    devops_metrics = DevOpsAnalyzer(repo_path).analyze()
    logger.info(f"  [✓] DevOps           score={devops_metrics['score']:>6.1f}  ({time.perf_counter()-t:.2f}s)")

    # Score
    metrics = {
        "code_quality":  code_metrics["score"],
        "collaboration": collab_metrics["score"],
        "devops":        devops_metrics["score"],   # ← now calculated
        "security":      security_metrics["score"],
        "branch":        branch_metrics["score"],
    }

    result = HealthScorer().calculate_score(metrics)
    grade  = _grade(result["total_score"])

    # Build report
    report = {
        "repository":   args.repo,
        "analyzed_at":  datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "final_score":  result,
        "grade":        grade,
        "metrics":      metrics,
        "details": {
            "collaboration": collab_metrics,
            "devops":        devops_metrics,
            "security":      security_metrics.get("details", {}),
            "branch":        branch_metrics.get("details", {}),
        },
    }

    ReportGenerator().generate(report)

    # Summary
    logger.info("\n" + "=" * 55)
    logger.info(f"  Final Score : {result['total_score']:.1f} / 100   Grade: {grade}")
    logger.info("  Breakdown:")
    for k, v in result["breakdown"].items():
        logger.info(f"    {k:<20} {v:>6.1f}")
    logger.info("=" * 55)


if __name__ == "__main__":
    main()
