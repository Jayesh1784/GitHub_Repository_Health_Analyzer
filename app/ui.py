import streamlit as st
import json
import subprocess

st.title("🚀 Git Repository Health Checker")

repo_url = st.text_input("Enter GitHub Repository URL")

if st.button("Analyze Repository"):
    if repo_url:
        st.write("Running analysis...")

        # Run your backend
        subprocess.run(f"python3 -m app.main --repo {repo_url}", shell=True)

        # Load report
        with open("report.json") as f:
            data = json.load(f)

        st.success("Analysis Complete ✅")

        st.subheader("Final Score")
        st.write(data["final_score"])

        st.subheader("Metrics")
        st.json(data["metrics"])

    else:
        st.warning("Please enter a repository URL")
