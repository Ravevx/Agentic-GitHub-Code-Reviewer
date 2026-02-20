# agents/summariser.py
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
from llm import get_llm

llm = get_llm(temperature=0.1)

SUMMARY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a tech lead writing a final code review summary.
    Be concise. Write in bullet points.

    Structure your response as:
    VERDICT: Approve / Request Changes / Needs Major Work
    SCORE: X/10
    SECURITY RISK: Low / Medium / High
    
    TOP 3 CRITICAL ISSUES:
    - issue 1
    - issue 2  
    - issue 3
    
    TOP 3 IMPROVEMENTS:
    - improvement 1
    - improvement 2
    - improvement 3
    
    ESTIMATED FIX TIME: X hours"""),
    ("human", """Repo: {repo_title}
Files reviewed: {changed_files}

REVIEW HIGHLIGHTS:
{all_reviews}

Write the final summary:""")
])

def truncate_reviews(reviews: dict, max_chars: int = 1500) -> str:
    """
    Hard cap total review text to fit in 4096 token context.
    Takes equal slice from each file review.
    """
    if not reviews:
        return "No reviews."
    per_file  = max_chars // max(len(reviews), 1)
    condensed = []
    for fname, review in reviews.items():
        # Take only first N chars and cut at last newline
        snippet = review[:per_file]
        last_nl = snippet.rfind("\n")
        if last_nl > per_file // 2:
            snippet = snippet[:last_nl]
        condensed.append(f"FILE: {fname}\n{snippet.strip()}")
    return "\n\n".join(condensed)

def summariser_agent(state: dict) -> dict:
    print("\n[SUMMARISER] Writing final report...")

    pr_info     = state["pr_info"]
    reviews     = state["reviews"]
    suggestions = state.get("suggestions", {})

    #Hard truncate to stay under 4096 tokens
    condensed = truncate_reviews(reviews, max_chars=1500)

    chain   = SUMMARY_PROMPT | llm
    summary = chain.invoke({
        "repo_title":    pr_info["title"],
        "changed_files": pr_info["changed_files"],
        "all_reviews":   condensed
    })

    # ── Build full report ──
    timestamp    = datetime.now().strftime("%Y-%m-%d %H:%M")
    final_report = f"""#AI Code Review Report
**Generated:** {timestamp}  
**Repo:** {pr_info['title']}  
**Author:** @{pr_info['author']}  
**Files Reviewed:** {pr_info['changed_files']}  

---

## Executive Summary
{summary.content}

---

## File-by-File Reviews
"""
    for fname, review in reviews.items():
        final_report += f"\n### `{fname}`\n{review}\n"
        if fname in suggestions:
            final_report += f"\n**💡 Fix Suggestions:**\n{suggestions[fname]}\n"
        final_report += "\n---\n"

    print("[SUMMARISER] Report complete!")
    return {**state, "final_report": final_report}
