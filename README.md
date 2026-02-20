# 🤖 AI Code Review Agent

> A fully local, privacy-safe multi-agent system that automatically reviews  
> any GitHub repository and generates a detailed code review report —  
> powered by LangGraph + LM Studio.  
> **No API keys. No data leaves your machine.**

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green)
![LM Studio](https://img.shields.io/badge/LM%20Studio-Local%20LLM-purple)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-red)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20UI-orange)

---

## 📌 What It Does

Give it any GitHub repository URL → it automatically:

- 📥 **Fetches** all source files via GitHub API  
- 🧠 **Indexes** code into a ChromaDB vector store (RAG)  
- 🔍 **Reviews** each file for bugs, security issues, performance problems  
- 💡 **Suggests** minimal, targeted code fixes  
- 📋 **Generates** a full markdown report with executive summary + score  

---

## 🏗️ Architecture

```
GitHub URL
↓
┌─────────────────────────────────────────────────┐
│              LangGraph State Machine             │
│                                                  │
│  [FETCHER] → [REVIEWER] → [SUGGESTER] → [SUMMARISER] │
│      ↓            ↓            ↓             ↓   │
│  GitHub API    RAG Query    Fix Suggest   .md Report│
└─────────────────────────────────────────────────┘
↓
review_YYYYMMDD_HHMMSS.md
```

---

### Agent Roles

| Agent | Responsibility |
|------|----------------|
| **Fetcher** | Calls GitHub API, extracts code from notebooks, builds ChromaDB RAG index |
| **Reviewer** | Static analysis — bugs, security, performance, readability |
| **Suggester** | Generates before/after code fixes |
| **Summariser** | Writes executive summary with verdict + score |

---

## 🛠 Tech Stack

| Layer | Technology |
|------|-------------|
| Agent Orchestration | LangGraph |
| LLM Framework | LangChain |
| Local LLM | LM Studio |
| Embeddings | Nomic Embed Text |
| Vector Store | ChromaDB |
| Web UI | Streamlit |
| REST API | FastAPI |

---

## ⚙️ Prerequisites

- Python **3.11+**
- LM Studio installed and running
- GitHub Personal Access Token
- Chat model loaded in LM Studio
- Embedding model loaded

---

## 🚀 Setup & Installation

### 1️⃣ Clone Repo
```bash
git clone https://github.com/yourusername/ai-code-review-agent.git
cd ai-code-review-agent
```

### 2️⃣ Create Environment
```bash
conda create -n agent-local python=3.11
conda activate agent-local
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Create `.env`
```
GITHUB_TOKEN=your_token_here
```

### 5️⃣ Configure Model
Edit `config.py`

```python
LM_MODEL = "your-model-name"
MAX_FILE_SIZE = 4000
MAX_FILES = 5
```

---

## ▶️ Usage

### CLI
```bash
python main.py
```

---

### Web UI
```bash
streamlit run app.py
```

---

### API
```bash
uvicorn api:app --reload
```

Docs → http://localhost:8000/docs

---

## 📊 Example Output

```
VERDICT: Approved with Minor Fixes
SCORE: 8.5/10
SECURITY RISK: Low

TOP ISSUES
• Missing validation
• Silent failures
• Memory inefficiency
```

---

## 📁 Project Structure

```
.
├── main.py
├── api.py
├── app.py
├── config.py
├── llm.py
├── requirements.txt
│
├── agents/
├── graph/
├── rag/
└── tools/
```

---

## 🔧 Config Reference

| Setting | Default |
|--------|---------|
MAX_FILE_SIZE | 4000 |
MAX_FILES | 5 |
LM_MODEL | ministral-3b |
Context | 8192 |

---

## ⚠️ Troubleshooting

| Problem | Fix |
|--------|-----|
Model won't connect | Start LM Studio |
Timeout | Reduce file limits |
Import error | Upgrade packages |

---

## 🔮 Roadmap

- Async reviewing
- AST chunking
- Cached indexing
- Confidence scores
- Conditional agents
- PR diff-only mode

---

## 📜 License
MIT License

---

## 🙏 Credits

- LangGraph
- LM Studio
- ChromaDB
- GitHub API
