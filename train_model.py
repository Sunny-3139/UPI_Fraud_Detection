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

# Drop original date columns
df = df.drop(['Transaction_DateTime'], axis=1)

# 3. Separate Features (X) and Target (y)
X = df.drop('Fraud_Label', axis=1).values
y = df['Fraud_Label'].values

print(f"Features shape before scaling: {X.shape}")
print(f"Feature columns: {df.drop('Fraud_Label', axis=1).columns.tolist()}")
print(f"Target distribution: {np.bincount(y.astype(int))}")

# 3. Standardize the data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Save the scaler to use it later in app.py
joblib.dump(scaler, 'scaler.pkl')

# 4. DO NOT reshape - use as is for Dense layers
# X stays as (Samples, Features)

# 5. Build a simple but effective model for small dataset
model = tf.keras.Sequential([
    layers.Dense(32, activation='relu', input_shape=(X.shape[1],)),
    layers.Dropout(0.2),
    layers.Dense(16, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(8, activation='relu'),
    layers.Dense(1, activation='sigmoid') 
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 6. Train the model with more epochs and class weights to handle imbalance
print("\nTraining the model... please wait.")
print(f"Training data shape: {X.shape}")
print(f"Fraud ratio: {(y.sum() / len(y) * 100):.1f}%")

# Calculate class weights to handle imbalance
from sklearn.utils.class_weight import compute_class_weight
class_weights = compute_class_weight('balanced', classes=np.unique(y), y=y)
class_weight_dict = dict(enumerate(class_weights))
print(f"Class weights: {class_weight_dict}")

history = model.fit(X, y, epochs=1000, verbose=1, batch_size=2, 
                   class_weight=class_weight_dict,
                   validation_split=0.2)

# 7. SAVE THE MODEL FILE
model.save('upi_fraud_model.h5')
print("\nSuccessfully created 'upi_fraud_model.h5' and 'scaler.pkl'!")
print(f"Final training accuracy: {history.history['accuracy'][-1]:.4f}")
print(f"Final training loss: {history.history['loss'][-1]:.4f}")

# Evaluate on training data
train_loss, train_acc = model.evaluate(X, y, verbose=0)
print(f"Training Accuracy: {train_acc:.4f}")