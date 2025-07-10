# Ollama Job Interviewer

> **Generate rich job descriptions and instantly rank incoming résumés with a local Ollama LLM.**  
> Provide a one-line job title and a folder of PDF résumés—receive a complete JD plus a ranked applicant list in seconds.

[![Python](https://img.shields.io/badge/python-3.9%20%E2%80%93%203.13-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/github/license/YOURORG/ollama-job-interviewer)](#license)
[![CI](https://github.com/YOURORG/ollama-job-interviewer/actions/workflows/ci.yml/badge.svg)](https://github.com/YOURORG/ollama-job-interviewer/actions)

---

## ✨ Features

- **One‑shot Job Description** – transforms a job title into a multi‑section JD (overview, responsibilities, must‑haves, nice‑to‑haves, daily routine).  
- **PDF Résumé Extraction** – converts PDF résumés to plain text via *pypdf*.  
- **LLM‑powered Ranking** – prompts the LLM to order applicants by best fit.  
- **CLI & Python API** – run from the terminal *or* integrate as a library.  
- **Editable Install Friendly** – `pip install -e .` for rapid iteration.

---

## 🚀 Quick Start

### 1 Start Ollama

```bash
ollama serve                         # default: http://localhost:11434
ollama pull gemma3:latest            # or any compatible model
```

### 2 Install the package

```bash
git clone https://github.com/YOURORG/ollama-job-interviewer.git
cd ollama-job-interviewer
python -m pip install -e .[dev]      # editable + dev deps
```

### 3 Run

```bash
python -m mainPackage "IT Manager" resumes/alice.pdf resumes/bob.pdf

# custom model / endpoint
python -m mainPackage --model llama3     --base-url http://127.0.0.1:11434     "Data Analyst" resumes/*.pdf
```

---

## 🛠 Library Usage

```python
from pathlib import Path
import mainPackage as mp

jd = mp.generate_job_description("Frontend Engineer")
ranking = mp.rank_applicants(jd, [Path("alice.pdf"), Path("bob.pdf")])

print(jd)
print(ranking)
```

---

## 📦 Installation Options

| Scenario | Command |
|----------|---------|
| Stable release (PyPI) | `pip install mainPackage` |
| Latest development build | `pip install git+https://github.com/YOURORG/ollama-job-interviewer.git` |
| Editable clone (contributing) | `pip install -e .[dev]` |

---

## 🧑‍💻 Contributing

1. Fork → feature branch → PR.  
2. Run `ruff`, `black`, and `pytest` before pushing.  
3. Ensure CI (GitHub Actions) passes and new code includes tests.

---

## 📄 License

Licensed under the **MIT License**. See the [`LICENSE`](LICENSE) file for full text.

---

> © 2025 YOUR NAME / YOUR ORG — Built with ❤️ and ☕
