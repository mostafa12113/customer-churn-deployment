import streamlit as st
import pandas as pd
import joblib

# 1. إعداد الصفحة (لازم يكون أول سطر بعد الـ import)
st.set_page_config(page_title="Customer Churn Prediction", layout="centered")

# 2. تحميل الموديل والأعمدة
@st.cache_resource
def load_model():
    model = joblib.load('model.pkl')
    columns = joblib.load('columns.pkl')
    return model, columns

try:
    model, columns = load_model()
except:
    st.error("Model files not found!")

# 3. واجهة المستخدم
st.title("📊 Customer Churn Intelligence")
st.write("ادخل بيانات العميل للتوقع (Stay or Churn)")
st.write("---")

# تقسيم المدخلات لصفوف منظمة
col1, col2 = st.columns(2)

with col1:
    tenure = st.slider("مدة الاشتراك (Tenure)", 0, 72, 12)
    monthly_charges = st.number_input("المصاريف الشهرية ($)", value=50.0)
    gender = st.selectbox("النوع", ["Female", "Male"])

with col2:
    contract = st.selectbox("نوع العقد", ["Month-to-month", "One year", "Two year"])
    internet = st.selectbox("الإنترنت", ["DSL", "Fiber optic", "No"])
    payment = st.selectbox("طريقة الدفع", ["Electronic check", "Mailed check", "Bank transfer", "Credit card"])

st.write("---")

# 4. زر التوقع
if st.button("Predict / توقع الحالة"):
    # إنشاء DataFrame وتصفيره
    input_df = pd.DataFrame(0, index=[0], columns=columns)
    
    # ملء البيانات الأساسية
    input_df['tenure'] = tenure
    input_df['MonthlyCharges'] = monthly_charges
    input_df['gender'] = 1 if gender == "Male" else 0
    
    # تحويل العقد لرقم (Encoding بسيط)
    if contract == "Month-to-month":
        if 'Contract_Month-to-month' in columns: input_df['Contract_Month-to-month'] = 1
    elif contract == "One year":
        if 'Contract_One year' in columns: input_df['Contract_One year'] = 1

    # تنفيذ التوقع
    prediction = model.predict(input_df)
    
    st.write("### النتيجة:")
    if prediction[0] == 1:
        st.error("⚠️ النتيجة: العميل سيغادر (Customer will Churn)")
    else:
        st.success("✅ النتيجة: العميل سيبقى (Customer will Stay)")
