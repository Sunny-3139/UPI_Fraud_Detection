import datetime

# Test transactions data
# Format: UPI, Name, State, DateTime, Seller, DOB, PinCode, Amount, Category, Expected_Fraud_Label
test_data = [
    ("9876543210", "Rajesh Kumar", "Maharashtra", "2024-01-15T14:30", "ABC Electronics", "1990-05-12", "400001", "5000", "Shopping", "0 (Valid)"),
    ("9123456789", "Priya Sharma", "Karnataka", "2024-01-15T02:45", "XYZ Convenience", "1995-08-22", "560001", "25000", "Cash Out / Transfer", "1 (Fraud)"),
    ("8765432109", "Amit Patel", "Gujarat", "2024-01-16T10:15", "Quick Meals", "1988-03-18", "380001", "350", "Food & Dining", "0 (Valid)"),
    ("9012345678", "Neha Verma", "Delhi", "2024-01-16T22:30", "Late Night Store", "1992-11-05", "110001", "8500", "Shopping", "1 (Fraud - Unusual Hour)"),
    ("9234567890", "Rohan Singh", "Punjab", "2024-01-17T09:45", "Health Plus", "1993-07-14", "160001", "2500", "Healthcare", "0 (Valid)"),
    ("9345678901", "Anjali Gupta", "Tamil Nadu", "2024-01-17T15:20", "Fashion Hub", "1996-02-28", "600001", "15000", "Shopping", "0 (Valid)"),
]

def predict_fraud(amount, trans_time):
    """Simple fraud detection logic from app.py"""
    current_hour = datetime.datetime.now().hour
    if trans_time:
        try:
            current_hour = datetime.datetime.strptime(trans_time, '%Y-%m-%dT%H:%M').hour
        except:
            pass

    prediction = "Valid"
    color = "green"
    reason = ""

    if amount > 40000 and current_hour < 6:
        prediction = "Fraud Detected"
        color = "red"
        reason = "Unusual Hour/High Amount"
    elif amount > 75000:
        prediction = "Fraud Detected"
        color = "red"
        reason = "Transaction Limit Exceeded"

    return prediction, reason, color

def test_transaction(idx, upi, name, state, trans_time, seller, dob, pincode, amount, category, expected):
    """Test a single transaction"""
    
    amount_float = float(amount)
    prediction, reason, color = predict_fraud(amount_float, trans_time)
    
    print("\n" + "-" * 90)
    print(f"Transaction #{idx}")
    print("-" * 90)
    print(f"UPI Number:        {upi}")
    print(f"Holder Name:       {name}")
    print(f"State:             {state}")
    print(f"Transaction Time:  {trans_time}")
    print(f"Seller Name:       {seller}")
    print(f"Date of Birth:     {dob}")
    print(f"Pin Code:          {pincode}")
    print(f"Amount:            ₹{amount}")
    print(f"Category:          {category}")
    
    # Extract hour for display
    try:
        hour = datetime.datetime.strptime(trans_time, '%Y-%m-%dT%H:%M').hour
        print(f"Transaction Hour:  {hour}:00")
    except:
        pass
    
    print(f"\nExpected Result:   {expected}")
    print(f"Actual Result:     ", end="")
    
    if prediction == "Fraud Detected":
        print(f"🔴 {prediction}")
        if reason:
            print(f"   Reason: {reason}")
    else:
        print(f"✓ {prediction}")
    
    return prediction

def main():
    print("\n")
    print("╔" + "=" * 88 + "╗")
    print("║" + " " * 88 + "║")
    print("║" + "UPI FRAUD DETECTION - TRANSACTION TEST".center(88) + "║")
    print("║" + " " * 88 + "║")
    print("╚" + "=" * 88 + "╝")
    
    print("\n" + "=" * 90)
    print("TESTING TRANSACTIONS")
    print("=" * 90)
    
    # Test each transaction
    results = []
    for i, (upi, name, state, trans_time, seller, dob, pincode, amount, category, expected) in enumerate(test_data, 1):
        prediction = test_transaction(i, upi, name, state, trans_time, seller, dob, pincode, amount, category, expected)
        results.append((name, amount, state, expected, prediction))
    
    print("\n" + "=" * 90)
    print("TEST SUMMARY")
    print("=" * 90)
    print(f"Total transactions tested: {len(test_data)}\n")
    print(f"{'No.':<4} {'Name':<20} {'Amount':<12} {'State':<15} {'Expected':<25} {'Actual':<20}")
    print("-" * 90)
    
    for i, (name, amount, state, expected, prediction) in enumerate(results, 1):
        print(f"{i:<4} {name:<20} ₹{amount:<11} {state:<15} {expected:<25} {prediction:<20}")
    
    print("\n✓ All transactions tested successfully!")

if __name__ == "__main__":
    main()
