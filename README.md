# 🤖 AI Code Review Agent

> A fully local, privacy-safe multi-agent system that automatically reviews
> any GitHub repository and generates a detailed code review report
> powered by LangGraph + LM Studio. No API keys. No data leaves your machine.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green)
![LM Studio](https://img.shields.io/badge/LM%20Studio-Local%20LLM-purple)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-red)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20UI-orange)


## 📌 What It Does

Give it any GitHub repository URL → it automatically:

- 📥 **Fetches** all source files via GitHub API
- 🧠 **Indexes** code into a ChromaDB vector store (RAG)
- 🔍 **Reviews** each file for bugs, security issues, performance problems
- 💡 **Suggests** minimal, targeted code fixes
- 📋 **Generates** a full markdown report with executive summary + score


## 🏗️ Architecture


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


### Agent Roles

| Agent | Responsibility |
|---|---|
| **Fetcher** | Calls GitHub API, extracts code from notebooks, builds ChromaDB RAG index |
| **Reviewer** | Strict static analysis — BUGS, SECURITY, PERFORMANCE, READABILITY |
| **Suggester** | Generates before/after code fixes for every finding |
| **Summariser** | Writes executive summary with VERDICT, SCORE, estimated fix time |



## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | LangGraph |
| LLM Framework | LangChain + LangChain-OpenAI |
| Local LLM | LM Studio (Mistral / any model) |
| Embeddings | Nomic Embed Text (via LM Studio) |
| Vector Store | ChromaDB |
| Code Splitting | RecursiveCharacterTextSplitter (code-aware) |
| GitHub Integration | GitHub REST API v3 |
| Web UI | Streamlit |
| REST API | FastAPI + Uvicorn |



## ⚙️ Prerequisites

- Python 3.11+
- [LM Studio](https://lmstudio.ai/) installed and running
- A GitHub Personal Access Token
- A chat model loaded in LM Studio (e.g. `mistral-3b`)
- An embedding model loaded in LM Studio (e.g. `nomic-embed-text`)

---

## 🚀 Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-code-review-agent.git
cd ai-code-review-agent
```


### 2. Create and activate conda environment

```bash
conda create -n agent-local python=3.11
conda activate agent-local
```


### 3. Install dependencies

```bash
pip install -r requirements.txt
```


### 4. Create `.env` file

```bash
# .env
GITHUB_TOKEN=your_github_personal_access_token_here
```

> Get your token at: GitHub → Settings → Developer Settings → Personal Access Tokens

### 5. Configure LM Studio

- Open LM Studio → load a chat model (e.g. `Ministral 3B`)
- Load an embedding model (e.g. `nomic-embed-text`)
- Start the local server on `http://127.0.0.1:1234`
- Set **Context Length** to `8192` or higher in model settings


### 6. Update `config.py` with your model name

```python
LM_MODEL      = "your-model-name-in-lm-studio"
MAX_FILE_SIZE = 4000   # chars per file
MAX_FILES     = 5      # number of files to review
```


---

## ▶️ How to Run

### Option 1 — Command Line

```bash
python main.py
```

```
🔗 Enter GitHub PR URL: https://github.com/owner/repo
...
💾 Report saved to: review_20260220_153700.md
```


---

### Option 2 — Streamlit Web UI

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

```
1. Paste any GitHub repo URL
2. Click 🚀 Review PR
3. Wait ~2-5 minutes (depends on model + file count)
4. Download the .md report
```


---

### Option 3 — REST API

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

**Swagger docs:** `http://localhost:8000/docs`

**Example request:**

```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{"pr_url": "https://github.com/owner/repo"}'
```

**Example response:**

```json
{
  "status": "success",
  "report": "# 🤖 AI Code Review Report\n**Score:** 8.5/10 ..."
}
```


---

## 📊 Sample Output

```
═══════════════════════════════════════════════════════
   🤖 AI CODE REVIEW AGENT
═══════════════════════════════════════════════════════

🔍 [FETCHER] Fetching repository files from GitHub...
   📌 Repo: Machine-Learning | ⭐ 1 stars
   📂 Loading 9 code files...
✅ [FETCHER] Loaded 9 files

📚 [RAG] Building code index...
   📄 Indexed 63 chunks from 9 files
✅ [RAG] Code index ready!

🔎 [REVIEWER] Analysing code...
   🔍 Reviewing: decision_tree.ipynb
   🔍 Reviewing: logistic_regression.ipynb
✅ [REVIEWER] Reviewed 9 files

💡 [SUGGESTER] Generating fix suggestions...
✅ [SUGGESTER] Generated suggestions for 9 files

📋 [SUMMARISER] Writing final report...
✅ [SUMMARISER] Report complete!

💾 Report saved to: review_20260220_153700.md
```


### Report Preview

```
VERDICT: Approved with Minor Fixes
SCORE: 8.5/10
SECURITY RISK: Low

TOP 3 CRITICAL ISSUES:
- No input validation on file paths → path traversal risk
- Silent failures on empty DataFrames → AttributeError risk
- .tolist() on large datasets → memory inefficiency

ESTIMATED FIX TIME: 12–16 hours
```


---

## 📁 Project Structure

```
ai-code-review-agent/
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

## 🔧 Configuration Reference

| Setting | Default | Description |
| :-- | :-- | :-- |
| `MAX_FILE_SIZE` | `4000` | Max chars per file sent to LLM |
| `MAX_FILES` | `5` | Max files to review per run |
| `LM_STUDIO_URL` | `http://127.0.0.1:1234/v1` | LM Studio server URL |
| `LM_MODEL` | `ministral-3b` | Model name in LM Studio |
| Context Length | `8192` | Set in LM Studio model settings |


---

## ⚠️ Troubleshooting

| Error | Cause | Fix |
| :-- | :-- | :-- |
| `ConnectionRefusedError port 11434` | Ollama not running | Use LM Studio on port 1234 |
| `n_keep >= n_ctx` | Context window too small | Set LM Studio context to 8192+ |
| `ReadTimeout` | Files too large / model too slow | Reduce `MAX_FILE_SIZE` or `MAX_FILES` |
| `input must be a string` | Embedding format error | Add `check_embedding_ctx_length=False` |
| `cannot import text_splitter` | Old LangChain | `pip install langchain-text-splitters` |
| All files skipped | Extension not in list | Add extension to `CODE_EXTENSIONS` |


---

## 🔮 Future Improvements

- [ ] Async parallel file reviewing (9x speed improvement)
- [ ] Tree-sitter AST-based code chunking
- [ ] Persistent RAG cache (skip re-indexing same repo)
- [ ] Confidence scoring per finding
- [ ] LangGraph conditional branching (skip suggester for clean code)
- [ ] PR diff-only mode (review changed lines only)

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

## 🙏 Acknowledgements

- [LangGraph](https://github.com/langchain-ai/langgraph) — multi-agent orchestration
- [LM Studio](https://lmstudio.ai/) — local LLM inference
- [ChromaDB](https://www.trychroma.com/) — vector storage
- [GitHub REST API](https://docs.github.com/en/rest) — repository access

```

***

Save this as `README.md` in the root of your project, push to GitHub, and it will render beautifully. 🚀```

#   A g e n t i c - G i t H u b - C o d e - R e v i e w e r 
 
 
