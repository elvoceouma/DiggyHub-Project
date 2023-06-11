// Form submission event handler
document.querySelector("form").addEventListener("submit", function (event) {
  // Perform form validation (example using HTML5 constraint validation)
  if (this.checkValidity()) {
    // Retrieve form data
    const customerName = document.getElementById("customer_name").value;
    const businessName = document.getElementById("business_name").value;
    const businessAddress = document.getElementById("business_address").value;
    const phoneNumber = document.getElementById("phone_number").value;
    const emailAddress = document.getElementById("email_address").value;
    const productDescription = document.getElementById(
      "product_description"
    ).value;
    const sku = document.getElementById("sku").value;
    const quantity = document.getElementById("quantity").value;
    const amountDue = document.getElementById("amount_due").value;
    const paymentMethod = document.getElementById("payment_method").value;
    const purchaseDate = document.getElementById("purchase_date").value;
    const purchaseTime = document.getElementById("purchase_time").value;
    const employeeNumber = document.getElementById("employee_number").value;
    const receiptNumber = document.getElementById("receipt_number").value;

    // Create an object with the form data
    const formData = {
      customer_name: customerName,
      business_name: businessName,
      business_address: businessAddress,
      phone_number: phoneNumber,
      email_address: emailAddress,
      product_description: productDescription,
      sku,
      quantity,
      amount_due: amountDue,
      payment_method: paymentMethod,
      purchase_date: purchaseDate,
      purchase_time: purchaseTime,
      employee_number: employeeNumber,
      receipt_number: receiptNumber,
    };

    // Make an Ajax request to send the receipt data to the server
    // Replace the URL with your server endpoint
    fetch("/generate_receipt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle the response from the server
        if (data.success) {
          showMessage("Receipt generated successfully!", "success");
        } else {
          showMessage("Failed to generate receipt. Please try again.", "error");
        }
      })
      .catch((error) => {
        showMessage("An error occurred. Please try again later.", "error");
      });
  } else {
    // Display validation error messages (example using HTML5 constraint validation)
    this.reportValidity();
  }
});

// Show message helper function
function showMessage(message, type) {
  const messagesContainer = document.getElementById("messages");

  if (messagesContainer) {
    const messageElement = document.createElement("li");
    messageElement.textContent = message;
    messageElement.classList.add(type);
    messagesContainer.appendChild(messageElement);
  } else {
    // Handle absence of messages container gracefully
    console.log(
      "No messages container found. Displaying message in an alternative way:",
      message
    );
  }
}
