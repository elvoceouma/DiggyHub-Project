import mysql.connector
from flask import Flask, render_template, request, redirect, flash, jsonify
from database import connect_to_database, save_receipt, send_whatsapp_receipt, send_email_receipt, get_receipt
from datetime import datetime


app = Flask(__name__)
app.secret_key = "your-secret-key"  # Replace with your own secret key

# Home page route


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/save-receipt', methods=['POST'])
def save_receipt():
    # Handle receipt data
    data = request.get_json()
    # Save the receipt to the database
    # ...


@app.route('/send-whatsapp-receipt', methods=['POST'])
def send_whatsapp_receipt():
    # Handle receipt data
    data = request.get_json()


@app.route('/send-email-receipt', methods=['POST'])
def send_email_receipt():
    # Handle receipt data
    if __name__ == '__main__':
        data = request.get_json()


# Generate receipt route
@app.route('/generate_receipt', methods=['POST'])
def generate_receipt():
    transaction_data = {
        'customer_name': request.form['customer_name'],
        'purchase_date': request.form['purchase_date'],
        # Add more transaction data fields as required
    }

    # Save receipt details in the database
    receipt_id = save_receipt(transaction_data)

    # Redirect to choose delivery method
    return redirect(f'/send_receipt/{receipt_id}')

# Send receipt route


@app.route('/send_receipt/<receipt_id>', methods=['GET', 'POST'])
def send_receipt(receipt_id):
    if request.method == 'POST':
        # Retrieve receipt details from the database
        receipt = get_receipt(receipt_id)
        delivery_method = request.form['delivery_method']
        recipient = request.form['recipient']

        if delivery_method == 'whatsapp':
            # Send receipt via WhatsApp
            send_whatsapp_receipt(receipt, recipient)
            flash('Receipt sent via WhatsApp!')
        elif delivery_method == 'email':
            send_email_receipt(receipt, recipient)  # Send receipt via email
            flash('Receipt sent via email!')
        else:
            flash('Invalid delivery method.')

        return redirect('/')

    return render_template('send_receipt.html', receipt_id=receipt_id)


if __name__ == '__main__':
    app.run(debug=True)
