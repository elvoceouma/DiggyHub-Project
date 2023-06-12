import mysql.connector
from flask import Flask, Response, render_template, request, redirect, flash, jsonify, render_template_string
from database import connect_to_database, save_receipt, send_whatsapp_receipt, send_email_receipt, get_receipt
from datetime import datetime
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO
import base64


app = Flask(__name__)
app.secret_key = "your-secret-key"  # Replace with your own secret key

receipt_number = 0

# Defining a custom filter for base64 encoding


@app.template_filter('b64encode')
def base64_encode(value):
    encoded_bytes = base64.b64encode(value)
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate_receipt', methods=['POST'])
def generate_receipt():
    global receipt_number

    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

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
        'purchase_date': current_date,
        'purchase_time': current_time,
        'employee_number': request.form['employee_number'],
        'receipt_number': receipt_number,
    }

    barcode_value = f"RECEIPT-{current_date}-{receipt_number}"
    receipt_number += 1

    barcode_image = generate_barcode_image(barcode_value)

    return render_template('receipt_template.html', **transaction_data, current_date=current_date, current_time=current_time, barcode_image=barcode_image)


def generate_barcode_image(barcode_value):
    code128 = Code128(barcode_value, writer=ImageWriter())
    stream = BytesIO()
    code128.write(stream)
    stream.seek(0)
    return stream.getvalue()


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
