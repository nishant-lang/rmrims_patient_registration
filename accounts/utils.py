

import os
from datetime import datetime
from django.core.mail import EmailMessage
from django.db.models import Count
from django.db.models import Avg
from django.db.models.functions import ExtractYear
from .models import PatientRegistration  # Ensure the correct import path for your model
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


# BAR CHART 

def get_patient_growth_data():
    # Fetch and annotate data based on appointment year

    mx_of_year=10

    patients_by_years = PatientRegistration.objects.annotate(year=ExtractYear('appointment_date'))\
    .values('year')\
    .annotate(total_patients=Count('id'))\
    .order_by('year')
    
    
    total_number_year=len(patients_by_years)

    if total_number_year>=mx_of_year:

        print('if part runed....')
        start_year_from=total_number_year-mx_of_year

        # Prepare the data for charts
        years = [entry['year'] for entry in patients_by_years][start_year_from:]
        patient_growth = [entry['total_patients'] for entry in patients_by_years][start_year_from:]

        return years, patient_growth
    
    else:
        print('else part runed.....')
        years = [entry['year'] for entry in patients_by_years]
        patient_growth = [entry['total_patients'] for entry in patients_by_years]

        return years, patient_growth

def get_department_patient_data():

    # Query to group patients by department and count them.
   
    department_data = PatientRegistration.objects.values('department')\
        .annotate(patient_count=Count('id'))\
        .order_by('department')
    
     # Map department codes to their human-readable names
    # department_labels = dict(PatientRegistration.DEPARTMENTS)
 
    
    # Prepare the labels and data arrays
    department = [[entry['department']] for entry in department_data]
    patient_count = [entry['patient_count'] for entry in department_data]

    print(department)
    print(patient_count)
    
    return department, patient_count


def patient_age_per_department():

    department_avg_ages=PatientRegistration.objects.values('department').annotate(avg_age=Avg('age')).order_by('department')

    print(department_avg_ages)
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



def get_patient_data_per_month():
    # Get the current year
    current_year = datetime.now().year

    print(f'current year {current_year}')

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

    # Debugging output (optional, remove in production)
    print(months)
    print(counts)

    # Return the data as a tuple
    return months, counts
