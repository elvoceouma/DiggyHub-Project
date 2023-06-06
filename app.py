
from flask import Flask, render_template, request, redirect, flash
from database import connect_to_database, save_receipt, send_whatsapp_receipt, send_email_receipt

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Replace with your own secret key

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Generate receipt route
@app.route('/generate_receipt', methods=['POST'])
def generate_receipt():
    transaction_data = {
        'customer_name': request.form['customer_name'],
        'purchase_date': request.form['purchase_date'],
        # Add more transaction data fields as required
    }

    receipt_id = save_receipt(transaction_data)  # Save receipt details in the database

    return redirect(f'/send_receipt/{receipt_id}')  # Redirect to choose delivery method

# Send receipt route
@app.route('/send_receipt/<receipt_id>', methods=['GET', 'POST'])
def send_receipt(receipt_id):
    if request.method == 'POST':
        receipt = get_receipt(receipt_id)  # Retrieve receipt details from the database
        delivery_method = request.form['delivery_method']
        recipient = request.form['recipient']

        if delivery_method == 'whatsapp':
            send_whatsapp_receipt(receipt, recipient)  # Send receipt via WhatsApp
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
