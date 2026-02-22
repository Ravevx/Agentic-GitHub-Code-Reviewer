# Agentic GitHub Code Reviewer

> A fully local, privacy-safe multi-agent system that automatically reviews  
> any GitHub repository and generates a detailed code review report 
> powered by LangGraph + LM Studio.  
> **No API keys. No data leaves your machine.**

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green)
![LM Studio](https://img.shields.io/badge/LM%20Studio-Local%20LLM-purple)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-red)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20UI-orange)

---

##  What It Does

Give it any GitHub repository URL → it automatically:

- **Fetches** all source files via GitHub API  
- **Indexes** code into a ChromaDB vector store (RAG)  
- **Reviews** each file for bugs, security issues, performance problems  
- **Suggests** minimal, targeted code fixes  
- **Generates** a full markdown report with executive summary + score  

---

## Architecture

```
                        GitHub URL
                            ↓
┌──────────────────────────────────────────────────────┐
│              LangGraph State Machine                 │
│                                                      │
│  [FETCHER] → [REVIEWER] → [SUGGESTER] → [SUMMARISER] │
│      ↓            ↓            ↓             ↓       │
│  GitHub API    RAG Query    Fix Suggest   .md Report │
└──────────────────────────────────────────────────────┘
                            ↓
                 review_YYYYMMDD_HHMMSS.md
```

---

### Agent Roles

| Agent | Responsibility |
|------|----------------|
| **Fetcher** | Calls GitHub API, extracts code from notebooks, builds ChromaDB RAG index |
| **Reviewer** | Static analysis:- bugs, security, performance, readability |
| **Suggester** | Generates before/after code fixes |
| **Summariser** | Writes executive summary with verdict + score |

---

## Tech Stack

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

## Prerequisites

- Python **3.11+**
- LM Studio installed and running
- GitHub Personal Access Token
- Chat model loaded in LM Studio
- Embedding model loaded

---

## Setup & Installation

### 1️. Clone Repo
```bash
git clone https://github.com/Ravevx/Agentic-GitHub-Code-Reviewer.git
cd Agentic-GitHub-Code-Reviewer
```
### 2️. Create Environment
```bash
conda create -n agent-local python=3.11
conda activate agent-local
```

### 3️. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️. Create `.env`
```
GITHUB_TOKEN=your_token_here
```

### 5️. Configure Model
Edit `config.py`

```python
LM_MODEL = "your-model-name"
MAX_FILE_SIZE = 4000
MAX_FILES = 5
```

---

## Usage

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

## Example Output
```
   AI CODE REVIEW AGENT

[FETCHER] Fetching repository files from GitHub...
Repo: Machine-Learning
Loading 9 code files...
[FETCHER] Loaded 9 files

[RAG] Building code index...
Indexed 63 chunks from 9 files
[RAG] Code index ready!

[REVIEWER] Analysing code...
Reviewing: decision_tree.ipynb
Reviewing: logistic_regression.ipynb
[REVIEWER] Reviewed 9 files

[SUGGESTER] Generating fix suggestions...
[SUGGESTER] Generated suggestions for 9 files

[SUMMARISER] Writing final report...
[SUMMARISER] Report complete!

Report saved to: review_20260220_153700.md
```
Report output:
```
VERDICT: Approved with Minor Fixes
SCORE: 8.5/10
SECURITY RISK: Low

TOP ISSUES
• `train_claim_type.py` Data Leakage Risk
   - Line: `self.df = self.df[self.df["claim"] == 1].reset_index(drop=True)`
• `model_span.py` Dimension Mismatch
  - Line: `self.classifier = nn.Linear(hidden_size, 1)`
• `train_span.py` Unsafe Hardcoded Splits
```

---

##  Project Structure

```
i-Agentic-GitHub-Code-Reviewer/
│
├── main.py                  ← CLI runner
├── api.py                   ← FastAPI REST server
├── app.py                   ← Streamlit web UI
├── llm.py                   ← LM Studio LLM factory
├── config.py                ← Settings (URL, model, limits)
├── test_lm.py               ← LM Studio connection test
├── requirements.txt         ← Dependencies
├── .env                     ← GitHub token (not committed)
│
├── tools/
│   └── github_tools.py      ← GitHub API integration
│
├── rag/
│   └── code_store.py        ← ChromaDB vector index
│
├── graph/
│   └── review_graph.py      ← LangGraph pipeline
│
└── agents/
    ├── fetcher.py            ← Agent 1: Fetch + RAG
    ├── reviewer.py           ← Agent 2: Code review
    ├── suggester.py          ← Agent 3: Fix suggestions
    └── summariser.py         ← Agent 4: Final report
```

---

## Config Reference

| Setting | Default |
|--------|---------|
MAX_FILE_SIZE | 4000 |
MAX_FILES | 5 |
LM_MODEL | ministral-3b |
Context | 8192 |

---

## Troubleshooting

| Problem | Fix |
|--------|-----|
Model won't connect | Start LM Studio |
Timeout | Reduce file limits |
Token error | Increase Tokens |


---

## License
MIT License

---

## Credits

- LangGraph
- LM Studio
- ChromaDB
- GitHub API
