import streamlit as st
import json
import os
import sys
import datetime

# Add project root to path so 'app' package is findable
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

REPORT_PATH = os.path.join(PROJECT_ROOT, "report.json")

st.title("🚀 GitHub Repository Health Analyzer")
repo_url = st.text_input("Enter GitHub Repository URL")

if st.button("Analyze Repository"):
    if repo_url:
        with st.spinner("Cloning and analyzing repository..."):
            try:
                from app.integrations.git_client import GitClient
                from app.integrations.github_client import GitHubClient
                from app.analyzers.code_quality import CodeQualityAnalyzer
                from app.analyzers.security import SecurityAnalyzer
                from app.analyzers.branch_health import BranchHealthAnalyzer
                from app.analyzers.collaboration import CollaborationAnalyzer
                from app.analyzers.devops import DevOpsAnalyzer
                from app.core.scoring import HealthScorer
                from app.report.generator import ReportGenerator

                def _grade(score):
                    if score >= 90: return "A"
                    if score >= 75: return "B"
                    if score >= 60: return "C"
                    if score >= 45: return "D"
                    return "F"

                repo = GitClient(repo_url).clone()
                repo_path = repo.working_tree_dir

                token = os.getenv("GITHUB_TOKEN")
                github = GitHubClient(token)
                parts = repo_url.rstrip("/").split("/")
                owner, repo_name = parts[-2], parts[-1].replace(".git", "")

                code_metrics     = CodeQualityAnalyzer(repo).analyze()
                security_metrics = SecurityAnalyzer(repo_path).analyze()
                branch_metrics   = BranchHealthAnalyzer(repo).analyze()
                collab_metrics   = CollaborationAnalyzer(github, owner, repo_name).analyze()
                devops_metrics   = DevOpsAnalyzer(repo_path).analyze()

                metrics = {
                    "code_quality":  code_metrics["score"],
                    "collaboration": collab_metrics["score"],
                    "devops":        devops_metrics["score"],
                    "security":      security_metrics["score"],
                    "branch":        branch_metrics["score"],
                }

                result = HealthScorer().calculate_score(metrics)
                grade  = _grade(result["total_score"])

                report = {
                    "repository":  repo_url,
                    "analyzed_at": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "final_score": result,
                    "grade":       grade,
                    "metrics":     metrics,
                    "details": {
                        "collaboration": collab_metrics,
                        "devops":        devops_metrics,
                        "security":      security_metrics.get("details", {}),
                        "branch":        branch_metrics.get("details", {}),
                    },
                }

                ReportGenerator().generate(report)

                st.success("Analysis Complete ✅")

                col1, col2 = st.columns(2)
                col1.metric("Health Score", f"{result['total_score']:.1f} / 100")
                col2.metric("Grade", grade)

                st.subheader("Score Breakdown")
                for metric, value in result["breakdown"].items():
                    st.progress(
                        int(value),
                        text=f"{metric.replace('_', ' ').title()}: {value:.1f} / 100"
                    )

                with st.expander("📋 Collaboration Details"):
                    st.json(collab_metrics)

                with st.expander("🛠️ DevOps Details"):
                    st.json(devops_metrics)

                with st.expander("🔐 Security Details"):
                    st.json(security_metrics)

                with st.expander("🌿 Branch Details"):
                    st.json(branch_metrics)

                with st.expander("📄 Full Report JSON"):
                    st.json(report)

            except Exception as e:
                st.error(f"Analysis failed: {e}")
                st.exception(e)
    else:
        st.warning("Please enter a repository URL")
