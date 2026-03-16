import streamlit as st
import pandas as pd
import joblib

# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📉",
    layout="wide"
)

st.title("📉 Customer Churn Prediction")
st.markdown(
"""
Predict whether a telecom customer is likely to **churn** based on their
demographics, account information, and service usage.
"""
)

# -------------------------
# Load Model
# -------------------------

model = joblib.load("churn_model.pkl")

# -------------------------
# User Input Section
# -------------------------

st.sidebar.header("Customer Information")

gender = st.sidebar.selectbox("Gender", ["Male", "Female"])

senior_option = st.sidebar.selectbox("Senior Citizen", ["No", "Yes"])

senior = 1 if senior_option == "Yes" else 0

partner = st.sidebar.selectbox("Partner", ["Yes","No"])

dependents = st.sidebar.selectbox("Dependents", ["Yes","No"])

tenure = st.sidebar.slider("Tenure (months)", 0, 72, 12)

phone_service = st.sidebar.selectbox("Phone Service", ["Yes","No"])

multiple_lines = st.sidebar.selectbox("Multiple Lines", ["Yes","No"])

internet_service = st.sidebar.selectbox(
    "Internet Service",
    ["DSL","Fiber optic","No"]
)

online_security = st.sidebar.selectbox("Online Security", ["Yes","No"])

online_backup = st.sidebar.selectbox("Online Backup", ["Yes","No"])

device_protection = st.sidebar.selectbox("Device Protection", ["Yes","No"])

tech_support = st.sidebar.selectbox("Tech Support", ["Yes","No"])

streaming_tv = st.sidebar.selectbox("Streaming TV", ["Yes","No"])

streaming_movies = st.sidebar.selectbox("Streaming Movies", ["Yes","No"])

contract = st.sidebar.selectbox(
    "Contract",
    ["Month-to-month","One year","Two year"]
)

paperless_billing = st.sidebar.selectbox("Paperless Billing", ["Yes","No"])

payment_method = st.sidebar.selectbox(
    "Payment Method",
    [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]
)

monthly_charges = st.sidebar.slider("Monthly Charges", 0.0, 150.0, 70.0)

total_charges = st.sidebar.slider("Total Charges", 0.0, 9000.0, 2000.0)

# -------------------------
# Create Input Data
# -------------------------

input_data = pd.DataFrame({
    "gender":[gender],
    "SeniorCitizen":[senior],
    "Partner":[partner],
    "Dependents":[dependents],
    "tenure":[tenure],
    "PhoneService":[phone_service],
    "MultipleLines":[multiple_lines],
    "InternetService":[internet_service],
    "OnlineSecurity":[online_security],
    "OnlineBackup":[online_backup],
    "DeviceProtection":[device_protection],
    "TechSupport":[tech_support],
    "StreamingTV":[streaming_tv],
    "StreamingMovies":[streaming_movies],
    "Contract":[contract],
    "PaperlessBilling":[paperless_billing],
    "PaymentMethod":[payment_method],
    "MonthlyCharges":[monthly_charges],
    "TotalCharges":[total_charges]
})

# -------------------------
# Prediction Section
# -------------------------

st.subheader("Prediction")

st.info("Enter customer information and click **Predict Churn**.")

if st.button("Predict Churn"):

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Churn Probability", f"{probability:.2%}")

    with col2:
        if probability < 0.3:
            st.success("🟢 Low Churn Risk")
        elif probability < 0.6:
            st.warning("🟡 Medium Churn Risk")
        else:
            st.error("🔴 High Churn Risk")

    if prediction == 1:
        st.error("⚠️ Customer Likely to Churn")
    else:
        st.success("✅ Customer Likely to Stay")

    st.subheader("Input Summary")
    st.dataframe(input_data)