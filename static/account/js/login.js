
console.log('login.js loading...');


document.addEventListener("DOMContentLoaded", function() {
    const alertMessage = document.getElementById("alert-message");

    // Only run the timeout if `data-has-messages` is present
    if (alertMessage && alertMessage.dataset.hasMessages === "true") {

        alertMessage.style.display = 'none';
    }
});


// Add click event listener to the close button

// if (close_btn) {
//     close_btn.addEventListener("click", function () {
//         console.log('close-btn is loaded and running');
//         error_div.style.display = 'none';
//     });
// }

// Reusable function to handle input validation

// function validateInput(inputElement, errorElement, errorTextElement, errorMessage) {

//     inputElement.addEventListener('input', function () {

//         if (inputElement.value.trim() === ""){
//             errorElement.style.display = 'flex';
//             errorTextElement.textContent = errorMessage;

//         } else {
//             errorElement.style.display = 'none';
//         }
//     });
// }

// const inputs = [

//     {
//         input: document.getElementById('email'),
//         error: document.getElementById('email-error'),
//         errorText: document.getElementById('email-error-text'),
//         errorMessage: "Email field cannot be empty"
//     },
//     {
//         input: document.getElementById('password1'),
//         error: document.getElementById('pass-error'),
//         errorText: document.getElementById('pass-error-text'),
//         errorMessage: "Password field cannot be empty"
//     },
// ];

// Apply the validation function to each input
// inputs.forEach(({ input, error, errorText, errorMessage }) =>{
//     validateInput(input, error, errorText, errorMessage);
// });


document.addEventListener("DOMContentLoaded", function() {

        const errorDiv = document.getElementById('error-div');
        // console.log(errorDiv)
        const emailInput = document.getElementById('email'); // Update with the actual ID
        // console.log(emailInput)
        const passwordInput = document.getElementById('password1'); // Update with the actual ID
        // console.log(passwordInput)

        // Hide the error message when the user interacts with the email input
        emailInput.addEventListener('focus', function() {
            // console.log('email input runing...')
            if (errorDiv) {
                errorDiv.style.display = 'none'; // Hide error messages
            }
        });

        // Hide the error message when the user starts reentering the password
        passwordInput.addEventListener('focus', function() {
            // console.log('password input runing...')
            if (errorDiv) {
                errorDiv.style.display = 'none'; // Hide error messages
            }
        });
    });

 



document.addEventListener("DOMContentLoaded", function() {
    const emailInput = document.getElementById('email'); 
    const passwordInput = document.getElementById('password1'); 
    const emailErrorDiv = document.getElementById('email-error');
    const passwordErrorDiv = document.getElementById('pass-error');
    const emailError = document.getElementById('email-error-text');
    const passwordError = document.getElementById('pass-error-text');
    const submitbtn = document.getElementById('form-submit');
    
    // Reusable function to handle input validation
    function validateInput(inputElement, errorElement, errorTextElement, errorMessage) {
        inputElement.addEventListener('input', function () {
            if (inputElement.value.trim() === "") {
                errorElement.style.display = 'flex';
                errorTextElement.textContent = errorMessage;
            } else {
                errorElement.style.display = 'none';
            }
        });
    }

    // Validate each input field on input event
    validateInput(emailInput, emailErrorDiv, emailError, "Email field can not be empty.");
    validateInput(passwordInput, passwordErrorDiv, passwordError, "Password field can not be empty.");
    
    submitbtn.addEventListener("click", function(event) {
        console.log('form submit btn clicked');

        // Hide error divs by default
        emailErrorDiv.style.display = 'none';
        passwordErrorDiv.style.display = 'none';

        // Clear previous errors
        emailError.textContent = "";
        passwordError.textContent = "";

        let valid = true;

        // Check if both fields are filled
        if (!emailInput.value) {
            emailError.textContent = "Email field can not be empty.";
            emailErrorDiv.style.display = 'flex';
            valid = false;
        }

        if (!passwordInput.value) {
            passwordError.textContent = "Password field can not be empty.";
            passwordErrorDiv.style.display = 'flex';
            valid = false;
        }

        // If either field is empty, prevent form submission
        if (!valid) {
            event.preventDefault();
        }
    });
});
