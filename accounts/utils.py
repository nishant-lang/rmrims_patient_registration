

import os
from datetime import datetime
from django.core.mail import EmailMessage
from django.db.models import Count
from django.db.models import Avg
from django.db.models.functions import ExtractYear
from accounts.models import PatientRegistration  # Ensure the correct import path for your model
from django.db.models.functions import TruncMonth

class Utils:
    @staticmethod
    def send_email(data):
        # Validate the `data` dictionary
        required_keys = ['subject', 'body', 'to_email']
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing required key: {key}")
        
        from_email = os.environ.get('EMAIL_FROM')

        if not from_email:
            raise EnvironmentError("Environment variable 'EMAIL_FROM' is not set")
        
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=from_email,
            to=[data['to_email']]
        )

        # try:
        email.send()

        # except Exception as e:
        #     # Handle or log the exception as needed
        #     print(f"Error sending email: {e}")
        #     # You might want to raise the exception or log it based on your application's needs


""""BAR CHART  CODE START""" 

def get_patient_growth_data():
    # Fetch and annotate data based on appointment year

    mx_of_year=10

    patients_by_years = PatientRegistration.objects.annotate(year=ExtractYear('appointment_date'))\
    .values('year')\
    .annotate(total_patients=Count('id'))\
    .order_by('year')
    
    
    total_number_year=len(patients_by_years)

    if total_number_year>=mx_of_year:

        # print('if part runed....')
        start_year_from=total_number_year-mx_of_year

        # Prepare the data for charts
        years = [entry['year'] for entry in patients_by_years][start_year_from:]
        patient_growth = [entry['total_patients'] for entry in patients_by_years][start_year_from:]

        return years, patient_growth
    
    else:
        # print('else part runed.....')
        years = [entry['year'] for entry in patients_by_years]
        patient_growth = [entry['total_patients'] for entry in patients_by_years]

        return years, patient_growth

""""BAR CHART  CODE END""" 

""""PIE CHART  CODE START""" 
def get_department_patient_data():

    # Query to group patients by department and count them.

    department_data = PatientRegistration.objects.values('department')\
        .annotate(patient_count=Count('id'))\
        .order_by('department')
        
    # Prepare the labels and data arrays
    department = [[entry['department']] for entry in department_data]
    patient_count = [entry['patient_count'] for entry in department_data]
    
    print('department:', department)
    print('patient_count:',patient_count )

    return department, patient_count

""""PIE CHART  CODE END""" 

"""HORIZONTAL CHART  CODE START"""
def patient_age_per_department():
    department_avg_ages=PatientRegistration.objects.values('department').annotate(avg_age=Avg('age')).order_by('department')

    # print(department_avg_ages)
    
# Prepare data for return
    departments = [
        item['department']  # Directly use the department name
        for item in department_avg_ages
    ]
    ages = [
        item['avg_age'] if item['avg_age'] is not None else 0
        for item in department_avg_ages
    ]

    return departments,ages

"""HORIZONTAL CHART  CODE END"""



"""LINE CHART  CODE START"""

def get_patient_data_per_month():
    # Get the current year
    current_year = datetime.now().year

    # Query to count patients registered per month for the current year
    patient_data = (
        PatientRegistration.objects.filter(appointment_date__year=current_year)  # Filter by current year
        .annotate(month=TruncMonth('appointment_date'))  # Group by month
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    # Prepare data for the frontend
    months = []
    counts = []
    for entry in patient_data:
        if entry['month']:
            months.append(entry['month'].strftime('%B'))  # Convert to full month name
            counts.append(entry['count'])
        else:
            months.append('Unknown')  # Handle cases where `month` is None
            counts.append(0)

    # Return the data as a tuple
    return months, counts

"""LINE CHART CODE END"""


"""PATIENT STATISTICS START"""

def patient_statistics():

    total_patients = PatientRegistration.objects.count()
    gender_counts = PatientRegistration.objects.values('gender').annotate(count=Count('gender'))

    # Prepare gender-specific counts
    gender_stats = {item['gender']: item['count'] for item in gender_counts}

    total_male = gender_stats.get('MALE', 0)
    total_female = gender_stats.get('FEMALE', 0)
    total_other = gender_stats.get('OTHER', 0)
    total_prefer_not_to_say = gender_stats.get('PREFER_NOT_TO_SAY', 0)

    return total_patients,total_male,total_female,total_other

"""PATIENT STATISTICS END"""



"""BELOW CODE IS FOR POPULATE THE DATABASE FOR STATE WISE DISTRICT"""

import os
import json
from accounts.models import State, District

# Function to load the states and districts from JSON

os.environ['DJANGO_SETTINGS_MODULE'] = 'rmrims_api.settings'
import django

def load_states_and_district(file_path):

    django.setup()

  
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






'''
NOTE:

RUN BELOW CODE TO POPULATE THE DATA

python manage.py shell
from utils import load_states_and_districts
load_states_and_district(r'static\account\data\states_data.json')

'''


"""CODE END"""



"""load_data.py code written below"""

# import os
# import django
# import json

# os.environ['DJANGO_SETTINGS_MODULE'] = 'rmrims_api.settings'

# import django
# django.setup()

# from accounts.models import State, District

# # Function to load the states and districts from JSON
# def load_states_and_districts(file_path):
#     with open(file_path, 'r') as file:  # Open the file with the correct path
#         data = json.load(file)
        
#         print(f'data: {data}')

#     for state_data in data:
#         state_name = state_data['state']
#         state, created = State.objects.get_or_create(name=state_name)  # Case-insensitive lookup

#         # Debugging: Check if the state is created or already exists
#         print(f"State: {state_name}, Created: {created}")

#         for district_name in state_data['districts']:
#             # Debugging: Check if the district is being created
#             district, created = District.objects.get_or_create(name=district_name, state=state)
#             print(f"District: {district_name}, Created: {created}")

#     print("Data successfully loaded into the database.")

# # Path to your JSON file
# file_path = 'states_data.json'  # Update this with your JSON file's path

# # Call the function to load data
# load_states_and_districts(file_path)


