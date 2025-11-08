from typing import List
from langchain_openai import ChatOpenAI
import httpx
from config import BASE_URL, API_KEY, GENERATOR_MODEL

SYSTEM = (
    "You are a professional customer support assistant. "
    "Write concise, empathetic, and actionable replies. "
    "Never disclose internal details. Keep responses under 120 words when possible."
)

def generate_response(ticket: str, category: str, retrieved_templates: List[str]) -> str:
    client = httpx.Client(verify=False)
    llm = ChatOpenAI(
        base_url=BASE_URL,
        model=GENERATOR_MODEL,
        api_key=API_KEY,
        http_client=client,
        temperature=0.3,
    )
    context = "\n\n".join([f"TEMPLATE {i+1}: {t}" for i, t in enumerate(retrieved_templates)])
    user = (
        f"Category: {category}\n"
        f"Ticket: {ticket.strip()}\n\n"
        f"Use the templates below as guidance; adapt them to the user's case:\n{context}\n\n"
        f"Return ONLY the final response text; no preface, no JSON."
    )
    res = llm.invoke([
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user}
    ])
    return res.content if hasattr(res, 'content') else str(res)
