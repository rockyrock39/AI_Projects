import os

# Base URL and API key come from environment (per XXX GenAI Lab handbook)
BASE_URL = os.getenv("GENAILAB_BASE_URL", "https://genailab.XXX.in")
API_KEY = os.getenv("GENAILAB_API_KEY", "sk-nKr66dLub27Nc7EjMmsUeQ")

# Default models – override with env vars if needed
CATEGORIZER_MODEL = os.getenv("CATEGORIZER_MODEL", "azure/genailab-maas-gpt-4o")
EMBEDDING_MODEL  = os.getenv("EMBEDDING_MODEL", "azure/genailab-maas-text-embedding-3-large")
GENERATOR_MODEL  = os.getenv("GENERATOR_MODEL", "azure/genailab-maas-gpt-4o")  # fallback to Llama-3.2-3b-it if needed

# Known categories – customize for your dataset
CATEGORIES = [
    "Billing",
    "Account Access",
    "Login Issue",
    "Technical",
    "Feedback",
]
