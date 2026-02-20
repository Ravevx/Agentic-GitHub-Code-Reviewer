# graph/review_graph.py
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, Any
from agents.fetcher    import fetcher_agent
from agents.reviewer   import reviewer_agent
from agents.suggester  import suggester_agent
from agents.summariser import summariser_agent

class ReviewState(TypedDict):
    pr_url:       str
    pr_info:      Optional[dict]
    files:        Optional[list]
    reviews:      Optional[dict]
    suggestions:  Optional[dict]
    final_report: Optional[str]
    owner:        Optional[str]
    repo:         Optional[str]
    pr_number:    Optional[int]
    repo_info:    Optional[dict]
    vectorstore:  Optional[Any]

def build_review_graph():
    graph = StateGraph(ReviewState)
    graph.add_node("fetcher",    fetcher_agent)
    graph.add_node("reviewer",   reviewer_agent)
    graph.add_node("suggester",  suggester_agent)
    graph.add_node("summariser", summariser_agent)
    graph.set_entry_point("fetcher")
    graph.add_edge("fetcher",    "reviewer")
    graph.add_edge("reviewer",   "suggester")
    graph.add_edge("suggester",  "summariser")
    graph.add_edge("summariser", END)
    return graph.compile()

review_graph = build_review_graph()

def run_review(repo_url: str) -> str:
    print(f"AI CODE REVIEW AGENT")
    print(f"   Repo: {repo_url}\n")
    result = review_graph.invoke({"pr_url": repo_url})
    return result["final_report"]
