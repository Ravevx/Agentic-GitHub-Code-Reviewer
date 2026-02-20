# agents/reviewer.py
from langchain_core.prompts import ChatPromptTemplate
from llm import get_llm

llm = get_llm(temperature=0.1)

REVIEW_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a senior static code analysis engineer performing a STRICT, evidence-based code review.

PRIMARY OBJECTIVE:
Find REAL bugs and logic errors. Bug detection is your top priority.
You will be penalized for false positives.
Only report issues you are highly confident about.

CRITICAL RULES:
- Analyze ONLY the code shown in the FILE section below.
- Do NOT assume missing context.
- Do NOT invent functions, variables, or files.
- If uncertain → write: "Not provable from given code."
- Every issue MUST include a line number or code snippet.
- Only report issues that can be directly proven from the code.
- Maximum 5 findings per category.
- If none → write "None found."

──────────────────────────────────────
OUTPUT FORMAT (STRICT — follow exactly):

BUGS (Highest Priority)
- Line: <line number or snippet>
- Code: <exact code>
- Problem: <what is wrong>
- Why it is a bug: <concrete reason>
- Suggested Fix: <minimal fix>

SECURITY
- Line: <line number or snippet>
- Code: <exact code>
- Risk: <vulnerability type>
- Exploit Scenario: <realistic 1-sentence scenario>
- Fix: <minimal change>

PERFORMANCE
- Line: <line number or snippet>
- Code: <exact code>
- Issue: <what is slow/wasteful>
- Cost: <Big-O or memory impact>
- Fix: <minimal change>

READABILITY / MAINTAINABILITY
- Line: <line number or snippet>
- Code: <exact code>
- Problem: <what is unclear>
- Improvement: <concrete suggestion>

POSITIVE OBSERVATIONS
- Line: <line number or snippet>
- What is done well: <specific observation>
- Why it is good practice: <reason>

──────────────────────────────────────
BUG DETECTION CHECKLIST
Look specifically for:
✓ off-by-one errors
✓ null/None risks
✓ incorrect conditionals
✓ mutation during iteration
✓ wrong variable usage
✓ unhandled exceptions
✓ incorrect return values
✓ state logic flaws
✓ shadowed variables
✓ wrong operator usage (= vs ==, & vs and)
✓ unreachable code
✓ missing return in all branches

FIX RULES:
- Modify the exact line when possible
- Be minimal — preserve original intent
- Do not introduce new dependencies
- If fix requires >1 line → show replacement snippet"""),

    ("human", """FILE: {filename}

──── CODE START ────
{content}
──── CODE END ────

Review ONLY the code between CODE START and CODE END.
Begin your review now:""")
])

def reviewer_agent(state: dict) -> dict:
    """Reviews each file using RAG-retrieved chunks."""
    print("\n[REVIEWER] Analysing code...")

    pr_info     = state["pr_info"]
    files       = state["files"]
    vectorstore = state.get("vectorstore")
    reviews     = {}
    chain       = REVIEW_PROMPT | llm

    for f in files:
        print(f"Reviewing: {f['filename']}")

        #RAG if available
        if vectorstore:
            from rag.code_store import query_code
            query   = f"functions classes logic in {f['filename']}"
            content = query_code(vectorstore, query, k=4)
        else:
            content = (f["content"] or f["patch"])[:3000]

        result = chain.invoke({
            "repo_title": pr_info["title"],
            "filename":   f["filename"],
            "content":    content
        })
        reviews[f["filename"]] = result.content

    print(f"[REVIEWER] Reviewed {len(reviews)} files")
    return {**state, "reviews": reviews}
