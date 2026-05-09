import streamlit as st
import pandas as pd
import joblib

# 1. Page Configuration
st.set_page_config(page_title="Telco Churn Predictor", layout="wide")

# 2. Load Assets
# Load the model and columns files
model = joblib.load('model.pkl')
columns = joblib.load('columns.pkl')

st.title("📊 Customer Retention Prediction System")
st.markdown("Enter customer data to get an accurate analysis of their status (Stay or Churn).")
st.write("---")

# --- Data Input Interface (3 Columns) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.header("👤 Customer Demographics")
    gender = st.selectbox("Gender", ["Female", "Male"])
    senior = st.selectbox("Senior Citizen", [0, 1])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])
    tenure = st.slider("Tenure (Months)", 0, 72, 12)

with col2:
    st.header("🌐 Subscribed Services")
    internet = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
    security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
    backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
    support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])

with col3:
    st.header("💰 Financial Details")
    monthly_charges = st.number_input("Monthly Charges ($)", value=60.0)
    total_charges = st.number_input("Total Charges ($)", value=1000.0)
    payment = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
    paperless = st.selectbox("Paperless Billing", ["Yes", "No"])

st.write("---")

# --- Prediction Button and Results ---
if st.button("🔍 Run Customer Analysis"):
    # Prepare data for the model
    input_df = pd.DataFrame(0, index=[0], columns=columns)
    
    # Mapping inputs to the dataframe (names must match columns.pkl)
    input_df['tenure'] = tenure
    input_df['MonthlyCharges'] = monthly_charges
    input_df['TotalCharges'] = total_charges
    input_df['gender'] = 1 if gender == "Male" else 0
    input_df['SeniorCitizen'] = senior
    input_df['Partner'] = 1 if partner == "Yes" else 0
    input_df['Dependents'] = 1 if dependents == "Yes" else 0
    input_df['PaperlessBilling'] = 1 if paperless == "Yes" else 0
    
    # Execute Prediction
    prediction = model.predict(input_df)
    probability = model.predict_proba(input_df)[0][1]

    # --- Display Final Result ---
    st.write("## Final Result:")
    
    if prediction[0] == 1:
        # Churn Status
        st.error("## 🛑 Prediction: Customer Will CHURN")
        st.metric(label="Churn Probability", value=f"{probability:.1%}")
        st.progress(probability)
    else:
        # Stay Status
        st.success("## ✅ Prediction: Customer Will STAY")
        st.metric(label="Stay Probability", value=f"{(1-probability):.1%}")
        st.progress(1 - probability)
        
    st.write("---")
    st.info("Note: This prediction is based on the machine learning model's analysis of the company's historical Excel dataset.")

  
  
    
