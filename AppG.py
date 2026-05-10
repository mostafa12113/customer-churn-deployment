import streamlit as st
import pandas as pd
import joblib

# 1. إعدادات الصفحة الاحترافية (لازم أول سطر)
st.set_page_config(page_title="Telco Intelligence Dashboard", layout="wide")

# 2. تحميل الموديل والأعمدة
@st.cache_resource
def load_assets():
    model = joblib.load('model.pkl')
    columns = joblib.load('columns.pkl')
    return model, columns

try:
    model, columns = load_assets()
except Exception as e:
    st.error("Error loading model files. Please check model.pkl and columns.pkl")

# --- الـ Sidebar (لوحة التحكم الجانبية) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=80)
st.sidebar.title("Configuration")
st.sidebar.markdown("---")

with st.sidebar:
    st.subheader("👤 Customer Profile")
    gender = st.selectbox("Gender", ["Female", "Male"])
    senior = st.selectbox("Senior Citizen", [0, 1])
    tenure = st.slider("Tenure (Months)", 0, 72, 12)
    
    st.subheader("🌐 Services")
    internet = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
    payment = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer", "Credit card"])

    st.subheader("💰 Financials")
    monthly_charges = st.number_input("Monthly Charges ($)", value=65.0)
    total_charges = st.number_input("Total Charges ($)", value=monthly_charges * tenure)

# --- الصفحة الرئيسية ---
st.title("📊 Telco Customer Churn Intelligence")
st.markdown("This dashboard uses **Machine Learning** to predict customer loyalty based on behavioral patterns.")
st.write("---")

# عرض ملخص البيانات المختارة في كروت (Metrics)
col_a, col_b, col_c = st.columns(3)
col_a.metric("Selected Tenure", f"{tenure} Months")
col_b.metric("Monthly Cost", f"${monthly_charges}")
col_c.metric("Contract Type", contract)

st.write("---")

# زر التوقع بتصميم كبير
if st.button("🔍 RUN AI ANALYSIS", use_container_width=True):
    # تجهيز الداتا
    input_df = pd.DataFrame(0, index=[0], columns=columns)
    
    # ملء البيانات الرقمية
    input_df['tenure'] = tenure
    input_df['MonthlyCharges'] = monthly_charges
    input_df['TotalCharges'] = total_charges
    input_df['SeniorCitizen'] = senior
    input_df['gender'] = 1 if gender == "Male" else 0

    # أهم خطوة: الـ Encoding اليدوي عشان الموديل يتفاعل
    if contract == "Month-to-month":
        if 'Contract_Month-to-month' in columns: input_df['Contract_Month-to-month'] = 1
    elif contract == "One year":
        if 'Contract_One year' in columns: input_df['Contract_One year'] = 1

    if internet == "Fiber optic":
        if 'InternetService_Fiber optic' in columns: input_df['InternetService_Fiber optic'] = 1
    elif internet == "DSL":
        if 'InternetService_DSL' in columns: input_df['InternetService_DSL'] = 1

    if payment == "Electronic check":
        if 'PaymentMethod_Electronic check' in columns: input_df['PaymentMethod_Electronic check'] = 1

    # تنفيذ التوقع
    prediction = model.predict(input_df)
    probability = model.predict_proba(input_df)[0][1]

    # عرض النتيجة النهائية
    st.subheader("🎯 Analysis Result:")
    
    res_col1, res_col2 = st.columns([2, 1])
    
    with res_col1:
        if prediction[0] == 1 or probability > 0.5:
            st.error(f"### Result: Customer is likely to CHURN")
            st.write(f"The model is **{probability:.1%}** confident that this customer will leave.")
            st.progress(probability)
        else:
            st.success(f"### Result: Customer is likely to STAY")
            st.write(f"The model is **{(1-probability):.1%}** confident that this customer is loyal.")
            st.progress(1 - probability)
            
    with res_col2:
        st.write("💡 **Recommendation:**")
        if prediction[0] == 1:
            st.write("- Offer a discount immediately.\n- Suggest switching to a 1-year contract.")
        else:
            st.write("- Great customer loyalty.\n- Consider upselling premium services.")
  


  
