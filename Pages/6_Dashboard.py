import streamlit as st
import requests
from Services.visualizeservice import plottopproducts, plotmonthlytrend, plotratingdist


st.title("Business Dashboard")
 
st.header("Sales Analytics")

if st.button("Load Charts"):
    with st.spinner("Loading visualizations..."):
        try: 

            st.subheader("1. Top Performing Product Categories")
            fig1 = plottopproducts()
            st.pyplot(fig1)

            st.subheader("2. Monthly Sales Trend")
            fig2 = plotmonthlytrend()
            st.pyplot(fig2)

            st.subheader("3. Distribution of Review Ratings")
            fig3 = plotratingdist()
            st.pyplot(fig3)

        except Exception as e:
            st.error(f"Error: {e}")

st.divider()
# Section 2: Sales Prediction Form
st.header("Revenue Forecast")
st.write("Enter last month's figures to predict next month's revenue:")

col1, col2 = st.columns(2)

with col1:
    monthrev = st.number_input("Last Month Revenue (£)", min_value=0.0, value=650000.0)
    monthordercount = st.number_input("Order Count", min_value=0, value=1300)

with col2:
    monthavgrevenue = st.number_input("Avg Order Value (£)", min_value=0.0, value=23.5)
    monthnumber = st.slider("Month (1=Jan, 12=Dec)", min_value=1, max_value=12, value=9)

if st.button("Predict Next Month Revenue"):
    with st.spinner("Calling prediction API..."):
        try:
            payload = {
                    "MonthlyRevenue": monthrev,
                    "Invoicecount": monthordercount,
                    "monAvgRev": monthavgrevenue ,
                    "monthnumber": monthnumber
}
            response = requests.post("http://localhost:8000/predict-sales", json=payload)
            result = response.json()
            st.success(f"Predicted Revenue: £{result['predictedrevenue']:,.2f}")   
        except Exception as e:
            st.error(f"Error: {e}")