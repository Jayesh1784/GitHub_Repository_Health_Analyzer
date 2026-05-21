# 🩺 GitHub Repository Health Analyzer

> An automated DevOps tool that analyzes the engineering quality of any GitHub repository and produces a composite health score across five key dimensions.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit)](https://apprepositoryhealthanalyzer-mes9gzj57wsq7qpdrwb89z.streamlit.app/)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E)](LICENSE)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)

## 🌐 Live Demo

**[👉 Try it here](https://apprepositoryhealthanalyzer-mes9gzj57wsq7qpdrwb89z.streamlit.app/)**

Enter any public GitHub repository URL and get an instant health report.

## 📌 Overview

Maintaining a healthy repository is foundational to sustainable software delivery. This tool acts as an automated health check — it clones a GitHub repository and runs five independent analyzers across key engineering dimensions, then aggregates the results into a single, actionable score with a letter grade.

Built as a college internship project, it demonstrates end-to-end DevOps thinking: automated analysis, modular architecture, CLI tooling, and an interactive web interface deployed on Streamlit Cloud.

## 🎯 What Gets Measured

| Dimension | Weight | What It Captures |
|---|---|---|
| **Code Quality** | 20% | Complexity, duplication, style violations |
| **Security** | 20% | Hardcoded secrets, unsafe patterns, vulnerability signatures |
| **Branch Health** | 20% | Stale branches, naming conventions, merge hygiene |
| **Collaboration** | 20% | Contributor diversity, PR activity, issue engagement |
| **DevOps Readiness** | 20% | CI/CD configs, containerisation, README, dependency manifests, test suite |

> All five scores are **calculated dynamically** from the actual repository — nothing is hardcoded.

## 🏗️ Architecture
User Input (GitHub URL)
│
▼
GitClient ──── clones repo to /tmp
│
▼
┌────────────────────────────────────────────┐
│                 Analyzers                   │
│  CodeQualityAnalyzer   SecurityAnalyzer     │
│  BranchHealthAnalyzer  CollaborationAnalyzer│
│  DevOpsAnalyzer                             │
└────────────────────────────────────────────┘
│ 
▼
HealthScorer ──── weighted composite score
│
▼
ReportGenerator ──── report.json
│
▼
CLI output  /  Streamlit Web UI

## 📂 Project Structure
GitHub_Repository_Health_Analyzer/
├── app/
│   ├── core/
│   │   ├── logger.py
│   │   └── scoring.py
│   ├── analyzers/
│   │   ├── repo_analyzer.py
│   │   ├── code_quality.py
│   │   ├── security.py
│   │   ├── branch_health.py│   │   ├── collaboration.py
│   │   └── devops.py
│   ├── integrations/
│   │   ├── git_client.py
│   │   └── github_client.py
│   ├── report/
│   │   └── generator.py
│   ├── main.py
│   └── ui.py
├── .streamlit/
│   └── config.toml
├── requirements.txt
└── README.md
## ⚙️ How the Analyzers Work

### 🤝 Collaboration Analyzer
Fetches live data from the GitHub API:

| Sub-metric | Max pts | Method |
|---|---|---|
| Contributor diversity | 30 | Unique contributors, tiered scoring |
| Pull request activity | 40 | Number of PRs merged |
| Issue activity | 30 | Number of issues opened |

### 🛠️ DevOps Analyzer
Inspects the repository file structure:

| Check | Pts | Looks for |
|---|---|---|
| CI/CD config | 30 | `.github/workflows`, `.gitlab-ci.yml`, `Jenkinsfile`, CircleCI, Travis, Azure |
| Containerisation | 20 | `Dockerfile`, `docker-compose.yml` |
| README | 15 | `README.md` / `.rst` / `.txt` |
| Dependency manifest | 15 | `requirements.txt`, `package.json`, `pom.xml`, `go.mod`, etc. |
| Test suite | 10 | `tests/`, `test/`, `__tests__/`, `test_*.py`, `*.test.js` |
| `.gitignore` | 10 | Presence + count of active rules |

## 📊 Scoring System
Final Score = (code_quality  × 0.20)
+ (security       × 0.20)
+ (branch         × 0.20)
+ (collaboration  × 0.20)
+ (devops         × 0.20)
| Score | Grade | Interpretation |
|---|---|---|
| 90 – 100 | **A** | Excellent — production-ready practices |
| 75 – 89  | **B** | Good — minor improvements recommended |
| 60 – 74  | **C** | Fair — several areas need attention |
| 45 – 59  | **D** | Poor — significant technical debt |
| 0 – 44   | **F** | Critical — immediate action required |

## ▶️ Run Locally

```bash
git clone https://github.com/Jayesh1784/GitHub_Repository_Health_Analyzer.git
cd GitHub_Repository_Health_Analyzer
pip install -r requirements.txt
export GITHUB_TOKEN=your_github_token_here
python3 -m streamlit run app/ui.py
```

### CLI

```bash
python3 -m app.main --repo https://github.com/username/repository
```

## 🚀 Deployment

Deployed on **Streamlit Cloud**: https://apprepositoryhealthanalyzer-mes9gzj57wsq7qpdrwb89z.streamlit.app/

To deploy your own instance:
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub
3. Set **Main file path** to `app/ui.py`
4. Add `GITHUB_TOKEN` in Secrets under Advanced Settings
5. Click Deploy

## 🗺️ Roadmap

- [ ] PDF export of health reports
- [ ] Trend tracking across runs over time
- [ ] Dependency vulnerability lookup via OSV / Snyk API
- [ ] Support for GitLab and Bitbucket URLs
- [ ] Docker image for zero-install usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-improvement`)
3. Commit with a clear message
4. Open a pull request

## 👨‍💻 Author

**Jayesh** — [@Jayesh1784](https://github.com/Jayesh1784)

*Built as a college internship project to demonstrate automated DevOps tooling and repository quality monitoring.*
