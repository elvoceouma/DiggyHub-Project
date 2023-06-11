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
        'business_name': request.form['business_name'],
        'business_address': request.form['business_address'],
        'phone_number': request.form['phone_number'],
        'email_address': request.form['email_address'],
        'product_description': request.form['product_description'],
        'sku': request.form['sku'],
        'quantity': request.form['quantity'],
        'amount_due': request.form['amount_due'],
        'payment_method': request.form['payment_method'],
        'purchase_date': request.form['purchase_date'],
        'purchase_time': request.form['purchase_time'],
        'employee_number': request.form['employee_number'],
        'receipt_number': request.form['receipt_number']
    }

    # Generate the receipt using the transaction_data

    # Replace the following print statements with your code to generate the receipt
    print('Customer Name:', transaction_data['customer_name'])
    print('Business Name:', transaction_data['business_name'])
    print('Business Address:', transaction_data['business_address'])
    print('Phone Number:', transaction_data['phone_number'])
    print('Email Address:', transaction_data['email_address'])
    print('Product Description:', transaction_data['product_description'])
    print('SKU:', transaction_data['sku'])
    print('Quantity:', transaction_data['quantity'])
    print('Amount Due:', transaction_data['amount_due'])
    print('Payment Method:', transaction_data['payment_method'])
    print('Purchase Date:', transaction_data['purchase_date'])
    print('Purchase Time:', transaction_data['purchase_time'])
    print('Employee Number:', transaction_data['employee_number'])
    print('Receipt Number:', transaction_data['receipt_number'])

    return render_template('receipt_template.html', **transaction_data)


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
