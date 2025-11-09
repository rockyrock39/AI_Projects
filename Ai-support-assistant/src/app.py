import os, json, pandas as pd
import streamlit as st
from pipeline import run_pipeline

st.set_page_config(page_title="Support AI Assistant")
st.title("AI Agent: Ticket Categorization & Response Suggestion")

# Paths
ROOT = os.path.dirname(os.path.dirname(__file__))
DEFAULT_TEMPLATES = os.path.join(ROOT, "data", "templates.csv")

#with st.expander("Environment (read-only)", expanded=False):
   # st.write({
     #   "GENAILAB_BASE_URL": os.getenv("GENAILAB_BASE_URL", "https://genailab.XXX.in"),
    #    "CATEGORIZER_MODEL": os.getenv("CATEGORIZER_MODEL", "azure_ai/genailab-maas-DeepSeek-V3-0324"),
     #   "EMBEDDING_MODEL": os.getenv("EMBEDDING_MODEL", "azure/genailab-maas-text-embedding-3-large"),
     #   "GENERATOR_MODEL": os.getenv("GENERATOR_MODEL", "azure_ai/genailab-maas-Llama-3.3-70B-Instruct"),
   # })

st.markdown("""**Instructions For Raising Support Ticket**
1. Please raise your ticket in the box below.
2. Click **Submit**.
3. Review category, templates, and suggested response.
4. Export JSON/CSV if needed.
""")

ticket = st.text_area("Ticket text", height=150, placeholder="e.g., I was charged twice for my subscription but only used it once this month.")
templates_file = st.file_uploader("Upload image for issue", type=["csv"])
#templates_file = st.file_uploader("Upload templates CSV (optional)", type=["csv"])

team_mail={
    "Billing" :["Costing Team","cost@XXX.com"],
    "Account Access" :["Admin Team","admin@XXX.com"],
    "Login Issue" :["Admin Team","admin@XXX.com"],
    "Technical" :["IT Team","it@XXX.com"],
    "Feedback" :["Support Team","support@XXX.com"]

}
if st.button("Submit Ticket", type="primary"):
    if not ticket.strip():
        st.error("Please enter a ticket text.")
        st.stop()
    if templates_file:
        # Save to a temp path
        tmp_path = os.path.join(ROOT, "data", "uploaded_templates.csv")
        with open(tmp_path, "wb") as f:
         f.write(templates_file.getvalue())
        templates_path = tmp_path
    else:
        templates_path = DEFAULT_TEMPLATES

    with st.spinner("Thinking...."):
        payload = run_pipeline(ticket, templates_path)

    # st.subheader("Result (JSON)")
    # st.code(json.dumps(payload, indent=2))

    st.subheader("Suggested Response")
    #st.write(payload["suggested_response"])
    st.write("**Suggested Response:**", payload["suggested_response"])
    st.write("**Category:**", payload["category"])
    st.write("**Confidence:**", payload["category_confidence"])
    st.write("**SLA:**", str(payload["SLA"])+" Days")
    if  team_mail.get(payload["category"]):
        st.write("**Team Information:**", team_mail.get(payload["category"])[0],team_mail.get(payload["category"])[1])
    



    # Export
    export_df = pd.DataFrame([{
        "ticket": ticket,
        "category": payload["category"],
        "category_confidence": payload["category_confidence"],
        "suggested_response": payload["suggested_response"],
    }])
    st.download_button("Download Response CSV", data=export_df.to_csv(index=False), file_name="ai_ticket_response.csv")
    st.download_button("Download Response JSON", data=json.dumps(payload, indent=2), file_name="ai_ticket_response.json")

#st.caption("XXX Internal – AI Fridays Hackathon demo app.")
