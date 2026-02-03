import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
from datetime import datetime

# 1. Load the data from the CSV you just created
df = pd.read_csv('transactions.csv')

# 2. Preprocess the data
# Drop unnecessary columns
df = df.drop(['UPI_Number', 'Holder_Name', 'Seller_Name'], axis=1)

# Encode categorical columns
le_state = LabelEncoder()
df['State'] = le_state.fit_transform(df['State'])

le_merchant = LabelEncoder()
df['Merchant_Category'] = le_merchant.fit_transform(df['Merchant_Category'])

# Parse dates
df['Transaction_DateTime'] = pd.to_datetime(df['Transaction_DateTime'])
df['hour'] = df['Transaction_DateTime'].dt.hour
df['day_of_week'] = df['Transaction_DateTime'].dt.dayofweek

df['Date_of_Birth'] = pd.to_datetime(df['Date_of_Birth'])
current_year = datetime.now().year
df['age'] = current_year - df['Date_of_Birth'].dt.year

# Drop original date columns
df = df.drop(['Transaction_DateTime', 'Date_of_Birth'], axis=1)

# 3. Separate Features (X) and Target (y)
X = df.drop('Fraud_Label', axis=1).values
y = df['Fraud_Label'].values

# 3. Standardize the data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Save the scaler to use it later in app.py
joblib.dump(scaler, 'scaler.pkl')

# 4. Reshape for CNN (Samples, Features, 1)
X = X.reshape(X.shape[0], X.shape[1], 1)

# 5. Build the CNN Model
model = tf.keras.Sequential([
    layers.Conv1D(32, 2, activation='relu', input_shape=(X.shape[1], 1)),
    layers.Flatten(),
    layers.Dense(16, activation='relu'),
    layers.Dense(1, activation='sigmoid') 
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 6. Train the model
print("Training the CNN model... please wait.")
model.fit(X, y, epochs=50, verbose=0)

# 7. SAVE THE MODEL FILE
model.save('upi_fraud_model.h5')
print("Successfully created 'upi_fraud_model.h5' and 'scaler.pkl'!")