import streamlit as st
import pandas as pd
import requests

BACKEND_URL = "http://backend:7860"

st.set_page_config(page_title="SuperKart Forecaster", page_icon="🛒", layout="centered")
st.title("🛒 SuperKart Sales Forecasting System")
st.markdown("Enter the product and store details below to predict expected sales revenue.")

col1, col2 = st.columns(2)
with col1:
    Product_Id_char = st.selectbox("Product ID Category", ["FD", "DR", "NC"])
    Product_Type_Category = st.selectbox("Perishability", ["Perishables", "Non Perishables"])
    Product_Sugar_Content = st.selectbox("Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
    Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
    Product_Allocated_Area = st.number_input("Allocated Area Ratio", min_value=0.0, max_value=1.0, value=0.027)

with col2:
    Product_MRP = st.number_input("Product MRP (₹)", min_value=0.0, value=117.08)
    Store_Type = st.selectbox("Store Format", ["Supermarket Type1", "Supermarket Type2", "Supermarket Type3", "Departmental Store", "Food Mart"])
    Store_Size = st.selectbox("Store Size", ["Small", "Medium", "High"])
    Store_Location_City_Type = st.selectbox("City Tier", ["Tier 1", "Tier 2", "Tier 3"])
    Store_Age_Years = st.number_input("Store Age (Years)", min_value=0, value=16)

if st.button("Run Single Prediction", type='primary'):
    product_data = {
        "Product_Weight": Product_Weight,
        "Product_Sugar_Content": Product_Sugar_Content,
        "Product_Allocated_Area": Product_Allocated_Area,
        "Product_MRP": Product_MRP,
        "Store_Size": Store_Size,
        "Store_Location_City_Type": Store_Location_City_Type,
        "Store_Type": Store_Type,
        "Product_Id_char": Product_Id_char,
        "Store_Age_Years": Store_Age_Years,
        "Product_Type_Category": Product_Type_Category
    }
    with st.spinner("Calculating..."):
        response = requests.post(f"{BACKEND_URL}/v1/predict", json=product_data)
        if response.status_code == 200:
            st.success(f"💰 **Predicted Sales Revenue: ₹{response.json()['Sales']:,.2f}**")
        else:
            st.error("Connection to Prediction API failed.")

st.divider()
st.subheader("📂 Batch Prediction")
uploaded_file = st.file_uploader("Upload a historical CSV file for bulk processing", type=["csv"])
if uploaded_file is not None:
    if st.button("Run Batch Prediction", type='primary'):
        with st.spinner("Processing batch dataset..."):
            response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file})
            if response.status_code == 200:
                st.success("Batch predictions computed successfully!")
                res_df = pd.DataFrame(list(response.json().items()), columns=["Row_Index", "Predicted_Sales"])
                st.dataframe(res_df, use_container_width=True)
            else:
                st.error("Batch processing failed.")
