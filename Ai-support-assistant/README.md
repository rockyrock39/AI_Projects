# TCS AI Fridays – Customer Support AI Assistant

End-to-end project for **Automated Ticket Categorization and Response Suggestion**.
Designed to run **inside the TCS GenAI Lab** using the provided base URL and models from the Participant Handbook.

## ✨ Features
- Categorizes incoming tickets with an in-lab reasoning model.
- Retrieves top response templates via **semantic search (Chroma + embeddings)**.
- Generates a polished response with an in-lab instruct model.
- Simple **Streamlit UI** + JSON/CSV export.
- Fully local/vendored to meet **no external MaaS** constraints beyond provided lab endpoint.

## 🧱 Architecture
```
Ticket → Categorizer (DeepSeek-V3-0324) → Embedding Retrieval (text-embedding-3-large + Chroma)
      → Generator (Llama-3.3-70B-Instruct or Llama-3.2-3B-it) → JSON/CSV Output
```
All models accessed at `https://genailab.tcs.in` via `langchain_openai` per handbook.

## 🚀 Quickstart
1) **Install deps** (use the lab laptop):
```bash
pip install -r requirements.txt
```

2) **Set environment variables** (key will be provided by organizers):
```bash
export GENAILAB_BASE_URL="https://genailab.tcs.in"
export GENAILAB_API_KEY="PASTE_YOUR_KEY"
# Optional model overrides:
# export CATEGORIZER_MODEL="azure_ai/genailab-maas-DeepSeek-V3-0324"
# export EMBEDDING_MODEL="azure/genailab-maas-text-embedding-3-large"
# export GENERATOR_MODEL="azure_ai/genailab-maas-Llama-3.3-70B-Instruct"
```

3) **Run Streamlit app**
```bash
streamlit run src/app.py
```

4) **Use the UI**
- Paste a ticket text, hit **Run Pipeline**.
- See predicted category, suggested response, and export options.
- The vector index persists in `./chroma_index`.

## 📂 Project Structure
```
tcs-ai-fridays-support-assistant/
├── data/
│   └── templates.csv
├── src/
│   ├── app.py
│   ├── pipeline.py
│   ├── categorizer.py
│   ├── embeddings.py
│   ├── generator.py
│   └── config.py
├── requirements.txt
└── README.md
```

## 🧪 Sample Categories
- Billing
- Account Access
- Login Issue
- Technical
- Feedback

Edit `data/templates.csv` to add your org-specific templates.

## 🛡️ Notes (per Participant Handbook)
- Uses in-lab base URL and approved models.
- No cloning full solutions; this is original minimal code.
- Avoids external APIs beyond the provided lab endpoint.

## 📜 License
TCS Internal – For hackathon use.
