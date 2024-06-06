function validateEmail(email) {
  // Validate email format using regular expression
  var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function validatePhoneNumber(phoneNumber) {
  // Validate phone number format using regular expression
  var phoneRegex = /^\d{10}$/;
  return phoneRegex.test(phoneNumber);
}

document.getElementById("update-form").addEventListener("submit", function(event) {
  event.preventDefault();

  // Get form data
  var emailInput = document.getElementsByName("staff_update_email")[0];
  var phoneInput = document.getElementsByName("staff_update_phone")[0];
  var email = emailInput.value;
  var phoneNumber = phoneInput.value;

  // Validate email
  if (!validateEmail(email)) {
    // Invalid email format
    alert("Invalid email format");
    emailInput.focus();
  }

  // Validate phone number
  if (!validatePhoneNumber(phoneNumber)) {
    // Invalid phone number format
    alert("Invalid phone number format. Please enter a 10-digit number.");
    phoneInput.focus();
  }

});

document.getElementById("login-form").addEventListener("submit", function(event) {
  event.preventDefault();

  // Get form data
  var emailInput = document.getElementsByName("staff_email")[0];
  var phoneInput = document.getElementsByName("staff_phone")[0];
  var email = emailInput.value;
  var phoneNumber = phoneInput.value;

  // Validate email
  if (!validateEmail(email)) {
    // Invalid email format
    alert("Invalid email format");
    emailInput.focus();
    return;
  }

  // Validate phone number
  if (!validatePhoneNumber(phoneNumber)) {
    // Invalid phone number format
    alert("Invalid phone number format. Please enter a 10-digit number.");
    phoneInput.focus();
    return;
  }

});
