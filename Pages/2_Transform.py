import streamlit as st
from Services.transformservice import transformall

st.title("Transform Data")

if st.button("Transform"):
    with st.spinner("Cleaning Inprogress"):
        try:
            transformall ()
            st.success("Gold Data created successfully")
        except Exception as e:
            st.error(f"Error: {e}")