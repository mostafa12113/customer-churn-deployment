import streamlit as st
import pandas as pd
import joblib

# إعدادات الصفحة
st.set_page_config(page_title="Advanced Churn Predictor", layout="wide")

# تحميل الموديل والأعمدة
try:
    model = joblib.load('model.pkl')
    columns = joblib.load('columns.pkl')
except:
    st.error("Make sure model.pkl and columns.pkl are in the same folder!")

st.title("📊 Telco Customer Churn Intelligence")
st.markdown("Enter all customer details for a high-precision prediction.")
st.write("---")

# تقسيم المدخلات لثلاثة أعمدة عشان الشكل يبقى منظم وكبير
col1, col2, col3 = st.columns(3)

with col1:
    st.header("👤 Demographics")
    gender = st.selectbox("Gender", ["Male", "Female"])
    senior = st.selectbox("Senior Citizen", ["Yes", "No"])
    partner = st.selectbox("Has Partner?", ["Yes", "No"])
    dependents = st.selectbox("Has Dependents?", ["Yes", "No"])

with col2:
    st.header("📞 Services")
    tenure = st.slider("Tenure (Months)", 0, 72, 12)
    phone = st.selectbox("Phone Service", ["Yes", "No"])
    paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])

with col3:
    st.header("💰 Financials")
    monthly_charges = st.number_input("Monthly Charges ($)", value=50.0)
    total_charges = st.number_input("Total Charges ($)", value=600.0)
    payment_method = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer", "Credit card"])

st.write("---")

if st.button("Generate Prediction Report"):
    # تجهيز الداتا بكل الـ Features
    input_df = pd.DataFrame(0, index=[0], columns=columns)
    
    # ربط المدخلات بالأعمدة (Encoding بسيط)
    input_df['tenure'] = tenure
    input_df['MonthlyCharges'] = monthly_charges
    input_df['TotalCharges'] = total_charges
    input_df['gender'] = 1 if gender == "Male" else 0
    input_df['SeniorCitizen'] = 1 if senior == "Yes" else 0
    input_df['Partner'] = 1 if partner == "Yes" else 0
    input_df['Dependents'] = 1 if dependents == "Yes" else 0
    input_df['PhoneService'] = 1 if phone == "Yes" else 0
    input_df['PaperlessBilling'] = 1 if paperless == "Yes" else 0
    
    # التوقع
    prediction = model.predict(input_df)
    probability = model.predict_proba(input_df)[0][1] # نسبة احتمال الـ Churn
    
    st.subheader("Results:")
    if prediction[0] == 1:
        st.error(f"🚨 Prediction: Customer will CHURN (Probability: {probability:.2%})")
        st.info("Strategy: Consider offering a contract upgrade or discount.")
    else:
        st.success(f"✅ Prediction: Customer will STAY (Probability of leaving: {probability:.2%})")


    
