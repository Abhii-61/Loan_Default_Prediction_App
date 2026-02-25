# ==============================
# IMPORTS
# ==============================
import streamlit as st
import pandas as pd
import joblib

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Loan Default Prediction",
    page_icon="💰",
    layout="centered"
)

# ==============================
# LOAD MODEL
# ==============================
@st.cache_resource
def load_model():
    model = joblib.load("model/model.pkl")
    return model

model = load_model()

# ==============================
# TITLE
# ==============================
st.title("💰 Loan Default Prediction App")
st.markdown("Predict whether a customer will **not fully pay the loan**.")

st.divider()

# ==============================
# USER INPUT
# ==============================
st.subheader("📊 Enter Customer Details")

credit_policy = st.selectbox("Credit Policy", [0, 1])
purpose = st.selectbox(
    "Loan Purpose",
    ["credit_card", "debt_consolidation", "home_improvement",
     "major_purchase", "small_business", "all_other"]
)
int_rate = st.number_input("Interest Rate", value=0.10)
installment = st.number_input("Installment", value=100.0)
log_annual_inc = st.number_input("Log Annual Income", value=10.0)
dti = st.number_input("Debt-to-Income Ratio", value=10.0)
fico = st.number_input("FICO Score", value=700)
days_with_cr_line = st.number_input("Days with Credit Line", value=4000)
revol_bal = st.number_input("Revolving Balance", value=5000)
revol_util = st.number_input("Revolving Utilization", value=50.0)
inq_last_6mths = st.number_input("Inquiries (Last 6 Months)", value=1)
delinq_2yrs = st.number_input("Delinquencies (2 yrs)", value=0)
pub_rec = st.number_input("Public Records", value=0)

# ==============================
# CREATE INPUT DATAFRAME
# ==============================
input_data = pd.DataFrame({
    "credit.policy": [credit_policy],
    "purpose": [purpose],
    "int.rate": [int_rate],
    "installment": [installment],
    "log.annual.inc": [log_annual_inc],
    "dti": [dti],
    "fico": [fico],
    "days.with.cr.line": [days_with_cr_line],
    "revol.bal": [revol_bal],
    "revol.util": [revol_util],
    "inq.last.6mths": [inq_last_6mths],
    "delinq.2yrs": [delinq_2yrs],
    "pub.rec": [pub_rec],

})

# Convert log income back to actual income
annual_income = 10 ** log_annual_inc

# 1️⃣ Income to Installment Ratio
input_data["income_to_installment_ratio"] = annual_income / installment

# 2️⃣ Credit Utilization Ratio
input_data["credit_utilization_ratio"] = revol_util / 100  # since revol.util is %

# ==============================
# PREDICTION
# ==============================
if st.button("🔍 Predict"):
    prediction = model.predict(input_data)[0]

    st.divider()

    if prediction == 1:
        st.error("⚠️ High Risk: Customer may NOT fully pay the loan")
    else:
        st.success("✅ Low Risk: Customer is likely to repay the loan")

    st.subheader("📌 Input Summary")
    st.dataframe(input_data)