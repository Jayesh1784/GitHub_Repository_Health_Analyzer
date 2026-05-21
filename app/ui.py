import streamlit as st
import json
import subprocess
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_PATH = os.path.join(PROJECT_ROOT, "report.json")

st.title("🚀 GitHub Repository Health Analyzer")

repo_url = st.text_input("Enter GitHub Repository URL")

if st.button("Analyze Repository"):
    if repo_url:
        with st.spinner("Cloning and analyzing repository..."):
            result = subprocess.run(
                f"python3 -m app.main --repo {repo_url}",
                shell=True,
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True
            )

        if result.returncode != 0:
            st.error("Analysis failed. See details below:")
            st.code(result.stderr)
        else:
            if not os.path.exists(REPORT_PATH):
                st.error("Report file not found. Something went wrong.")
                st.code(result.stdout)
            else:
                with open(REPORT_PATH) as f:
                    data = json.load(f)

                st.success("Analysis Complete ✅")

                score = data["final_score"]["total_score"]
                grade = data.get("grade", "N/A")

                col1, col2 = st.columns(2)
                col1.metric("Health Score", f"{score:.1f} / 100")
                col2.metric("Grade", grade)

                st.subheader("Score Breakdown")
                breakdown = data["final_score"]["breakdown"]
                for metric, value in breakdown.items():
                    st.progress(int(value), text=f"{metric.replace('_', ' ').title()}: {value:.1f}")

                st.subheader("Full Report")
                st.json(data)
    else:
        st.warning("Please enter a repository URL")
