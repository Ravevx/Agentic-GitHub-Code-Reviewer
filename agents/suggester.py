# agents/suggester.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config import LM_STUDIO_URL, LM_MODEL

from langchain_openai import ChatOpenAI
from config import LM_STUDIO_URL, LM_MODEL

from llm import get_llm
llm = get_llm(temperature=0.2)

SUGGEST_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a senior engineer providing concrete fix suggestions.
    
    For each issue found in the code review, provide:
    1. The ORIGINAL problematic code snippet
    2. The FIXED code snippet  
    3. A one-line explanation of why the fix is better
    
    Format as:
    ### Fix for: [issue title]
    **Original:**
    ```
    [original code]
    ```
    **Fixed:**
    ```
    [fixed code]
    ```
    **Why:** [explanation]"""),
    ("human", """File: {filename}

CODE REVIEW FINDINGS:
{review}

ORIGINAL FILE CONTENT:
{content}

Provide specific fix suggestions with before/after code:""")
])

def suggester_agent(state: dict) -> dict:
    """Generates concrete fix suggestions for each reviewed file."""
    print("\n[SUGGESTER] Generating fix suggestions...")

    files      = state["files"]
    reviews    = state["reviews"]
    suggestions = {}
    chain      = SUGGEST_PROMPT | llm

    for f in files:
        filename = f["filename"]
        if filename not in reviews:
            continue
        print(f"Suggesting fixes: {filename}")
        result = chain.invoke({
            "filename": filename,
            "review":   reviews[filename],
            "content":  f["content"] or f["patch"]
        })
        suggestions[filename] = result.content

    print(f"[SUGGESTER] Generated suggestions for {len(suggestions)} files")
    return {**state, "suggestions": suggestions}
