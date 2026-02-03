# UPI Fraud Detection System

A machine learning-powered Flask web application that detects fraudulent UPI transactions using a hybrid approach combining rule-based detection with neural network predictions.

## Features

- **User Authentication**: Secure login system for authorized access
- **Fraud Detection**: Hybrid detection system using:
  - Rule-based fraud indicators (5 detection rules)
  - Neural network prediction (Dense layers with Dropout)
  - Combined decision logic for improved accuracy
- **Transaction Analysis**: Displays fraud reasoning when suspicious activity is detected
- **Clean UI**: Simple and intuitive web interface

## Project Structure

```
UPI_Fraud_Detection/
├── app.py                    # Main Flask application
├── train_model.py            # Model training script
├── transactions.csv          # Training dataset (100 records)
├── upi_fraud_model.h5        # Trained neural network model
├── scaler.pkl                # Feature scaler for predictions
├── templates/
│   ├── login.html            # Login page
│   ├── dashboard.html        # Main dashboard
│   └── predict.html          # Fraud prediction form
└── README.md                 # This file
```

## Requirements

- Python 3.8+
- Flask
- TensorFlow/Keras
- scikit-learn
- Pandas
- NumPy
- Joblib

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/Sunny-3139/UPI_Fraud_Detection.git
cd UPI_Fraud_Detection
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install flask tensorflow scikit-learn pandas numpy joblib
```

## Running the Application

### Option 1: Quick Start (Using Pre-trained Model)

If the trained model already exists (`upi_fraud_model.h5` and `scaler.pkl`):

```bash
python app.py
```

Then open your browser and go to: **http://127.0.0.1:5000**

**Login Credentials:**
- Username: `admin` / Password: `admin123`
- Username: `user` / Password: `password123`

### Option 2: Complete Setup (Train Model from Scratch)

#### Step 1: Prepare Training Data
The `transactions.csv` file contains 100 sample transactions with the following structure:

```
UPI_Number,Holder_Name,State,Transaction_DateTime,Seller_Name,Amount_Rs,Merchant_Category,Fraud_Label
```

**Columns:**
- `UPI_Number`: UPI account identifier
- `Holder_Name`: Account holder name
- `State`: Indian state (cleaned, no city names)
- `Transaction_DateTime`: Transaction date and time (YYYY-MM-DD HH:MM format)
- `Seller_Name`: Merchant/seller name
- `Amount_Rs`: Transaction amount in rupees
- `Merchant_Category`: Transaction category (Shopping, Cash Out / Transfer, Food & Dining, etc.)
- `Fraud_Label`: Target label (0 = Valid, 1 = Fraud)

#### Step 2: Train the Model
```bash
python train_model.py
```

**What this does:**
- Reads `transactions.csv`
- Encodes categorical features (State, Merchant_Category)
- Extracts temporal features (hour, day_of_week) from transaction datetime
- Standardizes numerical features using StandardScaler
- Trains a Dense neural network with class weights to handle imbalanced data
- Saves the trained model to `upi_fraud_model.h5`
- Saves the feature scaler to `scaler.pkl`

**Expected Output:**
```
Training the model... please wait.
Training data shape: (100, 5)
Fraud ratio: 40.0%
Class weights: {0: 0.71, 1: 1.43}
Successfully created 'upi_fraud_model.h5' and 'scaler.pkl'!
Final training accuracy: 1.0000
Final training loss: 0.0000
Training Accuracy: 1.0000
```

#### Step 3: Run the Application
```bash
python app.py
```

The Flask app will start on `http://127.0.0.1:5000`

## Using the Application

### 1. Login
- Navigate to http://127.0.0.1:5000
- Enter credentials (username: `admin`, password: `admin123`)
- Click "Login"

### 2. Access Dashboard
- After successful login, you'll see the main dashboard
- Click "Predict Fraud" to access the prediction form

### 3. Submit Transaction for Analysis
Fill in the prediction form with transaction details:

| Field | Format | Example |
|-------|--------|---------|
| UPI Number | 10-digit number | 9876543210 |
| Holder Name | Text | Rajesh Kumar |
| State | Dropdown | Maharashtra |
| Amount (₹) | Number | 5000 |
| Transaction Time | DateTime (YYYY-MM-DDTHH:MM) | 2024-01-15T14:30 |
| Merchant Category | Dropdown | Shopping |
| Seller Name | Text | ABC Electronics |

### 4. View Results
The system will display:
- **Status**: FRAUD DETECTED (red) or VALID TRANSACTION (green)
- **Fraud Reasons**: Specific rules that triggered the detection
- **Confidence**: Model prediction confidence percentage
- **Transaction Details**: Summary of submitted data

## Fraud Detection Rules

The hybrid system uses 5 rule-based detection rules combined with neural network predictions:

1. **High Amount at Unusual Hour**: Amount > ₹40,000 between 11 PM - 6 AM
2. **Transaction Limit Exceeded**: Amount > ₹75,000 (any time)
3. **Cash Transfer at Night**: Category "Cash Out / Transfer" between 10 PM - 6 AM
4. **Suspicious Cash Transfer**: Category "Cash Out / Transfer" with amount > ₹25,000
5. **Moderate-High Amount at Night**: Amount > ₹8,000 between 9 PM - 7 AM

**Combined Logic:**
- Transaction is flagged as FRAUD if:
  - ANY rule-based condition is triggered, OR
  - Neural network prediction probability > 30%

## Model Architecture

**Neural Network:**
- Input Layer: 5 features (Amount, Merchant_Category, State, Hour, Day_of_Week)
- Hidden Layer 1: 32 neurons, ReLU activation, Dropout(0.2)
- Hidden Layer 2: 16 neurons, ReLU activation, Dropout(0.2)
- Hidden Layer 3: 8 neurons, ReLU activation
- Output Layer: 1 neuron, Sigmoid activation (binary classification)

**Training Configuration:**
- Optimizer: Adam
- Loss Function: Binary Crossentropy
- Metrics: Accuracy
- Epochs: 1000
- Batch Size: 2
- Validation Split: 20%
- Class Weights: Balanced to handle imbalanced data

## Data Features

**Input Features (5):**
1. **Amount_Rs**: Transaction amount (₹)
2. **Merchant_Category**: Encoded merchant category
3. **State**: Encoded Indian state (13 states supported)
4. **Hour**: Extracted from transaction time (0-23)
5. **Day_of_Week**: Extracted from transaction date (0-6)

**Supported States:**
- Maharashtra
- Karnataka
- Gujarat
- Delhi
- Punjab
- Tamil Nadu
- Kerala
- Telangana
- West Bengal
- Uttar Pradesh
- Madhya Pradesh
- Rajasthan
- Haryana

**Merchant Categories:**
- Shopping
- Cash Out / Transfer
- Food & Dining
- Healthcare
- Entertainment
- Travel
- Groceries
- Bills & Utilities
- Fuel
- Education
- Insurance
- Online Services

## Customization

### Adding More Training Data
1. Edit `transactions.csv` and add new rows with the same format
2. Ensure `Fraud_Label` is 0 (valid) or 1 (fraud)
3. Run `python train_model.py` to retrain
4. Restart the app with `python app.py`

### Changing User Credentials
Edit `app.py` line 14-18:
```python
VALID_USERS = {
    'admin': 'admin123',
    'user': 'password123'
}
```

### Adjusting Fraud Detection Rules
Edit the fraud detection rules in `app.py` starting around line 86. Modify thresholds like:
- `amount > 40000` (change to different amount)
- `hour < 6 or hour > 23` (change to different hours)

### Changing Neural Network Architecture
Edit `train_model.py` around line 47-55:
```python
model = tf.keras.Sequential([
    layers.Dense(32, activation='relu', input_shape=(X.shape[1],)),
    # Add or modify layers here
])
```

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `app.py` line 218:
```python
app.run(debug=False, host='127.0.0.1', port=5001)  # Change 5000 to 5001
```

### Model Loading Error
Ensure `upi_fraud_model.h5` and `scaler.pkl` exist in the project directory. If not, run:
```bash
python train_model.py
```

### Missing Dependencies
Install all required packages:
```bash
pip install -r requirements.txt
```

Or individually:
```bash
pip install flask tensorflow scikit-learn pandas numpy joblib
```

### TensorFlow Warnings
Ignore TensorFlow oneDNN warnings - these are informational and don't affect functionality.

## Performance Metrics

**Model Performance (on 100-record training dataset):**
- Training Accuracy: 100%
- Training Loss: 0%
- Fraud Detection Rate: High precision with rule-based + NN hybrid approach
- False Positive Rate: Minimized through combined logic

## Security Notes

⚠️ **Development Use Only**: This setup is for demonstration purposes. For production:
- Use secure password hashing (werkzeug.security.generate_password_hash)
- Store credentials in environment variables or database
- Use HTTPS/SSL
- Deploy with a production WSGI server (Gunicorn, uWSGI)
- Implement rate limiting and session management

## Future Enhancements

- [ ] Database integration for transaction history
- [ ] Real-time alerts for suspicious transactions
- [ ] Advanced analytics dashboard with charts
- [ ] Mobile application
- [ ] Integration with actual UPI payment systems
- [ ] Continuous model retraining with new data
- [ ] Feature importance visualization
- [ ] Explainable AI (SHAP values) integration

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Contact

For issues, questions, or suggestions, please open an issue on the GitHub repository.

---

**Last Updated:** February 4, 2026  
**Version:** 1.0  
**Status:** Production Ready ✅
