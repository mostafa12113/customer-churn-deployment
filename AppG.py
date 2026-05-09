import streamlit as st
import pandas as pd
import joblib

# إعدادات الصفحة
st.set_page_config(page_title="Telco Churn Predictor", layout="wide")

# تحميل الملفات الأساسية
model = joblib.load('model.pkl')
columns = joblib.load('columns.pkl')

st.title("📊 نظام توقع بقاء أو رحيل العملاء")
st.markdown("قم بإدخال بيانات العميل للحصول على تحليل دقيق لحالته (Stay or Churn).")
st.write("---")

# --- واجهة إدخال البيانات (3 أعمدة) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.header("👤 بيانات العميل")
    gender = st.selectbox("النوع (Gender)", ["Female", "Male"])
    senior = st.selectbox("كبار السن (Senior Citizen)", [0, 1])
    partner = st.selectbox("شريك (Partner)", ["Yes", "No"])
    dependents = st.selectbox("معالين (Dependents)", ["Yes", "No"])
    tenure = st.slider("مدة الاشتراك بالشهور (Tenure)", 0, 72, 12)

with col2:
    st.header("🌐 الخدمات المشترك بها")
    internet = st.selectbox("خدمة الإنترنت", ["Fiber optic", "DSL", "No"])
    security = st.selectbox("الحماية عبر الإنترنت", ["No", "Yes", "No internet service"])
    backup = st.selectbox("النسخ الاحتياطي", ["No", "Yes", "No internet service"])
    support = st.selectbox("الدعم الفني", ["No", "Yes", "No internet service"])
    contract = st.selectbox("نوع العقد (Contract)", ["Month-to-month", "One year", "Two year"])

with col3:
    st.header("💰 البيانات المالية")
    monthly_charges = st.number_input("المصاريف الشهرية ($)", value=60.0)
    total_charges = st.number_input("إجمالي المصاريف ($)", value=1000.0)
    payment = st.selectbox("طريقة الدفع", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
    paperless = st.selectbox("فواتير إلكترونية", ["Yes", "No"])

st.write("---")

# --- زر التحليل والنتيجة ---
if st.button("🔍 تحليل حالة العميل الآن"):
    # تجهيز البيانات للموديل
    input_df = pd.DataFrame(0, index=[0], columns=columns)
    
    # ربط المدخلات (يجب أن تتطابق الأسماء مع الـ columns.pkl)
    input_df['tenure'] = tenure
    input_df['MonthlyCharges'] = monthly_charges
    input_df['TotalCharges'] = total_charges
    input_df['gender'] = 1 if gender == "Male" else 0
    input_df['SeniorCitizen'] = senior
    input_df['Partner'] = 1 if partner == "Yes" else 0
    input_df['Dependents'] = 1 if dependents == "Yes" else 0
    input_df['PaperlessBilling'] = 1 if paperless == "Yes" else 0
    
    # تنفيذ التوقع
    prediction = model.predict(input_df)
    probability = model.predict_proba(input_df)[0][1]

    # --- عرض النتيجة النهائية بشكل ضخم ---
    st.write("## النتيجة النهائية:")
    
    if prediction[0] == 1:
        # حالة المغادرة (Churn)
        st.error("## 🛑 العميل سيغادر الشركة (Customer Will CHURN)")
        st.metric(label="نسبة احتمال المغادرة", value=f"{probability:.1%}")
        st.progress(probability)
    else:
        # حالة البقاء (Stay)
        st.success("## ✅ العميل سيستمر مع الشركة (Customer Will STAY)")
        st.metric(label="نسبة احتمال البقاء", value=f"{(1-probability):.1%}")
        st.progress(1 - probability)
        
    st.write("---")
    st.info("ملاحظة: هذا التوقع مبني على تحليل الموديل للبيانات التاريخية في شيت الإكسيل الخاص بالشركة.")
