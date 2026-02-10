# 🚑 Agentic CI Healer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393.svg)](https://fastapi.tiangolo.com)
[![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-2088FF.svg)](https://github.com/features/actions)

> **Autonomous Self-Healing for CI/CD Pipelines** 🤖

An agentic, AI-driven system that automatically diagnoses CI/CD failures from real GitHub Actions logs and applies fixes by opening pull requests — closing the loop between failure detection and remediation.

---

## 📌 Overview

**Agentic CI Healer** is an autonomous DevOps agent that listens to GitHub Actions workflow failures in real time.

### When a pipeline fails, the system:

1. 📥 Fetches the actual CI logs from GitHub
2. 🔍 Extracts the root error context
3. 🧠 Uses an LLM (Gemini) to diagnose the failure
4. 🔧 Applies a fix to the codebase
5. 📤 Opens a pull request automatically

**The goal:** Reduce CI downtime and repetitive manual fixes by introducing an agentic reasoning loop into CI/CD workflows.

---



## 🏗️ System Architecture

```
GitHub Actions Failure
          ↓
GitHub Webhook Listener (FastAPI)
          ↓
Workflow Log Fetcher (GitHub API)
          ↓
Log Analyzer (Error Extraction)
          ↓
Reasoner (Gemini LLM)
          ↓
Fixer (Code / Config Patch)
          ↓
Pull Request Created
          ↓
CI Reruns Automatically
```

### Key Principles

- 📋 Real logs, not mocked errors
- 🔄 Agentic observe → reason → act loop
- 🔒 Idempotent processing per workflow run
- ⏱️ Rate-limited LLM usage
- 👥 Human approval via PRs

---

## 🧠 Agent Components

### 1. **Log Analyzer**
Extracts meaningful error context from raw CI logs (e.g., stack traces, import errors, missing dependencies).

### 2. **Reasoner (LLM)**
Uses Gemini to diagnose the root cause and propose a fix.

### 3. **Fixer**
Applies changes to the repository (e.g., dependency updates, config fixes) and opens a pull request.

### 4. **Verifier**
Checks confidence of the LLM output before applying fixes.

### 5. **Agentic Loop**
Coordinates retries, throttling, and safe execution of the healing process.

---

## ⚖️ Decision Logic

| Confidence Level | Action                        |
|------------------|-------------------------------|
| **Low**          | Escalate for manual review    |
| **Medium**       | Suggest fix via PR            |
| **High**         | Apply fix via PR              |

This ensures that risky changes are not auto-applied blindly.

---

## 📜 Auditability

Each healing cycle produces a clear trace:

1. ✅ Error extracted from logs
2. ✅ Diagnosis returned by LLM
3. ✅ Fix proposed and applied
4. ✅ Pull request URL

This makes every action **reviewable and debuggable**.

---

## 🧪 Example Flow

1. 🚨 A GitHub Actions workflow fails
2. 📡 Webhook event is received
3. 📥 Real logs are fetched for the failed run
4. 🔍 Error is extracted (e.g., `ModuleNotFoundError: No module named 'pytest'`)
5. 🧠 LLM diagnoses the issue as a missing dependency
6. 📝 `requirements.txt` is updated automatically
7. 🔀 A pull request is created with the fix
8. ✅ CI reruns after merge

---

## 💾 State & Safety

- ✅ Each workflow run is processed **once** (idempotent handling)
- ⏱️ LLM calls are **rate-limited** to avoid quota exhaustion
- ⚡ Background task execution prevents webhook timeouts
- 🛡️ Failures in the healing loop do **not crash** the webhook server

---

## 🛠️ Tech Stack

| Component          | Technology                          |
|--------------------|-------------------------------------|
| **Language**       | Python                              |
| **Web Framework**  | FastAPI                             |
| **Server**         | Uvicorn                             |
| **CI Integration** | GitHub Actions + Webhooks           |
| **LLM**            | Google Gemini API                   |
| **GitHub API**     | PyGithub + REST logs endpoint       |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- GitHub account with admin access to a repository
- Google Gemini API key
- GitHub Personal Access Token

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/agentic-ci-healer.git
cd agentic-ci-healer
```

2. **Create and activate virtual environment**

```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set environment variables**

```bash
export GEMINI_API_KEY=your_gemini_api_key
export GITHUB_TOKEN=your_github_token
export GITHUB_REPO=owner/repo
```

Or create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
GITHUB_TOKEN=your_github_token
GITHUB_REPO=owner/repo
```

5. **Run the webhook server**

```bash
python main.py
```

The server will start on `http://localhost:8000`

### Configure GitHub Webhook

1. Go to your repository **Settings** → **Webhooks** → **Add webhook**
2. Set **Payload URL** to: `http://your-server-url/github/webhook`
3. Set **Content type** to: `application/json`
4. Select **Let me select individual events** and choose:
   - ✅ Workflow runs
5. Click **Add webhook**

---

## 📁 Project Structure

```
agentic-ci-healer/
├── main.py                 # FastAPI webhook server
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── README.md              # This file
└── modules/
    ├── log_analyzer.py    # Error extraction logic
    ├── reasoner.py        # LLM diagnosis
    ├── fixer.py           # Code/config patching
    └── verifier.py        # Confidence checking
```

---

## 🔮 Future Improvements

- [ ] Duplicate PR prevention for identical fixes
- [ ] Pre-merge verification of fixes
- [ ] Support for more failure classes (test failures, infra issues)
- [ ] Multi-repository support
- [ ] Web dashboard for monitoring healing events
- [ ] Cloud deployment for 24/7 operation
- [ ] Slack/Discord notifications for healing events
- [ ] Machine learning-based confidence scoring
- [ ] Rollback mechanism for problematic fixes

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [Google Gemini](https://ai.google.dev/)
- Integrated with [GitHub Actions](https://github.com/features/actions)

---

## 📧 Contact

For questions or feedback, please open an issue or reach out to the maintainers.

---

<div align="center">

**Made with ❤️ by the DevOps Automation Community**

⭐ Star this repo if you find it helpful!

</div>
