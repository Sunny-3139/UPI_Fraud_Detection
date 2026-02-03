import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import joblib
from datetime import datetime
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load the model and scaler - SAME AS APP.PY
model = tf.keras.models.load_model('upi_fraud_model.h5')
scaler = joblib.load('scaler.pkl')

# Load label encoders by fitting on training data - SAME AS APP.PY
df_train = pd.read_csv('transactions.csv')

le_state = LabelEncoder()
le_state.fit(df_train['State'].values)

le_merchant = LabelEncoder()
le_merchant.fit(df_train['Merchant_Category'].values)

# Load the transactions CSV
df = pd.read_csv('transactions.csv')

print("=" * 100)
print("MODEL PREDICTION ANALYSIS (USING APP.PY LOGIC)")
print("=" * 100)

for idx, row in df.head(6).iterrows():
    # Extract data
    upi = row['UPI_Number']
    holder_name = row['Holder_Name']
    state = row['State']
    trans_datetime = row['Transaction_DateTime']
    seller_name = row['Seller_Name']
    dob = row['Date_of_Birth']
    pin_code = row['Pincode']
    amount = row['Amount_Rs']
    merchant_category = row['Merchant_Category']
    fraud_label = row['Fraud_Label']
    
    # Parse transaction datetime - SAME AS APP.PY
    trans_dt = datetime.strptime(trans_datetime, '%Y-%m-%d %H:%M')
    hour = trans_dt.hour
    day_of_week = trans_dt.weekday()
    
    # Calculate age - SAME AS APP.PY
    dob_dt = datetime.strptime(dob, '%Y-%m-%d')
    current_year = datetime.now().year
    age = current_year - dob_dt.year
    
    # Encode categorical features - SAME AS APP.PY
    state_encoded = le_state.transform([state])[0]
    merchant_encoded = le_merchant.transform([merchant_category])[0]
    
    # Prepare features - SAME AS APP.PY
    # Order: Pincode, Amount_Rs, Merchant_Category, State, hour, day_of_week, age
    features = np.array([[
        float(pin_code),
        amount,
        merchant_encoded,
        state_encoded,
        hour,
        day_of_week,
        age
    ]])
    
    # Standardize
    features_scaled = scaler.transform(features)
    
    # Predict
    prediction_prob = model.predict(features_scaled, verbose=0)[0][0]
    
    # HYBRID APPROACH: Combine neural network with rule-based detection
    rule_based_fraud = False
    fraud_reasons = []
    
    # Rule 1: High amount + unusual hour
    if amount > 40000 and (hour < 6 or hour > 23):
        rule_based_fraud = True
        fraud_reasons.append("High Amount (>40k) at Unusual Hour")
    
    # Rule 2: Very high amount
    if amount > 75000:
        rule_based_fraud = True
        fraud_reasons.append("Transaction Limit Exceeded (>75k)")
    
    # Rule 3: Cash Out/Transfer at night
    if merchant_category == "Cash Out / Transfer" and (hour < 6 or hour > 22):
        rule_based_fraud = True
        fraud_reasons.append("Cash Transfer at Unusual Hour")
    
    # Rule 4: Multiple high transactions (anomaly)
    if amount > 25000 and merchant_category == "Cash Out / Transfer":
        rule_based_fraud = True
        fraud_reasons.append("Suspicious Cash Transfer Amount")
    
    # Rule 5: Moderate/High amount at night on unusual hours
    if amount > 8000 and (hour > 21 or hour < 7):
        rule_based_fraud = True
        fraud_reasons.append("Moderate-High Amount at Night")
    
    # Combine rule-based with neural network
    is_fraud = rule_based_fraud or prediction_prob > 0.3
    
    print(f"\nTransaction #{idx + 1}: {holder_name}")
    print(f"  Amount: {amount}, Hour: {hour}, Merchant: {merchant_category}")
    print(f"  NN Probability: {prediction_prob:.6f}")
    print(f"  Rule-Based Flags: {fraud_reasons if fraud_reasons else 'None'}")
    print(f"  Model Prediction: {'FRAUD' if is_fraud else 'VALID'}")
    print(f"  Actual Label: {'FRAUD' if fraud_label == 1 else 'VALID'}")
    print(f"  Result: {'✓ CORRECT' if (is_fraud == (fraud_label == 1)) else '✗ INCORRECT'}")

print("\n" + "=" * 100)
