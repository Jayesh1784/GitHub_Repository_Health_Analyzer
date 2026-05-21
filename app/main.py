import argparse
from app.core.logger import setup_logger
from app.core.scoring import HealthScorer
from app.integrations.git_client import GitClient
from app.analyzers.repo_analyzer import RepoAnalyzer
from app.analyzers.code_quality import CodeQualityAnalyzer
from app.analyzers.security import SecurityAnalyzer
from app.analyzers.branch_health import BranchHealthAnalyzer
from app.analyzers.collaboration import CollaborationAnalyzer   # NEW
from app.analyzers.devops import DevOpsAnalyzer                 # NEW
from app.report.generator import ReportGenerator

def main():
    parser = argparse.ArgumentParser(
        description="GitHub Repository Health Analyzer"
    )
    parser.add_argument("--repo", required=True, help="GitHub repository URL")
    args = parser.parse_args()

    logger = setup_logger()
    logger.info(f"Starting analysis for: {args.repo}")

    repo = GitClient(args.repo).clone()
    repo_path = repo.working_tree_dir

    # Run all analyzers
    repo_metrics     = RepoAnalyzer(repo).analyze()
    code_metrics     = CodeQualityAnalyzer(repo).analyze()
    security_metrics = SecurityAnalyzer(repo_path).analyze()
    branch_metrics   = BranchHealthAnalyzer(repo).analyze()
    collab_metrics   = CollaborationAnalyzer(repo).analyze()   # NEW
    devops_metrics   = DevOpsAnalyzer(repo_path).analyze()     # NEW

    metrics = {
        "code_quality":  code_metrics["score"],
        "collaboration": collab_metrics["score"],              # ✅ calculated
        "devops":        devops_metrics["score"],              # ✅ calculated
        "security":      security_metrics["score"],
        "branch":        branch_metrics["score"],
    }

    result = HealthScorer().calculate_score(metrics)

    report = {
        "repository": args.repo,
        "final_score": result,
        "details": {
            "code_quality":  code_metrics.get("details", {}),
            "collaboration": collab_metrics["details"],
            "devops":        devops_metrics["details"],
            "security":      security_metrics.get("details", {}),
            "branch":        branch_metrics.get("details", {}),
        }
    }

    ReportGenerator().generate(report)
    logger.info(f"Health Score: {result['total_score']}/100")

if __name__ == "__main__":
    main()
