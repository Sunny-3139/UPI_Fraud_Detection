from flask import Flask, render_template, request, session, redirect, url_for
import datetime
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import joblib
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

# Simple user credentials (can be enhanced with database)
VALID_USERS = {
    'admin': 'admin123',
    'user': 'password123'
}

# Load the trained model and scaler
try:
    model = tf.keras.models.load_model('upi_fraud_model.h5')
    scaler = joblib.load('scaler.pkl')
    model_loaded = True
except Exception as e:
    print(f"Warning: Could not load model/scaler: {e}")
    model_loaded = False

# Load label encoders by fitting on training data
df_train = pd.read_csv('transactions.csv')

le_state = LabelEncoder()
le_state.fit(df_train['State'].values)

le_merchant = LabelEncoder()
le_merchant.fit(df_train['Merchant_Category'].values)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in VALID_USERS and VALID_USERS[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        # Capture all fields from the interface
        upi = request.form.get('upi_number')
        holder_name = request.form.get('holder_name')
        state = request.form.get('state')
        trans_time = request.form.get('trans_time')
        seller_name = request.form.get('seller_name')
        amount = float(request.form.get('amount', 0))
        merchant_category = request.form.get('merchant_category')
        
        # Parse transaction datetime to extract hour and day_of_week
        hour = 12  # default
        day_of_week = 0  # default
        if trans_time:
            try:
                trans_datetime = datetime.datetime.strptime(trans_time, '%Y-%m-%dT%H:%M')
                hour = trans_datetime.hour
                day_of_week = trans_datetime.weekday()
            except:
                pass
        
        # Encode categorical features
        try:
            state_encoded = le_state.transform([state])[0]
        except:
            state_encoded = 0
        
        try:
            merchant_encoded = le_merchant.transform([merchant_category])[0]
        except:
            merchant_encoded = 0
        
        # Prepare features in the same order as training
        # Order: Amount_Rs, Merchant_Category, State, hour, day_of_week
        features = np.array([[
            amount,
            merchant_encoded,
            state_encoded,
            hour,
            day_of_week
        ]])
        
        # Standardize using the saved scaler
        features_scaled = scaler.transform(features)
        
        # Make prediction
        prediction_prob = model.predict(features_scaled, verbose=0)[0][0]
        
        # HYBRID APPROACH: Combine neural network with rule-based detection
        # Rule-based fraud indicators
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
        if amount > 25000 and merchant_encoded == le_merchant.transform(["Cash Out / Transfer"])[0]:
            rule_based_fraud = True
            fraud_reasons.append("Suspicious Cash Transfer Amount")
        
        # Rule 5: Moderate/High amount at night on unusual hours
        if amount > 8000 and (hour > 21 or hour < 7):
            rule_based_fraud = True
            fraud_reasons.append("Moderate-High Amount at Night")
        
        # Combine rule-based with neural network
        # If neural network is uncertain or rules flag it, consider it fraud
        is_fraud = rule_based_fraud or prediction_prob > 0.3
        
        if is_fraud:
            prediction = f"🔴 FRAUD DETECTED"
            if fraud_reasons:
                prediction += f" (Reason: {', '.join(fraud_reasons)})"
            else:
                prediction += f" (Confidence: {prediction_prob*100:.1f}%)"
            color = "red"
        else:
            prediction = f"✓ VALID TRANSACTION (Confidence: {(1-prediction_prob)*100:.1f}%)"
            color = "green"
        
        # Return detailed result
        result_html = f"""
        <div style="background-color: {color}; color: white; padding: 30px; border-radius: 10px; text-align: center; margin: 20px;">
            <h1>{prediction}</h1>
            <h3>Transaction Details:</h3>
            <table style="margin: 20px auto; color: white; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid white;">
                    <td style="padding: 8px; text-align: left;"><b>UPI Number:</b></td>
                    <td style="padding: 8px; text-align: left;">{upi}</td>
                </tr>
                <tr style="border-bottom: 1px solid white;">
                    <td style="padding: 8px; text-align: left;"><b>Amount:</b></td>
                    <td style="padding: 8px; text-align: left;">₹{amount:,.2f}</td>
                </tr>
                <tr style="border-bottom: 1px solid white;">
                    <td style="padding: 8px; text-align: left;"><b>Time:</b></td>
                    <td style="padding: 8px; text-align: left;">{trans_time} (Hour: {hour})</td>
                </tr>
                <tr style="border-bottom: 1px solid white;">
                    <td style="padding: 8px; text-align: left;"><b>Category:</b></td>
                    <td style="padding: 8px; text-align: left;">{merchant_category}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; text-align: left;"><b>State:</b></td>
                    <td style="padding: 8px; text-align: left;">{state}</td>
                </tr>
            </table>
        </div>
        <br><center><a href='/' style="font-size: 18px; padding: 10px 20px; background: #333; color: white; text-decoration: none; border-radius: 5px;">Go Back</a></center>
        """
        
        return result_html
        
    except Exception as e:
        error_html = f"""
        <div style="background-color: orange; color: white; padding: 30px; border-radius: 10px; text-align: center; margin: 20px;">
            <h1>⚠️ ERROR IN PROCESSING</h1>
            <p>{str(e)}</p>
            <p>Please check your input and try again.</p>
        </div>
        <br><center><a href='/' style="font-size: 18px; padding: 10px 20px; background: #333; color: white; text-decoration: none; border-radius: 5px;">Go Back</a></center>
        """
        return error_html

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)