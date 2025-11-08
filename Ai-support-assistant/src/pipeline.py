from typing import Dict, Any
from categorizer import categorize_ticket
from embeddings import load_templates, build_or_load_index, retrieve_templates
from generator import generate_response

def run_pipeline(ticket_text: str, templates_csv_path: str) -> Dict[str, Any]:
    # 1) Categorize
    category, confidence , sla = categorize_ticket(ticket_text)

    # 2) Build / Load Embedding Index
    df = load_templates(templates_csv_path)
    vectordb = build_or_load_index(df)

    # 3) Retrieve Top Templates (query is the ticket text + category for relevance)
    retrieved = retrieve_templates(vectordb, f"{ticket_text}\nCategory:{category}", top_k=3)
    retrieved_texts = [t for (t, score, meta) in retrieved]

    # 4) Generate Response
    response = generate_response(ticket_text, category, retrieved_texts)

    # 5) Return standard payload
    return {
        "category": category,
        "category_confidence": round(confidence, 3),
        "SLA" : sla,
        "retrieved_templates": retrieved_texts,
        "suggested_response": response.strip(),
    }
