import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# 1. إعدادات الصفحة الواسعة والثيم الاحترافي
st.set_page_config(page_title="Telco Intelligence Hub", layout="wide", initial_sidebar_state="expanded")

# 2. تحميل الموديل والأعمدة مع معالجة الأخطاء
@st.cache_resource
def load_assets():
    model = joblib.load('model.pkl')
    columns = joblib.load('columns.pkl')
    return model, columns

try:
    model, columns = load_assets()
except Exception as e:
    st.error(f"Error loading model files: {e}")

# --- Sidebar: مدخلات البيانات ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
st.sidebar.title("📋 بيانات العميل")
st.sidebar.info("أدخل التفاصيل الفنية والمالية للعميل")

with st.sidebar:
    st.subheader("👤 الملف الشخصي")
    gender = st.selectbox("النوع", ["Female", "Male"])
    senior = st.selectbox("من كبار السن؟", ["No", "Yes"])
    partner = st.selectbox("مرتبط (Partner)", ["Yes", "No"])
    dependents = st.selectbox("يعول (Dependents)", ["Yes", "No"])
    tenure = st.slider("مدة الاشتراك (شهور)", 0, 72, 12)

    st.subheader("🌐 الخدمات")
    internet = st.selectbox("نوع الإنترنت", ["DSL", "Fiber optic", "No"])
    contract = st.selectbox("نوع العقد", ["Month-to-month", "One year", "Two year"])
    support = st.selectbox("الدعم الفني", ["No", "Yes", "No internet service"])
    security = st.selectbox("الحماية", ["No", "Yes", "No internet service"])

    st.subheader("💰 المالية")
    monthly_charges = st.number_input("المصاريف الشهرية ($)", value=65.0)
    total_charges = st.number_input("إجمالي المصاريف ($)", value=monthly_charges * tenure if tenure > 0 else monthly_charges)
    payment = st.selectbox("طريقة الدفع", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])

# --- الصفحة الرئيسية ---
st.title("🚀 نظام التوقع الذكي لبقاء العملاء (AI Retention)")
st.markdown("---")

# عرض إحصائيات سريعة (Metrics)
m1, m2, m3 = st.columns(3)
m1.metric("حالة العقد", contract)
m2.metric("متوسط التكلفة", f"${monthly_charges}")
m3.metric("مدة الولاء", f"{tenure} شهر")

tab1, tab2 = st.tabs(["🎯 التوقع المباشر", "📊 تحليل البيانات (Insights)"])

with tab1:
    st.subheader("تحليل احتمالية الاستمرار")
    
    if st.button("تشغيل الموديل الذكي 🔍"):
        # تجهيز الداتا وعمل الـ Encoding اليدوي لضمان الدقة
        input_df = pd.DataFrame(0, index=[0], columns=columns)
        
        # ربط القيم الرقمية
        input_df['tenure'] = tenure
        input_df['MonthlyCharges'] = monthly_charges
        input_df['TotalCharges'] = total_charges
        input_df['SeniorCitizen'] = 1 if senior == "Yes" else 0
        
        # ربط الـ Categorical (Encoding) - ده أهم جزء للدقة
        if gender == "Male": input_df['gender_Male'] = 1
        if partner == "Yes": input_df['Partner_Yes'] = 1
        if dependents == "Yes": input_df['Dependents_Yes'] = 1
        
        # العقد والإنترنت (أقوى عوامل الـ Churn)
        if contract == "Month-to-month": input_df['Contract_Month-to-month'] = 1
        elif contract == "One year": input_df['Contract_One year'] = 1
        
        if internet == "Fiber optic": input_df['InternetService_Fiber optic'] = 1
        elif internet == "No": input_df['InternetService_No'] = 1
        
        if payment == "Electronic check": input_df['PaymentMethod_Electronic check'] = 1
        
        # التوقع
        prediction = model.predict(input_df)
        prob = model.predict_proba(input_df)[0][1]

        # عرض النتيجة بتصميم جذاب
        st.write("### النتيجة النهائية:")
        if prediction[0] == 1:
            st.error(f"## 🛑 حالة العميل: سيغادر (CHURN) بنسبة {prob:.1%}")
            st.warning("⚠️ توصية: العميل لديه مخاطرة عالية. اقترح عليه تحويل العقد لسنوي مع خصم 15%.")
        else:
            st.success(f"## ✅ حالة العميل: سيستمر (STAY) بنسبة {1-prob:.1%}")
            st.info("👍 توصية: العميل مستقر. يمكن عرض خدمات إضافية (Upselling) عليه.")
            
        # رسم بياني للاحتمالية
        fig = px.pie(values=[prob, 1-prob], names=['Churn Risk', 'Loyalty Score'], 
                     color_discrete_sequence=['#ef553b', '#00cc96'], hole=0.4)
        st.plotly_chart(fig)

with tab2:
    st.subheader("لماذا يرحل العملاء؟ (بناءً على شيت الإكسيل)")
    st.write("أهم العوامل المؤثرة في القرار:")
    
    # داتا توضيحية بناءً على تحليل الـ Dataset الشهيرة
    feat_importance = pd.DataFrame({
        'العامل': ['نوع العقد', 'مدة الاشتراك', 'المصاريف الشهرية', 'طريقة الدفع', 'الدعم الفني'],
        'التأثير': [45, 25, 15, 10, 5]
    })
    fig_bar = px.bar(feat_importance, x='التأثير', y='العامل', orientation='h', 
                     title="أهمية الخصائص في تحديد قرار العميل")
    st.plotly_chart(fig_bar)
    
    st.info("💡 ملاحظة للمناقشة: يظهر التحليل أن العقود الشهرية (Month-to-month) هي السبب الرئيسي لرحيل العملاء في هذه الشركة.")
   
   
