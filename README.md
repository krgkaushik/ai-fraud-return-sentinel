# 🛡️ Merchant Risk Sentinel: AI-Driven Return Risk & Fraud Prevention Layer

> **Razorpay Hackathon Submission** — Intercepting silent profit bleed by predicting high-risk and fraudulent returns *before* order fulfillment.

---

## 🚀 Overview
Every year, e-commerce merchants lose billions of dollars to profit margin bleed caused by **serial returners**, wardrobing, and reverse-logistics overhead. Traditional payment gateways tell merchants if a payment went through, but they fail to answer the critical next question: *"Is this customer going to return the item?"*

**Merchant Risk Sentinel** solves this by inserting an intelligent AI layer right between payment capture (via Razorpay webhooks) and warehouse dispatch. It scores incoming orders in milliseconds based on **User Order History**, allowing merchants to automatically hold suspicious shipments and protect their bottom lines.

---

## 📊 Project Objectives & What It Solves

* **Pre-Fulfillment Risk Scoring:** Evaluates e-commerce transactions in real-time right after payment completion to predict the probability of a return or chargeback before the product is packed or shipped.
* **Stops Reverse-Logistics Bleed:** Prevents online stores from losing money on shipping costs, packaging, and non-refundable gateway fees when serial returners abuse return policies.
* **Bridges Post-Payment Vulnerabilities:** Operates immediately after payment capture to freeze high-risk orders (*On Hold*) before physical fulfillment expenses are incurred.
* **Eliminates Manual Review Fatigue:** Automatically flags high-frequency offenders based on user order history while clearing normal, trustworthy customers instantly.

---

## 🛠️ System Architecture & Tech Stack

```text
[Razorpay / Webhook] ➔ [FastAPI Backend] ➔ [Random Forest ML Model] 
                                                    │
                   ┌────────────────────────────────┴────────────────────────────────┐
                   ▼                                                                 ▼
[Streamlit Merchant Dashboard (Live Feed & ROI)]                 [Background Tasks ➔ Make.com / WhatsApp Alerts]




Machine Learning: Python, Scikit-Learn (Random Forest Classifier with balanced class weights for severe data imbalance).

Backend API: FastAPI, Pydantic, Uvicorn, Joblib (with asynchronous BackgroundTasks).

Frontend Dashboard: Streamlit, Pandas, Requests (Live transaction management table, risk badges, and ROI financial impact metrics).

Automation: Make.com webhooks for instant WhatsApp/Email alerts.

⚠️ Build Challenges & Technical Obstacles Overcome
Linux Server Build Failures: Cloud deployments initially crashed due to incompatible local audio libraries (PyAudio) and Windows-specific packages (pywin32).

Solution: Cleaned up requirements.txt by removing local audio dependencies and integrated platform-specific environment markers (sys_platform == 'win32').

Severe Data Class Imbalance: Fraudulent returns naturally account for only ~2% of baseline data, causing standard models to overlook threats.

Solution: Engineered custom synthetic training datasets reflecting user behavior history and applied balanced class weights to the Random Forest model.

Frontend-Backend Disconnection: Streamlit and FastAPI occasionally threw JSON parsing errors during live traffic testing.

Solution: Enabled CORS middleware and structured standardized JSON payloads for seamless communication.

🚀 Local Installation & Quickstart
Follow these steps to run the project locally:

1. Clone the Repository & Setup Environment
Bash
git clone [https://github.com/YOUR_USERNAME/ai-fraud-return-sentinel.git](https://github.com/YOUR_USERNAME/ai-fraud-return-sentinel.git)
cd ai-fraud-return-sentinel
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
2. Install Dependencies
Bash
pip install -r requirements.txt
3. Train the Machine Learning Model
Generate the synthetic historical dataset and compile the model artifact:

Bash
python src/train_model.py
4. Run the FastAPI Backend (Terminal 1)
Bash
uvicorn src.api:app --reload --port 8000
5. Run the Streamlit Dashboard (Terminal 2)
Bash
streamlit run src/dashboard.py
☁️ Cloud Deployment
Backend API: Deployed as a web service on Render using standard production start commands.

Frontend Dashboard: Deployed live on Streamlit Community Cloud, connected directly to the production API URL.

🏆 Hackathon Impact
By moving risk detection from post-return loss processing to pre-fulfillment interception, Merchant Risk Sentinel gives merchants absolute control over their fulfillment pipelines, securing profit margins that traditional payment infrastructure misses entirely.
