from flask import Flask, render_template, request, session, redirect, url_for
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key

# Simple user credentials (can be enhanced with database)
VALID_USERS = {
    'admin': 'admin123',
    'user': 'password123'
}

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
    
    # Capture all 9 fields from the interface
    upi = request.form.get('upi_number')
    holder_name = request.form.get('holder_name')
    state = request.form.get('state')
    trans_time = request.form.get('trans_time')
    seller_name = request.form.get('seller_name')
    dob = request.form.get('dob')
    pin_code = request.form.get('pin_code')
    amount = float(request.form.get('amount'))
    merchant_category = request.form.get('merchant_category')
    
    # Simple behavioral logic (to be replaced by CNN .h5 later)
    current_hour = datetime.datetime.now().hour
    if trans_time:
        try:
            current_hour = datetime.datetime.strptime(trans_time, '%Y-%m-%dT%H:%M').hour
        except:
            pass

    prediction = "Valid"
    color = "green"

    if amount > 40000 and current_hour < 6:
        prediction = "Fraud Detected (Reason: Unusual Hour/High Amount)"
        color = "red"
    elif amount > 75000:
        prediction = "Fraud Detected (Reason: Transaction Limit Exceeded)"
        color = "red"

    return f"<h1 style='color:{color}; text-align:center;'>Result: {prediction}</h1><br><center><a href='/'>Go Back</a></center>"

if __name__ == '__main__':
    app.run(debug=True)