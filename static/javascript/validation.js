function validateForm() {
  // Retrieve form input values
  var name = $('#name').val().trim();
  var email = $('#email').val().trim();
  var username = $('#username').val().trim();
  var password = $('#password').val().trim();
  var confirm_password = $('#confirm_password').val().trim();
  var card_number = $('#card_number').val().replace(/-/g, ''); // Remove any hyphen

  // Perform validation checks
  if (name === '' || email === '' || username === '' || password === '' || confirm_password === '') {
    alert('Please fill in all fields.');
    return false; // Prevent form submission
  }

  // Regular expression to verify valid email
  var email_regex = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
  if (!email_regex.test(email)) {
    alert('Please enter a valid email address.');
    return false; // Prevent form submission
  }

  if (card_number.length !== 16) {
    alert('Please enter a valid 16-digit credit/debit card number.');
    return false; // Prevent form submission
  }

  if (password.length < 8) {
    alert('Password must be at least 8 characters long.');
    return false; // Prevent form submission
  }

  if (password.search(/[a-z]/) < 0) {
    alert('Password must contain at least one lowercase letter.');
    return false; // Prevent form submission
  }

  if (password.search(/[A-Z]/) < 0) {
    alert('Password must contain at least one uppercase letter.');
    return false; // Prevent form submission
  }

  if (password.search(/[0-9]/) < 0) {
    alert('Password must contain at least one digit.');
    return false; // Prevent form submission
  }

  if (password !== confirm_password) {
    alert('Password and confirm password do not match.');
    return false; // Prevent form submission
  }

  // If all validations pass, allow form submission
  return true;
}

function togglePasswordVisibility(id) {
  var passwordInput = document.getElementById(id);
  var togglePasswordIcon = document.getElementById(`toggle-password-icon-${id}`);
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    togglePasswordIcon.className = "fas fa-eye-slash";
  } else {
    passwordInput.type = "password";
    togglePasswordIcon.className = "fas fa-eye";
  }
}

function formatCardNumber(input) {
  // Remove any non-digit characters
  var cardNumber = input.value.replace(/\D/g, '');

  // Limit the card number to 16 digits
  cardNumber = cardNumber.substring(0, 16);

  // Apply formatting
  var formattedCardNumber = '';
  for (var i = 0; i < cardNumber.length; i++) {
    if (i > 0 && i % 4 === 0) {
      formattedCardNumber += '-';
    }
    formattedCardNumber += cardNumber.charAt(i);
  }

  // Update the input value
  input.value = formattedCardNumber;
}
