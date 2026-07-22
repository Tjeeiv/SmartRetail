import streamlit as st 
from Services.visualizeservice import    plottopproducts ,plotmonthlytrend, plotratingdist
 

st.title("Visual Analytics")


if st.button("Generate Visualization"):
    with st.spinner("Loading Graph.."):
        try:
 
 
            st.subheader("1. Top-Performing Products")
            fig1 = plottopproducts( )
            st.pyplot(fig1)

            st.header("2. Monthly Sales Trend")
            fig2 = plotmonthlytrend()
            st.pyplot(fig2)

            st.header("3. Review Distribution")
            fig3 = plotratingdist()
            st.pyplot(fig3)

        except Exception as e:
            st.error(f"Error:{e}")
 