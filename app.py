import streamlit as st

st.set_page_config(page_title="SmartRetail 360", layout="wide")

st.title("SmartRetail 360 — Analytics & AI Platform")
st.write("An end-to-end data and AI intelligence platform for e-commerce businesses.")

st.divider()

st.subheader("Pipeline Steps")
st.markdown("""
1. **Ingest** — Load sales and review data into database
2. **Transform** — Clean and aggregate data (Bronze → Gold)
3. **Visualize** — Explore sales trends and review ratings
4. **ML** — Train revenue forecasting model
5. **Knowledge Base** — Build semantic search from reviews
6. **Dashboard** — Business analytics + revenue prediction
7. **AI Assistant** — Chat with your review data
""")