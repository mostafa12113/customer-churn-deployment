# --- جزء معالجة البيانات الجديد ---
if st.button("🔍 تحليل عميق لحالة العميل"):
    # 1. إنشاء DataFrame بكل الأعمدة اللي الموديل متدرب عليها وتصفيرها
    input_df = pd.DataFrame(0, index=[0], columns=columns)
    
    # 2. ملء القيم الرقمية مباشرة
    input_df['tenure'] = tenure
    input_df['MonthlyCharges'] = monthly_charges
    input_df['TotalCharges'] = total_charges
    input_df['SeniorCitizen'] = senior

    # 3. الـ Encoding اليدوي (ده اللي بيخلي الموديل يحس بالفرق)
    # تحويل الجنس
    if gender == "Male": input_df['gender_Male'] = 1
    
    # تحويل العقد (أهم ميزة للـ Churn)
    if contract == "Month-to-month": input_df['Contract_Month-to-month'] = 1
    elif contract == "One year": input_df['Contract_One year'] = 1
    elif contract == "Two year": input_df['Contract_Two year'] = 1

    # تحويل نوع الإنترنت
    if internet == "Fiber optic": input_df['InternetService_Fiber optic'] = 1
    elif internet == "DSL": input_df['InternetService_DSL'] = 1

    # تحويل الخدمات الإضافية
    if security == "Yes": input_df['OnlineSecurity_Yes'] = 1
    if support == "Yes": input_df['TechSupport_Yes'] = 1
    
    # 4. تنفيذ التوقع
    prediction = model.predict(input_df)
    probability = model.predict_proba(input_df)[0][1]

    # --- عرض النتيجة بذكاء ---
    st.write("---")
    if prediction[0] == 1:
        st.error(f"🚨 النتيجة: العميل في خطر مغادرة عالٍ ({probability:.1%})")
        st.progress(probability)
    else:
        st.success(f"✅ النتيجة: العميل مستقر ومن المحتمل بقاؤه ({1-probability:.1%})")
