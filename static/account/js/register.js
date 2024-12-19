    
console.log("register.js is loaded and running.");


//Below code to make the password1 visble (eye) 
document.getElementById('toggle-password1')?.addEventListener('click', function () {

    console.log('Password toggle function is called');

    const passwordField = document.getElementById('password1'); // Ensure this ID matches the form field ID

    if (passwordField) { // Check if passwordField exists before accessing attributes
        const passwordFieldType = passwordField.getAttribute('type');
        
        if (passwordFieldType === 'password') {
            passwordField.setAttribute('type', 'text');
            this.classList.add('show-password');
        } else {
            passwordField.setAttribute('type', 'password');
            this.classList.remove('show-password');
        }
    }
});


//Below code to make the password2 visble (eye)
document.getElementById('toggle-password2')?.addEventListener('click', function () {

    console.log('Password toggle function is called');

    const passwordField = document.getElementById('password2'); // Ensure this ID matches the form field ID

    if (passwordField) { // Check if passwordField exists before accessing attributes
        const passwordFieldType = passwordField.getAttribute('type');
        
        if (passwordFieldType === 'password') {
            passwordField.setAttribute('type', 'text');
            this.classList.add('show-password');
        } else {
            passwordField.setAttribute('type', 'password');
            this.classList.remove('show-password');
        }
    }
});


function validateInput(inputElement, errorElement, errorTextElement, errorMessage) {
    
//    console.log(inputElement)
//    console.log(errorElement)
//    console.log(errorTextElement)

    // Check for backend errors initially
    if (errorTextElement.textContent.trim()) {
        errorElement.classList.add('visible');  // Add class for visibility
    } else {
        errorElement.classList.remove('visible');  // Remove class if no backend error
    }

// Add event listener to handle input changes
inputElement.addEventListener('input', function () {
        
        if (inputElement.value.trim() === "") {

            // Show JavaScript error when input is empty
            errorTextElement.textContent = errorMessage;
            errorElement.classList.add('visible');  // Show the error 

        } else {
            // Hide error when input is valid or being filled
            errorElement.classList.remove('visible');  // Hide the error
        }
    });
}

// Define all the input, error, and error text elements

const inputs = [

    {
        input: document.getElementById('email'),
        error: document.getElementById('email-error'),
        errorText: document.getElementById('email-error-text'),
        errorMessage: "Email field cannot be empty"
    },

    {
        input: document.getElementById('first_name'),
        error: document.getElementById('first-error'),
        errorText: document.getElementById('first-error-text'),
        errorMessage: "First name field cannot be empty"
    },
    {
        input: document.getElementById('last_name'),
        error: document.getElementById('last-error'),
        errorText: document.getElementById('last-error-text'),
        errorMessage: "Last name field cannot be empty"
    },
    {
        input: document.getElementById('mobile'),
        error: document.getElementById('mob-error'),
        errorText: document.getElementById('mob-error-text'),
        errorMessage: "Mobile number field cannot be empty"
    },
    {
        input: document.getElementById('password1'),
        error: document.getElementById('pass1-error'),
        errorText: document.getElementById('pass1-error-text'),
        errorMessage: "Password field cannot be empty"
    },
    {
        input: document.getElementById('password2'),
        error: document.getElementById('pass2-error'),
        errorText: document.getElementById('pass2-error-text'),
        errorMessage: "Confirm Password field cannot be empty"
    }
];

// Apply the validation function to each input
inputs.forEach(({ input, error, errorText, errorMessage }) => {
    validateInput(input, error, errorText, errorMessage);
});




