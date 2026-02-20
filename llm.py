# llm.py
from langchain_openai import ChatOpenAI
from config import LM_STUDIO_URL, LM_MODEL

def get_llm(temperature: float = 0.1) -> ChatOpenAI:
    return ChatOpenAI(
        base_url=LM_STUDIO_URL,
        api_key="lm-studio",
        model=LM_MODEL,
        temperature=temperature,
        max_tokens=2048,
        timeout=300
    )
