
# rag/code_store.py
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from config import LM_STUDIO_URL
import os, shutil

CHROMA_DIR = "chroma_code_review"
LM_STUDIO_URL = "http://127.0.0.1:1234/v1"   
def build_code_index(files: list[dict], owner: str, repo: str) -> Chroma:
    print("\n[RAG] Building code index...")

    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\ndef ", "\nclass ", "\n\n", "\n", " "]
    )

    docs = []
    for f in files:
        content = f["content"]
        if not isinstance(content, str) or not content.strip():
            continue
        #Force plain text only (strips any notebook JSON noise)
        content = content.encode("utf-8", errors="ignore").decode("utf-8")
        chunks = splitter.split_text(content)
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                docs.append(Document(
                    page_content=str(chunk),
                    metadata={
                        "filename": str(f["filename"]),
                        "chunk":    i,
                        "repo":     f"{owner}/{repo}"
                    }
                ))

    print(f"Indexed {len(docs)} chunks from {len(files)} files")

    embeddings = OpenAIEmbeddings(
        base_url=LM_STUDIO_URL,
        api_key="lm-studio",
        model="text-embedding-nomic-embed-text-v1.5",
        check_embedding_ctx_length=False #disables token checking
    )

    #Embed in small batches to avoid overflow
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
        collection_metadata={"hnsw:space": "cosine"}
    )

    print("[RAG] Code index ready!")
    return vectorstore

def query_code(vectorstore, query: str, k: int = 4) -> str:
    docs = vectorstore.similarity_search(query, k=k)
    return "\n\n".join([
        f"# {d.metadata['filename']} (chunk {d.metadata['chunk']})\n{d.page_content}"
        for d in docs
    ])
