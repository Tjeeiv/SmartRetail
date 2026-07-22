import streamlit as st
from Services.ingestservice import ingestall

st.title("Ingest Data into DB")

if st.button("Import"):
    with st.spinner("Ingest Inprogress"):
        try:
            ingestall()
            st.success("Raw Data ingested successfully")
        except Exception as e:
            st.error(f"Error: {e}")