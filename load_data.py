import os
import django
import json
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'rmrims_api.settings'

import django
django.setup()

from accounts.models import State, District


# Function to load the states and districts from JSON
def load_states_and_districts(file_path):
    with open(file_path, 'r') as file:  # Open the file with the correct path
        data = json.load(file)
        print(f'data: {data}')

    for state_data in data:
        state_name = state_data['state']
        state, created = State.objects.get_or_create(name=state_name)  # Case-insensitive lookup

        # Debugging: Check if the state is created or already exists
        print(f"State: {state_name}, Created: {created}")

        for district_name in state_data['districts']:
            # Debugging: Check if the district is being created
            district, created = District.objects.get_or_create(name=district_name, state=state)
            print(f"District: {district_name}, Created: {created}")

    print("Data successfully loaded into the database.")

# Path to your JSON file
file_path = 'states_data.json'  # Update this with your JSON file's path

# Call the function to load data
load_states_and_districts(file_path)


