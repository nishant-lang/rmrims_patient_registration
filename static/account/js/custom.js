
document.addEventListener('DOMContentLoaded', function() {
    
    console.log('Statefield...')

    // Get the state and district dropdown elements

    const stateField = document.getElementById('id_state');
    const districtField = document.getElementById('id_district');

    // console.log(stateField)
    // console.log(districtField)

    if (stateField) {
        stateField.addEventListener('change', function() {

            const stateId = stateField.value; // Get the selected state ID

            if (stateId) {
                // Make an AJAX request to fetch districts for the selected state
                fetch(`/st_wise_dis/${stateId}/`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    // console.log(response.json())
                    return response.json();
                })
                .then(statewisedata => {
                    // console.log(statewisedata)
                    const districts = statewisedata.districts;

                    // Clear existing districts
                    districtField.innerHTML = '<option value="">select district</option>';

                    districts.forEach(district => {
                        console.log('District ID:', district.id, 'Name:', district.name);
                   
                    // Populate district dropdown with new options
                        const option = document.createElement('option');
                        option.value = district.id;
                        option.textContent = district.name;
                        districtField.appendChild(option);
                    });
                
                })
                .catch(error => {
                    console.error('Error fetching districts:', error);
                });
            } else {
                // If no state is selected, clear the district dropdown
                districtField.innerHTML = '<option value="">---------</option>';
            }
        });
    }
});
