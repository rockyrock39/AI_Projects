from typing import List, Tuple
import os
import pandas as pd
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import httpx
from config import BASE_URL, API_KEY, EMBEDDING_MODEL

INDEX_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_index")

def load_templates(csv_path: str) -> pd.DataFrame:
    return pd.read_csv(csv_path)

def build_or_load_index(df: pd.DataFrame) -> Chroma:
    client = httpx.Client(verify=False)
    embeddings = OpenAIEmbeddings(
        base_url=BASE_URL,
        model=EMBEDDING_MODEL,
        api_key=API_KEY,
        http_client=client
    )
    os.makedirs(INDEX_DIR, exist_ok=True)
    # Use template_text as documents; metadata includes category and index row id
    texts = df["template_text"].astype(str).tolist()
    metadatas = [{"category": c, "row": i} for i, c in enumerate(df["category"].astype(str).tolist())]
    # Create new persistent DB every run (simple hackathon flow)
    vectordb = Chroma.from_texts(texts, embeddings, metadatas=metadatas, persist_directory=INDEX_DIR)
    vectordb.persist()
    return vectordb

def retrieve_templates(vectordb: Chroma, query: str, top_k: int = 3) -> List[Tuple[str, float, dict]]:
    docs = vectordb.similarity_search_with_score(query, k=top_k)
    return [(d.page_content, float(score), d.metadata) for d, score in docs]
