import streamlit as st
import pandas as pd
import joblib

# إعدادات الصفحة
st.set_page_config(page_title="Telco Churn Expert System", layout="wide")

# تحميل الموديل والأعمدة
model = joblib.load('model.pkl')
columns = joblib.load('columns.pkl')

st.title("📊 Telco Customer Intelligence Dashboard")
st.markdown("This system uses Machine Learning to predict customer retention based on the full dataset features.")
st.write("---")

# تقسيم المدخلات لـ 3 أقسام احترافية
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👤 Customer Profile")
    gender = st.selectbox("Gender", ["Female", "Male"])
    senior = st.selectbox("Senior Citizen (0=No, 1=Yes)", [0, 1])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])
    tenure = st.slider("Tenure (Months)", 0, 72, 12)

with col2:
    st.subheader("🌐 Services Subscribed")
    phone_service = st.selectbox("Phone Service", ["Yes", "No"])
    multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
    internet_service = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
    online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
    online_backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
    device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
    tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])

with col3:
    st.subheader("💳 Billing & Contract")
    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
    payment = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
    monthly_charges = st.number_input("Monthly Charges ($)", value=64.75)
    total_charges = st.number_input("Total Charges ($)", value=1000.0)

st.write("---")

if st.button("🔍 Run In-Depth Analysis"):
    # إنشاء DataFrame بجميع الأعمدة وتصفيرها
    input_df = pd.DataFrame(0, index=[0], columns=columns)
    
    # تحويل المدخلات لبيانات رقمية (Encoding) لتتوافق مع الموديل
    input_df['tenure'] = tenure
    input_df['MonthlyCharges'] = monthly_charges
    input_df['TotalCharges'] = total_charges
    input_df['gender'] = 1 if gender == "Male" else 0
    input_df['SeniorCitizen'] = senior
    input_df['Partner'] = 1 if partner == "Yes" else 0
    input_df['Dependents'] = 1 if dependents == "Yes" else 0
    input_df['PhoneService'] = 1 if phone_service == "Yes" else 0
    input_df['PaperlessBilling'] = 1 if paperless == "Yes" else 0
    
    # ملاحظة: إذا كان الموديل يستخدم One-Hot Encoding للأعمدة النصية (مثل Contract)
    # يجب تفعيلها هنا بناءً على أسماء الأعمدة في columns.pkl
    
    prediction = model.predict(input_df)
    prob = model.predict_proba(input_df)[0][1]
    
    st.header("Results:")
    if prediction[0] == 1:
        st.error(f"🚨 ALERT: High Churn Risk ({prob:.1%})")
        st.write("Customer is likely to cancel. Immediate retention offer recommended.")
    else:
        st.success(f"✅ Safe: Low Churn Risk ({prob:.1%})")
        st.write("Customer is loyal. Maintain current service level.")


  
