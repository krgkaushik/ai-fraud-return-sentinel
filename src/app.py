import streamlit as st
import pandas as pd
import random
import requests

st.set_page_config(page_title="Merchant Risk Sentinel", layout="wide", initial_sidebar_state="expanded")

API_URL = "http://localhost:8000/score"

# Initialize Session State Database Mock
if "orders" not in st.session_state:
    st.session_state.orders = [
        {"id": "order_N182x9", "email": "repeat.offender@gmail.com", "amount": 3499, "past_orders": 15, "past_returns": 9, "risk_score": 88, "status": "Pending Verification"},
        {"id": "order_P92k11", "email": "new.buyer@yahoo.com", "amount": 1200, "past_orders": 1, "past_returns": 0, "risk_score": 42, "status": "Processing"},
        {"id": "order_A108z4", "email": "loyal.customer@gmail.com", "amount": 850, "past_orders": 45, "past_returns": 1, "risk_score": 8, "status": "Ready to Ship"},
    ]

# Dashboard Header
st.title("🛡️ Merchant Risk Sentinel")
st.markdown("Preventing logistics margin loss by predicting fraudulent returns using **User Order History**.")

# KPI Calculations
total_orders = len(st.session_state.orders)
high_risk_count = sum(1 for o in st.session_state.orders if o["risk_score"] >= 75)
revenue_at_risk = sum(o["amount"] for o in st.session_state.orders if o["risk_score"] >= 75 and o["status"] != "On Hold")

col1, col2, col3 = st.columns(3)
col1.metric("Live Orders (Today)", total_orders)
col2.metric("High Risk Threats ⚠️", high_risk_count)
col3.metric("Revenue at Risk", f"₹{revenue_at_risk:,.2f}")

st.divider()

# Order Feed Table
st.subheader("Live Transaction & Return-Risk Feed")

header_cols = st.columns((1.5, 2, 1, 2, 2, 2, 2))
header_cols[0].markdown("**Order ID**")
header_cols[1].markdown("**Customer**")
header_cols[2].markdown("**Amount**")
header_cols[3].markdown("**User History**")
header_cols[4].markdown("**Return Risk**")
header_cols[5].markdown("**Status**")
header_cols[6].markdown("**Action**")

st.markdown("---")

for i, order in enumerate(st.session_state.orders):
    cols = st.columns((1.5, 2, 1, 2, 2, 2, 2))
    
    cols[0].write(f"`{order['id']}`")
    cols[1].write(order['email'])
    cols[2].write(f"₹{order['amount']}")
    
    if order['past_returns'] > 0:
        cols[3].markdown(f"📦 {order['past_orders']} Orders | <span style='color:red;'>⚠️ {order['past_returns']} Returns</span>", unsafe_allow_html=True)
    else:
        cols[3].markdown(f"📦 {order['past_orders']} Orders | ✅ 0 Returns")
    
    risk = order['risk_score']
    if risk >= 75:
        risk_html = f"<span style='color: white; background-color: #ff4b4b; padding: 4px 8px; border-radius: 4px; font-weight: bold;'>{risk}% (High)</span>"
    elif risk >= 40:
        risk_html = f"<span style='color: black; background-color: #ffa500; padding: 4px 8px; border-radius: 4px; font-weight: bold;'>{risk}% (Med)</span>"
    else:
        risk_html = f"<span style='color: white; background-color: #00cc66; padding: 4px 8px; border-radius: 4px; font-weight: bold;'>{risk}% (Low)</span>"
    
    cols[4].markdown(risk_html, unsafe_allow_html=True)
    
    if order["status"] == "On Hold":
        cols[5].markdown(f"🛑 **{order['status']}**")
    elif order["status"] == "Cleared":
        cols[5].markdown(f"✅ **{order['status']}**")
    else:
        cols[5].write(order["status"])
    
    if order["status"] not in ["On Hold", "Cleared"]:
        if risk >= 75:
            if cols[6].button("Hold Shipment", key=f"hold_{i}", type="primary"):
                st.session_state.orders[i]["status"] = "On Hold"
                st.rerun() 
        else:
            if cols[6].button("Clear Order", key=f"clear_{i}"):
                st.session_state.orders[i]["status"] = "Cleared"
                st.rerun() 
    else:
        cols[6].write("—") 

st.divider()

# Financial Impact ROI Section
st.subheader("📊 Business Margin Protection")
total_saved = sum(o["amount"] for o in st.session_state.orders if o["status"] == "On Hold")
chart_data = pd.DataFrame({
    "Category": ["Protected Margin", "Unmitigated Loss Risk"],
    "Amount (₹)": [total_saved, 12500]
})
st.bar_chart(chart_data.set_index("Category"))

# Simulation Sidebar Control
with st.sidebar:
    st.header("Simulate Razorpay Webhook")
    demo_type = st.radio("Behavior Profile:", ["Normal Buyer", "Serial Returner"])
    
    if st.button("Simulate Incoming Payment", type="primary"):
        if demo_type == "Normal Buyer":
            payload = {"past_orders_count": 8, "past_returns_count": 0, "account_age_days": 400, "cart_value_usd": 35}
            email = f"buyer_{random.randint(100,999)}@gmail.com"
        else:
            payload = {"past_orders_count": 14, "past_returns_count": 10, "account_age_days": 40, "cart_value_usd": 150}
            email = f"abuser_{random.randint(100,999)}@tempmail.com"
            
        try:
            res = requests.post(API_URL, json=payload).json()
            new_order = {
                "id": f"order_{random.randint(100000, 999999)}",
                "email": email,
                "amount": int(payload["cart_value_usd"] * 83),
                "past_orders": payload["past_orders_count"],
                "past_returns": payload["past_returns_count"],
                "risk_score": res["risk_score"],
                "status": "Pending Verification"
            }
            st.session_state.orders.insert(0, new_order)
            st.rerun()
        except Exception as e:
            st.error(f"Connection failed. Is FastAPI running? Error: {e}")