
# from rest_framework_simplejwt.tokens import RefreshToken
import json
from django.middleware.csrf import get_token
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm,UserLoginForm,PatientRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from accounts.utils import get_patient_growth_data,get_department_patient_data,patient_age_per_department,get_patient_data_per_month,patient_statistics


def registration_view(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        # print(form.data)
        if form.is_valid():
            form.save()
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Hash the password
            user.save() 
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('/login-view/') 
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('/patient-registration/')
    else:
        form = UserLoginForm()
        print('geting form')
    return render(request, 'account/login.html', {'form': form})


@login_required(login_url='/login-view/') 
def logout_view(request):
    if request.method == 'POST':
        logout(request)  # This clears the session and logs out the user
        return redirect('/login-view/')  # Redirect to the login page after logging 


@login_required(login_url='/login-view/')  # Redirects unauthenticated users to a specific page

def patient_register_view(request):

    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.instance.registered_by=request.user
            form.save()  # Save the form data to the database

            messages.success(request,'Patient successfully registered.',)
            return redirect('/dashbord/',context={'success_value':'hellooo'})
        
        else:
            messages.error(request,'Please correct the errors below.',)
    else:
        form = PatientRegistrationForm()
    return render(request, 'account/patient_reg.html', {'form': form})



def patient_dashbord(request):

    total_patients,total_male,total_female,total_other= patient_statistics()

    years, patient_growth = get_patient_growth_data()

    department, patient_count = get_department_patient_data()

    departments, ages = patient_age_per_department()

    months,counts=get_patient_data_per_month()

    return render(request,'account/dashbord.html',{

        'total_patients':total_patients,
        'total_male':total_male,
        'total_female':total_female,
        'total_other':total_other,
        
        'years': years,
        'growth': patient_growth,
        'department':department,
        'patient_count':patient_count,
        'departments':departments,
        'ages':ages,
        'months':months,
        'counts':counts
    })
