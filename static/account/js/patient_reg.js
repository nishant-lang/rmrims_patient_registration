    
console.log("patient_reg.js is loaded and running.");


document.addEventListener('DOMContentLoaded', function () {
  
    const modalContainer = document.getElementById('modal');
    const modalHeaderBtn = document.getElementById('modl-header-btn');
    const modalFootBtn = document.getElementById('modl-foot-btn');

    if (modalContainer && modalHeaderBtn && modalFootBtn) {
        // Function to close modal smoothly
        function closeModal() {
            if (modalContainer) {
                console.log('hidden code  works')
                modalContainer.classList.add('hidden'); // Add hidden class to trigger smooth close
            }
        }

        // Close modal when header button is clicked
        modalHeaderBtn.addEventListener('click', closeModal);

        // Close modal when footer button is clicked
        modalFootBtn.addEventListener('click', closeModal);
    }
});



document.addEventListener('DOMContentLoaded', function () {

    const stateSelect = document.getElementById('state');  // Access the state dropdown
    const districtSelect = document.getElementById('district');  // Access the district dropdown

    console.log(stateSelect);
    console.log(districtSelect);

    // Ensure elements exist
    if (stateSelect && districtSelect) {

        // Function to fetch and populate districts
        const fetchDistricts = (selectedStateId) => {
            if (selectedStateId) {
                fetch(`/st_wise_dis/${selectedStateId}/`)
                    .then(response => response.json())
                    .then(data => {
                        // Clear the district dropdown before populating
                        districtSelect.innerHTML = "<option value=''>Select District</option>";

                        // Populate the district dropdown with fetched districts
                        data.districts.forEach(function (district) {
                            const option = document.createElement('option');
                            option.value = district.id;
                            option.textContent = district.name;
                            districtSelect.appendChild(option);
                        });
                    })
                    .catch(error => {
                        console.error("Error fetching districts:", error);
                    });
            } else {
                // If no state is selected, reset the district dropdown
                districtSelect.innerHTML = "<option value=''>Select District</option>";
            }
        };

        // Add event listener for state selection changes
        stateSelect.addEventListener('change', function () {
            const selectedStateId = stateSelect.value;
            fetchDistricts(selectedStateId);
        });

        // Automatically trigger change event if a default state is selected
        if (stateSelect.value) {
            fetchDistricts(stateSelect.value);
        }
    } else {
        console.error("State or District select element not found!");
    }
});


    
// //Below code for make none field error none.

// document.addEventListener('DOMContentLoaded', function () {
//     const close_btn  = document.getElementById('cls-btn');  // Access the state dropdown
//     const non_field_error=document.getElementById('non-field-error')

// close_btn.addEventListener('click',function(){

//         if (non_field_error){
//             non_field_error.style.display='none'
//         }
//         else{
//             non_field_error.style.display='none'
//         }
        
//     });
// });



//Below code is for make none_error_field none.

document.addEventListener('DOMContentLoaded', function () {
    
    const closeBtn = document.getElementById('cls-btn'); // Close button for error
    const nonFieldError = document.getElementById('non-field-error'); // Error container
    const formElements = document.querySelectorAll('input, select, textarea'); // All form fields

    // Hide error on close button click
    if (closeBtn) {
        closeBtn.addEventListener('click', function () {
            if (nonFieldError) {
                nonFieldError.style.display = 'none'; // Hide the error message
            }
        });
    }

    // Hide error on interaction with any form field
    formElements.forEach((element) => {
        element.addEventListener('input', function () {
            if (nonFieldError) {
                nonFieldError.style.display = 'none'; // Hide the error message
            }
        });

        element.addEventListener('change', function () {
            if (nonFieldError) {
                nonFieldError.style.display = 'none'; // Hide the error message
            }
        });
    });
});
