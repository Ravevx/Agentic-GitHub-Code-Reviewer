# test_lm.py
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="local-model",
    temperature=0.1
)

response = llm.invoke("Say hello in one sentence.")
print(response.content)
