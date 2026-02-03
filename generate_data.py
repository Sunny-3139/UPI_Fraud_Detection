import pandas as pd
import random

# Configuration
NUM_RECORDS = 1000
FILENAME = "transactions.csv"

data = []

for i in range(NUM_RECORDS):
    # 1. Decide if this row is Fraud (let's make 15% of data fraud)
    is_fraud = 1 if random.random() < 0.15 else 0
    
    if is_fraud:
        # FRAUD PATTERN: High Amount (20k to 1 Lakh), Night Time, Category 4
        amount = round(random.uniform(20000, 100000), 2)
        category = 4  # Cash Out
        hour = random.choice([0, 1, 2, 3, 4, 23]) # Late night/Early morning
    else:
        # VALID PATTERN: Low/Medium Amount (1 to 20k), Day Time, Mixed Categories
        amount = round(random.uniform(1, 20000), 2)
        category = random.randint(1, 3) # Ent, Food, Shopping
        hour = random.randint(8, 22)   # Working hours
        
    day_of_week = random.randint(1, 7)
    
    data.append([amount, category, hour, day_of_week, is_fraud])

# Save to CSV
df = pd.DataFrame(data, columns=['amount', 'category', 'hour', 'day_of_week', 'is_fraud'])
df.to_csv(FILENAME, index=False)

print(f"✅ Success! Generated {NUM_RECORDS} transactions in {FILENAME}")
print(df.head())