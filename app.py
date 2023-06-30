import mysql.connector
from flask import Flask, Response, render_template, request, redirect, flash, jsonify, send_file
from datetime import datetime
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO
import base64
import pdfkit
import os
from twilio.rest import Client
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from dotenv import load_dotenv

app = Flask(__name__)


load_dotenv()
app.secret_key = os.environ.get('APP_SECRET_KEY')
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')


options = {"enable-local-file-access": ""}
receipt_number = 20636
BASE_DIR = os.getcwd()
RECEIPT_DIR = os.path.join(BASE_DIR, 'stored_receipts')


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
    global output_path

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

    output_path = os.path.join(RECEIPT_DIR, f'{barcode_value}.pdf')

    if convert_to_pdf(html_content, output_path):
        # Call the send_email_receipt function
        send_whatsapp_receipt(transaction_data, output_path,
                              barcode_value)
        # Redirect to the PDF receipt route
        return redirect(f'/pdf_receipt?barcode_value={barcode_value}')
    else:
        return "Failed to generate PDF receipt."


def generate_barcode_image(barcode_value):
    code128 = Code128(barcode_value, writer=ImageWriter())
    stream = BytesIO()
    code128.write(stream)
    stream.seek(0)
    return stream.getvalue()


def convert_to_pdf(html_content, output_path):
    try:

        pdfkit.from_string(html_content, output_path, options=options)
        return True
    except Exception as e:
        print(f"PDF Conversion failed: {str(e)}")
        return False


@app.route('/pdf_receipt')
def pdf_receipt():
    barcode_value = request.args.get('barcode_value')
    pdf_path = os.path.join(RECEIPT_DIR, f'{barcode_value}.pdf')
    return send_file(pdf_path, mimetype='application/pdf')

# Route for sending the receipt via WhatsApp


@app.route('/send-whatsapp-receipt', methods=['POST'])
def send_whatsapp_receipt(transaction_data, pdf_path, recipient_phone,):
    # barcode_value = request.args.get('barcode_value')
    # pdf_path = os.path.join(RECEIPT_DIR, f'{barcode_value}.pdf')
    recipient_phone = request.form['phone_number']
    transaction_date = datetime.now().strftime("%Y-%m-%dT%H:%M")
    customer_name = transaction_data['customer_name']
    account_sid = twilio_account_sid
    auth_token = twilio_auth_token
    client = Client(account_sid, auth_token)
    from_whatsapp_number = 'whatsapp:+14155238886',  # Twilio sandbox WhatsApp number
    # Recipient's WhatsApp number
    to_whatsapp_number = f'whatsapp:{recipient_phone}'
    message_body = f"Dear {customer_name},\n\nThank you for your recent purchase! We're delighted to share your receipt with you. Please find it attached.\n\nIf you have any questions or need further assistance, feel free to reach out to our customer support team.\n\nBest regards,\nDiggyHub Company \n\n{transaction_data}"
    message = client.messages.create(
        from_=from_whatsapp_number,
        body=message_body,
        media_url=[
            'https://sitemate.com/wp-content/uploads/2019/04/2019-04-01-Example-Template-Project-Field-Service-Report-1-page-001.jpg'],
        to=to_whatsapp_number
    )

    if message.sid:
        return True
    else:
        return False


@app.route('/send-email-receipt', methods=['POST'])
def send_email_receipt(transaction_data, pdf_path):
    # Handle receipt data and recipient information
    email_subject = "Receipt"
    email_body = "Please find attached the receipt."
    sender_email = transaction_data['business_address']
    recipient_email = transaction_data['email_address']

    # Rest of the function code...

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = email_subject
    message['Body'] = email_body

    # Attach the PDF receipt
    with open(pdf_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment',
                        filename='receipt.pdf')
        message.attach(part)

    # Connect to the SMTP server and send the email
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    smtp_username = "elviceoumaonyango@gmail.com"
    smtp_password = "@Elvice.Dev"

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)

    return "Receipt sent via email."
# def send_whatsapp_receipt():
#
#    # Use the send_whatsapp_receipt function to send the receipt via WhatsApp
#    if send_whatsapp_receipt(pdf_path, recipient_phone):
#        flash('Receipt sent via WhatsApp!')
#    else:
#        flash('Failed to send receipt via WhatsApp.')
#
#    return redirect('/')


@app.route('/save-receipt', methods=['POST'])
def save_receipt():
    # Handle receipt data
    data = request.get_json()
    # Save the receipt to the database
    # ...


# @app.route('/send-whatsapp-receipt', methods=['POST'])
# def send_whatsapp_receipt():
#    # Handle receipt data
#    data = request.get_json()


# @app.route('/send-email-receipt', methods=['POST'])
# def send_email_receipt():
#    # Handle receipt data
#    if __name__ == '__main__':
#        data = request.get_json()


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
