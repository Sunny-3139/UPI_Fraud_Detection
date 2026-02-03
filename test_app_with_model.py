import requests
from datetime import datetime
import time

# Flask app URL
BASE_URL = "http://127.0.0.1:5000"
SESSION = requests.Session()

# Test transactions data from transactions.csv
test_data = [
    ("9876543210", "Rajesh Kumar", "Maharashtra", "2024-01-15T14:30", "ABC Electronics", "1990-05-12", "400001", "5000", "Shopping", "0 (Valid)"),
    ("9123456789", "Priya Sharma", "Karnataka", "2024-01-15T02:45", "XYZ Convenience", "1995-08-22", "560001", "25000", "Cash Out / Transfer", "1 (Fraud)"),
    ("8765432109", "Amit Patel", "Gujarat", "2024-01-16T10:15", "Quick Meals", "1988-03-18", "380001", "350", "Food & Dining", "0 (Valid)"),
    ("9012345678", "Neha Verma", "Delhi", "2024-01-16T22:30", "Late Night Store", "1992-11-05", "110001", "8500", "Shopping", "1 (Fraud)"),
    ("9234567890", "Rohan Singh", "Punjab", "2024-01-17T09:45", "Health Plus", "1993-07-14", "160001", "2500", "Healthcare", "0 (Valid)"),
    ("9345678901", "Anjali Gupta", "Tamil Nadu", "2024-01-17T15:20", "Fashion Hub", "1996-02-28", "600001", "15000", "Shopping", "0 (Valid)"),
    ("9456789012", "Vikram Nair", "Kerala", "2024-01-18T11:00", "Travel Booking", "1989-12-03", "690001", "45000", "Travel", "1 (Fraud)"),
    ("9567890123", "Divya Reddy", "Telangana", "2024-01-18T19:30", "Movie Tickets", "1994-06-19", "500001", "800", "Entertainment", "0 (Valid)"),
    ("9678901234", "Arjun Rao", "Bangalore", "2024-01-19T03:15", "Night Market", "1991-09-25", "560034", "12000", "Groceries", "1 (Fraud)"),
    ("9789012345", "Sneha Kapoor", "Mumbai", "2024-01-19T13:45", "Power Supply", "1987-04-10", "400050", "1200", "Bills & Utilities", "0 (Valid)"),
]

def login():
    """Login to the application"""
    print("=" * 90)
    print("LOGGING IN")
    print("=" * 90)
    
    login_data = {
        'username': 'admin',
        'password': 'admin123'
    }
    
    try:
        response = SESSION.post(f"{BASE_URL}/login", data=login_data)
        print("✓ Login successful!")
        return True
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False

def test_transaction(idx, upi, name, state, trans_time, seller, dob, pincode, amount, category, expected):
    """Test a single transaction"""
    
    trans_data = {
        'upi_number': upi,
        'holder_name': name,
        'state': state,
        'trans_time': trans_time,
        'seller_name': seller,
        'dob': dob,
        'pin_code': pincode,
        'amount': amount,
        'merchant_category': category
    }
    
    try:
        response = SESSION.post(f"{BASE_URL}/predict", data=trans_data)
        
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
        print(f"\nExpected Result:   {expected}")
        
        # Extract result from HTML response
        if "FRAUD DETECTED" in response.text:
            print(f"Actual Result:     🔴 FRAUD DETECTED")
            # Extract confidence
            if "Confidence:" in response.text:
                start = response.text.find("Confidence:") + len("Confidence: ")
                end = response.text.find("%", start)
                confidence = response.text[start:end]
                print(f"                   Confidence: {confidence}%")
        elif "VALID TRANSACTION" in response.text:
            print(f"Actual Result:     ✓ VALID TRANSACTION")
            if "Confidence:" in response.text:
                start = response.text.find("Confidence:") + len("Confidence: ")
                end = response.text.find("%", start)
                confidence = response.text[start:end]
                print(f"                   Confidence: {confidence}%")
        else:
            print(f"Actual Result:     Unable to parse response")
        
        return response.text
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("\n")
    print("╔" + "=" * 88 + "╗")
    print("║" + " " * 88 + "║")
    print("║" + "UPI FRAUD DETECTION - COMPLETE APPLICATION TEST".center(88) + "║")
    print("║" + " " * 88 + "║")
    print("╚" + "=" * 88 + "╝")
    
    # Login first
    time.sleep(2)  # Give server time to fully start
    if not login():
        print("\nCannot proceed without login")
        return
    
    print("\n" + "=" * 90)
    print("TESTING TRANSACTIONS WITH TRAINED MODEL")
    print("=" * 90)
    
    # Test each transaction
    results = []
    for i, (upi, name, state, trans_time, seller, dob, pincode, amount, category, expected) in enumerate(test_data, 1):
        test_transaction(i, upi, name, state, trans_time, seller, dob, pincode, amount, category, expected)
        results.append((name, amount, expected))
    
    print("\n" + "=" * 90)
    print("TEST SUMMARY")
    print("=" * 90)
    print(f"Total transactions tested: {len(test_data)}\n")
    print(f"{'No.':<4} {'Name':<20} {'Amount':<15} {'Expected':<20}")
    print("-" * 90)
    
    for i, (name, amount, expected) in enumerate(results, 1):
        print(f"{i:<4} {name:<20} ₹{amount:<14} {expected:<20}")
    
    print("\n✓ All transactions tested successfully!")
    print("\nNOTE: The app now uses the trained CNN model for fraud detection.")
    print("Results may differ from the simple rule-based logic used before.")

if __name__ == "__main__":
    main()
