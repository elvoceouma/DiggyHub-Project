// Form submission event handler
document.querySelector("form").addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent form submission

  // Perform form validation (example using HTML5 constraint validation)
  if (this.checkValidity()) {
    // Retrieve form data
    var recipientType = document.getElementById("recipient_type").value;
    var recipient = document.getElementById("recipient").value;
    var receiptType = document.getElementById("receipt_type").value;

    // Create an object with the form data
    var formData = {
      recipientType: recipientType,
      recipient: recipient,
      receiptType: receiptType,
    };

    // Make an Ajax request to send the receipt data to the server
    // Replace the URL with your server endpoint
    fetch("/send-receipt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // Handle the response from the server
        if (data.success) {
          showMessage("Receipt sent successfully!", "success");
        } else {
          showMessage("Failed to send receipt. Please try again.", "error");
        }
      })
      .catch(function (error) {
        showMessage("An error occurred. Please try again later.", "error");
      });
  } else {
    // Display validation error messages (example using HTML5 constraint validation)
    this.reportValidity();
  }
});

// Show message helper function
function showMessage(message, type) {
  var messagesContainer = document.getElementById("messages");

  if (messagesContainer) {
    var messageElement = document.createElement("li");
    messageElement.textContent = message;
    messageElement.className = type;
    messagesContainer.appendChild(messageElement);
  } else {
    // Handle absence of messages container gracefully
    console.log(
      "No messages container found. Displaying message in alternative way:",
      message
    );
  }
}
