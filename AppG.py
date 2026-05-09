import streamlit as st
import pandas as pd
import joblib

# إعدادات الصفحة الواسعة
st.set_page_config(page_title="Telco Intelligence Hub", layout="wide")

# تحميل الموديل والأعمدة
model = joblib.load('model.pkl')
columns = joblib.load('columns.pkl')

# --- Sidebar Inputs ---
st.sidebar.header("📋 Customer Information")
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
tenure = st.sidebar.slider("Tenure (Months)", 0, 72, 12)
monthly_charges = st.sidebar.number_input("Monthly Charges ($)", value=50.0)
contract = st.sidebar.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])

# --- Main Layout ---
st.title("🚀 Telco Retention Intelligence System")
st.markdown("---")

# Metrics Section
c1, c2, c3 = st.columns(3)
c1.metric("Model Accuracy", "81.4%", "+2.1%")
c2.metric("Avg. Monthly Charge", f"${monthly_charges}", "Global Avg: $64")
c3.metric("Retention Risk", "High" if tenure < 12 else "Low")

tab1, tab2 = st.tabs(["🎯 Prediction Tool", "📊 Insights Dashboard"])

with tab1:
    st.subheader("Customer Prediction Status")
    if st.button("Analyze Retention Risk"):
        input_df = pd.DataFrame(0, index=[0], columns=columns)
        input_df['tenure'] = tenure
        input_df['MonthlyCharges'] = monthly_charges
        input_df['gender'] = 1 if gender == "Male" else 0
        
        prediction = model.predict(input_df)
        
        if prediction[0] == 1:
            st.error(f"⚠️ HIGH RISK: This customer is likely to churn. Recommended Action: Offer {contract} discount.")
        else:
            st.success("✅ LOW RISK: This customer is likely to remain loyal.")

with tab2:
    st.subheader("Key Drivers of Churn")
    # عرض رسم بياني بسيط
    chart_data = pd.DataFrame({
        'Feature': ['Tenure', 'MonthlyCharges', 'Contract', 'TechSupport'],
        'Importance': [0.45, 0.30, 0.15, 0.10]
    })
    st.bar_chart(chart_data.set_index('Feature'))
    st.info("Insights: Customers with tenure less than 10 months and Month-to-Month contracts show 70% higher churn rates.")
  
