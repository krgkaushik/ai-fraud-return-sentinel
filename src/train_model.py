import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Ensure models directory exists
os.makedirs("models", exist_ok=True)
print("Generating user return history dataset...")

N = 10000
df = pd.DataFrame({
    'past_orders_count': np.random.randint(1, 50, N),
    'past_returns_count': np.random.randint(0, 10, N),
    'account_age_days': np.random.randint(1, 1000, N),
    'cart_value_usd': np.random.uniform(10, 1500, N),
    'is_fraudulent_return': np.random.choice([0, 1], p=[0.95, 0.05], size=N)
})

# Feature engineering: high past returns strongly correlate with risk
df.loc[df['is_fraudulent_return'] == 1, 'past_returns_count'] += 5

X = df.drop('is_fraudulent_return', axis=1)
y = df['is_fraudulent_return']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training model with balanced class weights...")
model = RandomForestClassifier(class_weight='balanced', max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Save artifact
joblib.dump(model, 'models/risk_model.pkl')
print("Success! Model saved to models/risk_model.pkl")