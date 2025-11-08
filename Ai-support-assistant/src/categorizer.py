from typing import Tuple
from langchain_openai import ChatOpenAI
import httpx
from config import BASE_URL, API_KEY, CATEGORIZER_MODEL, CATEGORIES

SYSTEM = (
        "You are an expert support triage assistant.\n"
    "Given a support ticket, classify it and assign SLA in days.\n\n"
    "Return ONLY valid JSON.\n\n"
    "category: one of [Billing, Account Access, Login Issue, Technical, Feedback]\n"
    "confidence: float between 0 and 1\n"
    "SLA: integer number of days based on rules below:\n\n"
    "SLA Rules:\n"
    "- Billing → 4 ays\n"
    "- Account Access → 1 day\n"
    "- Login Issue → 1 day\n"
    "- Technical → 3 days\n"
    "- Feedback → 7 days\n"

)

def categorize_ticket(text: str) -> Tuple[str, float]:
    client = httpx.Client(verify=False)
    llm = ChatOpenAI(
        base_url=BASE_URL,
        model=CATEGORIZER_MODEL,
        api_key=API_KEY,
        http_client=client,
        temperature=0.7,
    )
    allowed = ", ".join(CATEGORIES)
    prompt = (
        f"Allowed categories: [{allowed}].\n"
        f"Ticket: '''{text.strip()}'''\n"
        f"Return JSON only."
    )
    res = llm.invoke([
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": prompt}
    ])
    content = res.content if hasattr(res, 'content') else str(res)
    import json, re
    try:
        # Extract JSON
        start = content.find('{')
        end = content.rfind('}') + 1
        payload = json.loads(content[start:end])
        cat = payload.get("category", "Technical")
        conf = float(payload.get("confidence", 0.7))
        sla = float(payload.get("SLA", 1))
        if cat not in CATEGORIES:
            cat = "Technical"
        return cat, conf ,sla
    except Exception:
        return "Technical", 0.6
