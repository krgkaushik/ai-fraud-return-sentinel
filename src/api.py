import os
import requests
import pandas as pd
import joblib
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Return-Risk Sentinel API")

# Enable CORS for browser integrations and dashboards
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained machine learning model
model_path = os.path.join("models", "risk_model.pkl")
model = joblib.load(model_path)

# Pydantic schema for incoming transaction data
class Transaction(BaseModel):
    past_orders_count: int
    past_returns_count: int
    account_age_days: int
    cart_value_usd: float

def trigger_automation(customer_email: str, risk_score: float, order_amount: float):
    # Replace with your Make.com or webhook automation URL
    make_webhook_url = "https://hook.make.com/your_unique_webhook_id"
    
    tier = "CRITICAL" if risk_score > 85 else "HIGH"
    data = {
        "email": customer_email,
        "alert": "High Return Risk Detected",
        "score": risk_score,
        "risk_tier": tier,
        "amount_inr": order_amount,
        "action_required": "Manual Verification / Hold Shipment"
    }
    
    try:
        response = requests.post(make_webhook_url, json=data, timeout=5)
        print(f"Make.com Webhook triggered: Status {response.status_code}")
    except Exception as e:
        print(f"Webhook background task failed: {e}")

@app.post("/score")
def score_transaction(tx: Transaction, background_tasks: BackgroundTasks):
    df = pd.DataFrame([tx.model_dump()])
    risk_prob = float(model.predict_proba(df)[0][1] * 100)
    
    decision = "BLOCK" if risk_prob > 75 else "ALLOW"
    
    # Trigger non-blocking automation for high risk threats
    if decision == "BLOCK":
        background_tasks.add_task(
            trigger_automation, 
            customer_email="merchant_alert@store.com", 
            risk_score=risk_prob, 
            order_amount=tx.cart_value_usd * 83
        )
        
    return {
        "risk_score": round(risk_prob, 2),
        "decision": decision
    }