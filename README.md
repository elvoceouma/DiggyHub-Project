# Digital Receipt Generation and Delivery System

This project aims to implement a system for generating digital receipts to replace physical receipts issued by stores. The system allows users to generate receipts in PDF format and send them via WhatsApp and email.

## Features

- Generate PDF receipts with customizable templates.
- Send receipts to customers' WhatsApp numbers.
- Send receipts to customers' email addresses.

## Technologies Used

- Python: Programming language used for backend development.
- Flask: Lightweight web framework for building the application.
- HTML/CSS: Used for creating the receipt templates.
- Twilio API: Integrating WhatsApp messaging functionality.
- Flask-Mail: Library for sending emails from Flask applications.

## Installation

1. Clone the repository:

   git clone https://github.com/your-username/digital-receipt-system.git](https://github.com/elvoceouma/DiggyHub-Project.git

2. Install the project dependencies:

   ```shell
   pip install -r requirements.txt
   ```

3. Set up the necessary configuration:

   - Create a Twilio account and obtain the required credentials.
   - Configure the Flask-Mail settings with your SMTP server details.

4. Run the application:

   ```shell
   python app.py
   ```

   The application will be accessible at `http://localhost:5000`.

## Usage

1. Access the web application in your browser.

2. Fill in the necessary transaction details in the provided form.

3. Click on the "Generate Receipt" button.

4. Choose the delivery method: WhatsApp or Email.

5. Provide the recipient's WhatsApp number or email address.

6. Click on the "Send Receipt" button.

7. The receipt will be generated in PDF format and sent to the specified recipient.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Twilio](https://www.twilio.com/) for providing the WhatsApp messaging API.
- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [Flask-Mail](https://pythonhosted.org/Flask-Mail/) for email functionality.

Feel free to customize the README.md file according to your project's specific details and requirements.
