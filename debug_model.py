import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import joblib
from datetime import datetime
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load the model and scaler
model = tf.keras.models.load_model('upi_fraud_model.h5')
scaler = joblib.load('scaler.pkl')

# Load label encoders
le_state = LabelEncoder()
le_merchant = LabelEncoder()

states = ['Maharashtra', 'Karnataka', 'Gujarat', 'Delhi', 'Punjab', 'Tamil Nadu', 'Kerala', 
          'Telangana', 'Bangalore', 'Mumbai', 'Pune', 'Hyderabad', 'Lucknow', 'Jaipur', 
          'Chandigarh', 'Ahmedabad', 'Surat', 'Indore', 'Bhopal', 'Vadodara', 'Gurgaon', 
          'Kolkata', 'Kanpur']
le_state.fit(states)

merchant_categories = ['Shopping', 'Cash Out / Transfer', 'Food & Dining', 'Healthcare', 
                       'Travel', 'Entertainment', 'Groceries', 'Bills & Utilities', 
                       'Fuel', 'Education', 'Online Services', 'Insurance']
le_merchant.fit(merchant_categories)

# Load the transactions CSV
df = pd.read_csv('transactions.csv')

print("=" * 100)
print("MODEL PREDICTION ANALYSIS")
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
    
    # Parse transaction datetime
    trans_dt = datetime.strptime(trans_datetime, '%Y-%m-%d %H:%M')
    hour = trans_dt.hour
    day_of_week = trans_dt.weekday()
    
    # Calculate age
    dob_dt = datetime.strptime(dob, '%Y-%m-%d')
    current_year = datetime.now().year
    age = current_year - dob_dt.year
    
    # Encode categorical features
    state_encoded = le_state.transform([state])[0]
    merchant_encoded = le_merchant.transform([merchant_category])[0]
    
    # Prepare features
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
    
    # Reshape for CNN
    features_scaled = features_scaled.reshape(features_scaled.shape[0], features_scaled.shape[1], 1)
    
    # Predict
    prediction_prob = model.predict(features_scaled, verbose=0)[0][0]
    is_fraud = prediction_prob > 0.5
    
    print(f"\nTransaction #{idx + 1}")
    print(f"  Name: {holder_name}")
    print(f"  Amount: ₹{amount}")
    print(f"  Time: {trans_datetime} (Hour: {hour})")
    print(f"  Category: {merchant_category}")
    print(f"  State: {state}")
    print(f"  Age: {age}")
    print(f"  Features (raw): pincode={pin_code}, amount={amount}, merchant_enc={merchant_encoded}, state_enc={state_encoded}, hour={hour}, day={day_of_week}, age={age}")
    print(f"  Prediction Probability: {prediction_prob:.4f}")
    print(f"  Model Prediction: {'🔴 FRAUD' if is_fraud else '✓ VALID'}")
    print(f"  Actual Label: {'🔴 FRAUD' if fraud_label == 1 else '✓ VALID'}")
    print(f"  ✓ CORRECT" if (is_fraud == (fraud_label == 1)) else f"  ✗ INCORRECT")

print("\n" + "=" * 100)

# Check scaler statistics
print("\nScaler Information:")
print(f"Mean of training data: {scaler.mean_}")
print(f"Scale (std) of training data: {scaler.scale_}")
