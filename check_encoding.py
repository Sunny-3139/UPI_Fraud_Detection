import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

# Load data
df = pd.read_csv('transactions.csv')

# Check merchant categories
print("Unique Merchant Categories:")
print(df['Merchant_Category'].unique())
print(f"Number of unique categories: {df['Merchant_Category'].nunique()}")

# Check states
print("\nUnique States:")
print(df['State'].unique())
print(f"Number of unique states: {df['State'].nunique()}")

# Encode using training method
le_merchant = LabelEncoder()
le_merchant.fit(df['Merchant_Category'])
print(f"\nMerchant Category Encoding:")
for i, cat in enumerate(le_merchant.classes_):
    print(f"  {i}: {cat}")

le_state = LabelEncoder()
le_state.fit(df['State'])
print(f"\nState Encoding:")
for i, state in enumerate(le_state.classes_):
    print(f"  {i}: {state}")

# Now check what app.py is using
merchant_categories = ['Shopping', 'Cash Out / Transfer', 'Food & Dining', 'Healthcare', 
                       'Travel', 'Entertainment', 'Groceries', 'Bills & Utilities', 
                       'Fuel', 'Education', 'Online Services', 'Insurance']

states = ['Maharashtra', 'Karnataka', 'Gujarat', 'Delhi', 'Punjab', 'Tamil Nadu', 'Kerala', 
          'Telangana', 'Bangalore', 'Mumbai', 'Pune', 'Hyderabad', 'Lucknow', 'Jaipur', 
          'Chandigarh', 'Ahmedabad', 'Surat', 'Indore', 'Bhopal', 'Vadodara', 'Gurgaon', 
          'Kolkata', 'Kanpur']

print(f"\nAPP.PY uses {len(merchant_categories)} categories")
print(f"Training data has {len(df['Merchant_Category'].unique())} categories")
print(f"\nMismatch? {set(df['Merchant_Category'].unique()) != set(merchant_categories)}")

print(f"\nAPP.PY uses {len(states)} states")
print(f"Training data has {len(df['State'].unique())} states")
