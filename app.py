import streamlit as st
import plotly.graph_objects as go
import os
import sys
import math

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# PAGE CONFIG
st.set_page_config(
    page_title="Loan Repayment Risk Prediction",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
.header {
    background: linear-gradient(135deg, #1e3a5f, #2d5a87);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.risk-high {
    background: #dc3545;
    color: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    font-size: 1.8rem;
    font-weight: bold;
}
.risk-low {
    background: #28a745;
    color: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    font-size: 1.8rem;
    font-weight: bold;
}
.reason-box {
    background: #2c2c1a;
    border-left: 6px solid #ffc107;
    padding: 1rem;
    border-radius: 8px;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="header">
    <h1>Loan Repayment Risk Prediction</h1>
    <p>AI-Powered Credit Risk Assessment</p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR INPUTS
st.sidebar.markdown("### Loan Application Details")

age = st.sidebar.slider("Age", 21, 65, 30)
employment_years = st.sidebar.slider("Employment Years", 0, 40, 2)

st.sidebar.markdown("### Financial Information")
income = st.sidebar.number_input("Annual Income (₹)", 5000, 100000000, 600000, step=5000)
credit_score = st.sidebar.slider("Credit Score", 300, 850, 700)
existing_loans = st.sidebar.selectbox("Existing Loans", [0, 1, 2, 3, 4], index=0)

st.sidebar.markdown("### Loan Details")
loan_amount = st.sidebar.number_input("Loan Amount (₹)", 5000, 5000000000, 300000, step=10000)
loan_term = st.sidebar.selectbox("Loan Term (months)", [12, 24, 36, 48, 60], index=2)
interest_rate = st.sidebar.slider("Interest Rate (%)", 5.0, 30.0, 12.0)

predict = st.sidebar.button("Predict Risk", use_container_width=True)

# EMI FUNCTION
def calculate_emi(P, rate, months):
    r = rate / (12 * 100)
    return P * r * (1+r)**months / ((1+r)**months - 1)

# SAMPLE DATA (WHEN NOT PREDICTED)
if not predict:
    st.info(" Sample Loan Profiles")

    col1, col2 = st.columns(2)

    with col1:
        st.success(" **LOW RISK SAMPLE**")
        st.write("""
        - Credit Score: **780**
        - Annual Income: **₹12,00,000**
        - Loan Amount: **₹3,00,000**
        - Interest Rate: **10%**
        - Loan Term: **36 months**
        """)

    with col2:
        st.error(" **HIGH RISK SAMPLE**")
        st.write("""
        - Credit Score: **520**
        - Annual Income: **₹4,00,000**
        - Loan Amount: **₹5,00,000**
        - Interest Rate: **22%**
        - Loan Term: **12 months**
        """)

# PREDICTION LOGIC
if predict:

    monthly_income = income / 12
    emi = calculate_emi(loan_amount, interest_rate, loan_term)
    dti = emi / monthly_income

    reasons = []

    if credit_score < 650:
        reasons.append("Low Credit Score (< 650)")

    if interest_rate >= 20:
        reasons.append("High Interest Rate (≥ 20%)")

    if existing_loans >= 3:
        reasons.append("Too Many Existing Loans")

    if dti > 0.4:
        reasons.append("EMI exceeds 40% of monthly income")

    # FINAL DECISION
    if reasons:
        risk = "High"
        repay_prob = 0
        default_prob = 100
    else:
        risk = "Low"
        repay_prob = 100
        default_prob = 0

    # RISK CARD
    if risk == "High":
        st.markdown("""
        <div class="risk-high">
             HIGH RISK<br>
            <small>Likely to Default</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="risk-low">
             LOW RISK<br>
            <small>Likely to Repay</small>
        </div>
        """, unsafe_allow_html=True)

    # SHOW REASONS IF HIGH RISK
    if risk == "High":
        st.markdown("<div class='reason-box'><b>⚠ High Risk due to:</b>", unsafe_allow_html=True)
        for r in reasons:
            st.markdown(f"- {r}")
        st.markdown(f"""
        <br> Monthly EMI: ₹{emi:,.0f}<br>
         Monthly Income: ₹{monthly_income:,.0f}
        </div>
        """, unsafe_allow_html=True)

    # GAUGES
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(go.Figure(go.Indicator(
            mode="gauge+number",
            value=repay_prob,
            title={"text": "Repayment Probability"},
            gauge={"axis": {"range": [0, 100]}}
        )), use_container_width=True)

    with col2:
        st.plotly_chart(go.Figure(go.Indicator(
            mode="gauge+number",
            value=default_prob,
            title={"text": "Default Probability"},
            gauge={"axis": {"range": [0, 100]}}
        )), use_container_width=True)

    # APPLICATION SUMMARY
    st.markdown("###  Application Summary")
    a, b, c, d = st.columns(4)
    a.metric("Loan Amount", f"₹{loan_amount:,.0f}")
    b.metric("Monthly Payment", f"₹{emi:,.0f}")
    c.metric("Debt-to-Income", f"{dti:.2f}")
    d.metric("Credit Score", credit_score)

# FOOTER
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#777;'>Loan Risk Prediction System | 2025–2026</div>",
    unsafe_allow_html=True
)
