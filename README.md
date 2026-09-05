# 🛡️ Merchant Risk Sentinel: AI-Driven Return Risk & Fraud Prevention Layer

> **Razorpay Hackathon Submission** — Intercepting silent profit bleed by predicting high-risk and fraudulent returns *before* order fulfillment.

---

## 📌 Project Overview

E-commerce merchants lose billions of dollars annually to profit margin bleed caused by **serial returners**, wardrobing, and reverse-logistics overhead. Traditional payment gateways only verify if a payment went through, but they fail to answer the critical question: *"Is this customer going to return the item?"*

**Merchant Risk Sentinel** solves this by inserting an intelligent AI layer right between payment capture (via Razorpay webhooks) and warehouse dispatch. It scores incoming orders in milliseconds based on **User Order History**, allowing merchants to automatically hold suspicious shipments and protect their bottom lines.

The workflow includes:
- Capturing payment data via Razorpay webhooks
- Tracking user order and return history
- Scoring risk using a Random Forest machine learning model
- Managing incoming transactions via a live Streamlit merchant command center
- Triggering automated asynchronous alerts (WhatsApp/Make.com) for high-risk orders

---

## 🚀 Features

- **Pre-Fulfillment Risk Scoring:** Evaluates e-commerce transactions in real time right after payment completion.
- **User History Analysis:** Analyzes past order counts, past return history, account age, and cart value.
- **Live Merchant Command Center:** Displays a real-time transaction feed with intuitive risk tiers (High, Medium, Low).
- **Manual Review Action Buttons:** Allows merchants to instantly click **"Hold Shipment"** or **"Clear Order"**.
- **Automated Background Workflows:** Dispatches alerts via Make.com without introducing latency into the core API.
- **Business ROI Analytics:** Tracks financial metrics such as net margin protected and risk mitigation value directly on the dashboard.

---

## 🛠 Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| FastAPI & Uvicorn | High-Performance Backend API & Background Tasks |
| Streamlit | Merchant Dashboard & Command Center UI |
| Scikit-Learn | Random Forest Machine Learning Model |
| Pandas & NumPy | Data Processing & Feature Engineering |
| Joblib | Model Serialization & Loading |
| Requests & Make.com | Automated Webhook & WhatsApp Alerts |

---

## 📂 Project Structure

``1text
ai_fraud_detection/
│
├── models/
│   └── risk_model.pkl
├── src/
│   ├── train_model.py
│   ├── api.py
│   └── dashboard.py
├── requirements.txt
└── README.md``

📊 Dataset & Model Training
The project relies on a custom-engineered training pipeline that models user behavior history, emphasizing past returns and order frequency to predict future return risks.

Target Variable: is_fraudulent_return (binary classification)

Features: past_orders_count, past_returns_count, account_age_days, cart_value_usd

Handling Imbalance: Applied balanced class weights within the Random Forest classifier to accurately capture rare high-risk return patterns.

⚙ Installation
Clone the repository:
`git clone [https://github.com/YOUR_USERNAME/ai-fraud-return-sentinel.git](https://github.com/YOUR_USERNAME/ai-fraud-return-sentinel.git)`

Move into the project folder:
`cd ai-fraud-return-sentinel`

Create and activate a virtual environment:
`python -m venv venv`

On Windows:
`venv\Scripts\activate`

On Linux/Mac:
`source venv/bin/activate`

Install dependencies:
`pip install -r requirements.txt`

▶ Running the Project
1. Train the Machine Learning Model
Generate the historical training dataset and compile the model artifact:
`python src/train_model.py`

2. Run the FastAPI Backend (Terminal 1)
Start the API server to handle real-time scoring and background automation:
`uvicorn src.api:app --reload --port 8000`

3. Run the Streamlit Dashboard (Terminal 2)
Launch the live merchant command center:
`streamlit run src/dashboard.py`

🧠 Model Architecture
The prediction model leverages an optimized ensemble learning approach:

Random Forest Classifier

Balanced Class Weighting (to address severe class skew)

Real-time Inference via FastAPI endpoints

Architecture Flow:
`
[Razorpay Webhook] ➔ [FastAPI] ➔ [Random Forest AI] 
                                       │
                ┌──────────────────────┴──────────────────────┐
                ▼                                             ▼
[Streamlit Merchant Dashboard]             [Background Tasks ➔ WhatsApp/Make.com]`

⚠️ Build Challenges & Technical Obstacles Overcome
Linux Server Build Failures: Cloud deployments initially crashed due to incompatible local audio libraries (PyAudio) and Windows-specific packages (pywin32).

Solution: Cleaned up requirements.txt by removing local audio dependencies and integrated platform-specific environment markers (sys_platform == 'win32').

Severe Data Class Imbalance: Fraudulent returns naturally account for only ~2% of baseline data, causing standard models to overlook threats.

Solution: Engineered custom synthetic training datasets reflecting user behavior history and applied balanced class weights to the Random Forest model.

Frontend-Backend Disconnection: Streamlit and FastAPI occasionally threw JSON parsing errors during live traffic testing.

Solution: Enabled CORS middleware and structured standardized JSON payloads for seamless communication.

☁️ Cloud Deployment
Backend API: Deployed as a web service on Render using standard production start commands.

Frontend Dashboard: Deployed live on Streamlit Community Cloud, connected directly to the production API URL.

🏆 Hackathon Impact
By moving risk detection from post-return loss processing to pre-fulfillment interception, Merchant Risk Sentinel gives merchants absolute control over their fulfillment pipelines, securing profit margins that traditional payment infrastructure misses entirely.

👨‍💻 Author
Kaushik Rameshrao Gunjkar

Artificial Intelligence & Data Science Engineering Student

📜 License
This project is intended for educational, research, and hackathon demonstration purposes.
