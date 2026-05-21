"""
GitHub Repository Health Analyzer
==================================
Entry point. Orchestrates all analyzers, aggregates metrics, calculates
the composite health score, and triggers report generation.
"""

import argparse
import sys
import time

from app.core.logger import setup_logger
from app.core.scoring import HealthScorer
from app.integrations.git_client import GitClient
from app.analyzers.repo_analyzer import RepoAnalyzer
from app.analyzers.code_quality import CodeQualityAnalyzer
from app.analyzers.security import SecurityAnalyzer
from app.analyzers.branch_health import BranchHealthAnalyzer
from app.analyzers.collaboration import CollaborationAnalyzer
from app.analyzers.devops import DevOpsAnalyzer
from app.report.generator import ReportGenerator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="repo-health",
        description="GitHub Repository Health Analyzer — automated DevOps quality scoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --repo https://github.com/org/repo
  python main.py --repo https://github.com/org/repo --output html
  python main.py --repo https://github.com/org/repo --branch develop
        """,
    )
    parser.add_argument(
        "--repo",
        required=True,
        metavar="URL",
        help="GitHub (or any Git) repository URL to analyze",
    )
    parser.add_argument(
        "--branch",
        default=None,
        metavar="BRANCH",
        help="Branch to analyze (defaults to the repository's default branch)",
    )
    parser.add_argument(
        "--output",
        choices=["json", "html", "both"],
        default="json",
        help="Report output format (default: json)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed per-analyzer output to the terminal",
    )
    return parser.parse_args()


def run_analyzer(label: str, fn, logger, verbose: bool):
    """Run a single analyzer, log timing, and return its result."""
    start = time.perf_counter()
    try:
        result = fn()
        elapsed = time.perf_counter() - start
        logger.info(f"[✓] {label:<30} score={result.get('score', 'N/A'):>6}  ({elapsed:.2f}s)")
        if verbose:
            logger.debug(f"    details: {result.get('details', {})}")
        return result
    except Exception as exc:
        elapsed = time.perf_counter() - start
        logger.warning(f"[!] {label:<30} FAILED ({elapsed:.2f}s): {exc}")
        return {"score": 0, "details": {"error": str(exc)}}


def main() -> int:
    args = parse_args()
    logger = setup_logger()

    logger.info("=" * 60)
    logger.info("  GitHub Repository Health Analyzer")
    logger.info("=" * 60)
    logger.info(f"  Repository : {args.repo}")
    if args.branch:
        logger.info(f"  Branch     : {args.branch}")
    logger.info("=" * 60)

    # ── 1. Clone ───────────────────────────────────────────────────────
    logger.info("Cloning repository …")
    try:
        repo = GitClient(args.repo).clone(branch=args.branch)
    except Exception as exc:
        logger.error(f"Failed to clone repository: {exc}")
        return 1

    repo_path = repo.working_tree_dir
    logger.info(f"Cloned to: {repo_path}\n")

    # ── 2. Run analyzers ───────────────────────────────────────────────
    logger.info("Running analyzers …")

    _repo_metrics = run_analyzer(
        "RepoAnalyzer",
        lambda: RepoAnalyzer(repo).analyze(),
        logger, args.verbose,
    )
    code_metrics = run_analyzer(
        "CodeQualityAnalyzer",
        lambda: CodeQualityAnalyzer(repo).analyze(),
        logger, args.verbose,
    )
    security_metrics = run_analyzer(
        "SecurityAnalyzer",
        lambda: SecurityAnalyzer(repo_path).analyze(),
        logger, args.verbose,
    )
    branch_metrics = run_analyzer(
        "BranchHealthAnalyzer",
        lambda: BranchHealthAnalyzer(repo).analyze(),
        logger, args.verbose,
    )
    collab_metrics = run_analyzer(
        "CollaborationAnalyzer",
        lambda: CollaborationAnalyzer(repo).analyze(),
        logger, args.verbose,
    )
    devops_metrics = run_analyzer(
        "DevOpsAnalyzer",
        lambda: DevOpsAnalyzer(repo_path).analyze(),
        logger, args.verbose,
    )

    # ── 3. Aggregate & score ───────────────────────────────────────────
    metrics = {
        "code_quality":  code_metrics["score"],
        "collaboration": collab_metrics["score"],   # ← now calculated
        "devops":        devops_metrics["score"],    # ← now calculated
        "security":      security_metrics["score"],
        "branch":        branch_metrics["score"],
    }

    result = HealthScorer().calculate_score(metrics)

    # ── 4. Build full report payload ───────────────────────────────────
    import datetime as _dt

    report = {
        "repository": args.repo,
        "branch": args.branch or repo.active_branch.name,
        "analyzed_at": _dt.datetime.utcnow().isoformat() + "Z",
        "final_score": result,
        "details": {
            "code_quality":  code_metrics.get("details", {}),
            "collaboration": collab_metrics.get("details", {}),
            "devops":        devops_metrics.get("details", {}),
            "security":      security_metrics.get("details", {}),
            "branch":        branch_metrics.get("details", {}),
        },
    }

    # ── 5. Generate reports ────────────────────────────────────────────
    logger.info("\nGenerating report …")
    ReportGenerator().generate(report, output_format=args.output)

    # ── 6. Summary ─────────────────────────────────────────────────────
    score = result["total_score"]
    grade = _grade(score)

    logger.info("\n" + "=" * 60)
    logger.info(f"  Final Health Score : {score:.1f} / 100  (Grade: {grade})")
    logger.info("  Breakdown:")
    for key, val in result["breakdown"].items():
        logger.info(f"    {key:<20} {val:>6.1f}")
    logger.info("=" * 60)

    return 0


def _grade(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    if score >= 45:
        return "D"
    return "F"


if __name__ == "__main__":
    sys.exit(main())
