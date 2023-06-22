import mysql.connector
from flask import Flask, Response, render_template, request, redirect, flash, jsonify, render_template_string
from database import connect_to_database, save_receipt, send_whatsapp_receipt, send_email_receipt, get_receipt
from datetime import datetime
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import time
import pdfkit


app = Flask(__name__)
app.secret_key = "your-secret-key"  # Replace  secret key later

receipt_number = 20636

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
    html_content = render_template('receipt_template.html', **transaction_data,
                                   current_date=current_date, current_time=current_time, barcode_image=barcode_image)
    output_path = '/path/to/output/receipt.pdf'
    if convert_to_pdf(html_content, output_path):
        # Redirect to the PDF receipt route
        return redirect('http://127.0.0.1:5000/generate_receipt'('pdf_receipt'))
    else:
        return "Failed to generate PDF receipt."


def generate_barcode_image(barcode_value):
    code128 = Code128(barcode_value, writer=ImageWriter())
    stream = BytesIO()
    code128.write(stream)
    stream.seek(0)
    return stream.getvalue()


# Create a PDF file from the HTML content


def convert_to_pdf(html_content, output_path):
    try:
        pdfkit.from_string(html_content, output_path)
        return True
    except Exception as e:
        print(f"PDF Conversion failed: {str(e)}")
        return False


@app.route('/pdf_receipt')
def pdf_receipt():
    pdf_path = '/home/elvice/DiggyHub-Project/stored_receipts'
    return send_file(pdf_path, mimetype='application/pdf')


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
    start_time = time.time()
    app.run(debug=True)
    end_time = time.time()
    runtime = end_time - start_time
    print(f"Runtime: {runtime} seconds")
