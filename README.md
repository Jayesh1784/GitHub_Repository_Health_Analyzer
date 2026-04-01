# 🚀 GitHub Repository Health Analyzer
> A DevOps-focused tool to automate repository health analysis and improve code quality monitoring.

## 📌 Overview

This project is a **DevOps-based tool with both CLI and Web UI (Streamlit)** that analyzes the health of a GitHub repository by evaluating multiple engineering metrics such as:

* Code Quality
* Security
* Branch Management
* Collaboration & DevOps practices

It provides a **composite health score** along with a structured report, helping developers and teams assess repository quality.

---

## 🎯 Features

* 🔍 Repository cloning and analysis
* 📊 Code quality evaluation
* 🔐 Security analysis
* 🌿 Branch health inspection
* 🧮 Composite health scoring system
* 📄 Automated report generation
* 🌐 Interactive web UI using Streamlit
---

## ⚙️ How It Works

### 🔁 Workflow

1. User provides a GitHub repository URL
2. Repository is cloned locally
3. Multiple analyzers run:

   * RepoAnalyzer
   * CodeQualityAnalyzer
   * SecurityAnalyzer
   * BranchHealthAnalyzer
4. Metrics are aggregated
5. Health score is calculated
6. Report is generated

---

## 🧠 Architecture

```text
User Input → GitClient → Analyzers → HealthScorer → ReportGenerator
```

---

## 📂 Project Structure

```text
app/
├── core/
│   ├── logger.py
│   ├── scoring.py
│
├── analyzers/
│   ├── repo_analyzer.py
│   ├── code_quality.py
│   ├── security.py
│   ├── branch_health.py
│
├── integrations/
│   └── git_client.py
│
├── report/
│   └── generator.py
│
main.py
```

---

## ▶️ Usage

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Jayesh1784/DevOps-project.git
cd DevOps-project
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Run the analyzer

```bash
python main.py --repo https://github.com/username/repository
```

---


## ⚡ Quick Start (One-Click Run)

For ease of use, the project includes a shortcut command to launch the application.

### ▶️ Run the application

```bash
./run.command
```
## 📈 Sample Output


Health Score: 82



---

## 📊 Scoring System

The final score is computed using:

* Code Quality
* Security
* Branch Health
* Collaboration (placeholder)
* DevOps (placeholder)

---

## 🔐 Security Analysis

Analyzes repository for:

* Vulnerabilities
* Unsafe patterns
* Security risks

---

## 🌿 Branch Health

Evaluates:

* Branch activity
* Maintenance
* Structure

---

## 📄 Report Generation

Generates a summary report containing:

* Repository name
* Final health score
* Metrics breakdown

---
---

## 🌟 Key Highlights

* Modular architecture for scalability  
* Automated repository analysis  
* Real-time scoring system  
* CLI + Web UI support  
* Easy to use for both developers and non-technical users  

---

## 🔮 Future Improvements

* Add real collaboration metrics (PRs, commits)
* Integrate GitHub API
* Add visualization dashboard
* Export reports (PDF/HTML)
* Add CI/CD integration

---

## 🤝 Contributing

Contributions are welcome!

---

## 👨‍💻 Author

**Jayesh**
GitHub: https://github.com/Jayesh1784

---
