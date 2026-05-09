import streamlit as st
import pandas as pd
import joblib

# تحميل الموديل والأعمدة
model = joblib.load('model.pkl')
columns = joblib.load('columns.pkl')

st.title("📊 Customer Churn Prediction")
st.markdown("Enter customer details to predict if they will stay or leave.")

# خانات الإدخال
tenure = st.slider("Tenure (Months)", 0, 72, 12)
monthly_charges = st.number_input("Monthly Charges ($)", value=50.0)
gender = st.selectbox("Gender", ["Male", "Female"])

if st.button("Predict"):
    # تجهيز الداتا
    input_df = pd.DataFrame(0, index=[0], columns=columns)
    input_df['tenure'] = tenure
    input_df['MonthlyCharges'] = monthly_charges
    input_df['gender'] = 1 if gender == "Male" else 0
    
    # التوقع
    prediction = model.predict(input_df)
    
    if prediction[0] == 1:
        st.error("Prediction: Customer will Leave (Churn)")
    else:
        st.success("Prediction: Customer will Stay")
