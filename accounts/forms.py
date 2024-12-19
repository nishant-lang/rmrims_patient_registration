
from django import forms
from .models import CustomUser,PatientRegistration 
from accounts.models import State
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password1'}), label='Password', max_length=50)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password2'}), label='Confirm Password', max_length=50)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'mobile', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'id': 'email'}),
            'first_name': forms.TextInput(attrs={'id': 'first_name'}),
            'last_name': forms.TextInput(attrs={'id': 'last_name'}),
            'mobile': forms.TextInput(attrs={'id': 'mobile'}),
            'password1': forms.PasswordInput(attrs={'id': 'password1'}),
            'password2': forms.PasswordInput(attrs={'id': 'password2'}),
        }

    def clean(self):
        
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # Only perform this check if the combined validation has not already raised an error
        if not self.errors and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This Email is already registered.")
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        # Only perform this check if the combined validation has not already raised an error
        if not self.errors and CustomUser.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError("This mobile number is already registered.")
        return mobile


class UserLoginForm(forms.Form): 

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'id': 'email'}),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'password1'}),
        label='Password'
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                # print("This email is not registered.")
                raise forms.ValidationError("You are not a registered user.")

            if not user.check_password(password):
                # print("The password is incorrect.")
                raise forms.ValidationError("The password is invalid.")
            cleaned_data['user'] = user
        return cleaned_data



class PatientRegistrationForm(forms.ModelForm):
   
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'id': 'dob'})
    )

    gender = forms.ChoiceField(
        choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('PREFER_NOT_TO_SAY', 'Prefer Not to Say')],
        widget=forms.Select(attrs={'id': 'gender'})
    )

 # Define the state field here as a ModelChoiceField
    state = forms.ModelChoiceField(
        queryset=State.objects.all(),
        empty_label="Select State",
        widget=forms.Select(attrs={'id': 'state', 'class': 'expanded-dropdown'})
    )

    appointment_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date', 'id': 'appointment_date', 'placeholder': 'Select Appointment Date'})
    )

    class Meta:
        model = PatientRegistration

        fields = [ 'name','age' ,'gender', 'email','contact_number','aadhar_number', 'state', 'district', 'address', 'department', 
        'symptoms', 'consultation_type', 'appointment_date',] 


        widgets = {
            
            'name': forms.TextInput(attrs={'id': 'name','placeholder':'Enter your name.' }),

            'age': forms.TextInput(attrs={'id': 'age','placeholder':'Enter your age.'}),

            'gender': forms.Select(attrs={'id': 'gender'}),

            'email': forms.EmailInput(attrs={'id': 'email','placeholder':'Enter your email.'}),

            'contact_number': forms.TextInput(attrs={'id': 'contact_number','placeholder':'Enter contact number.'}),

            'aadhar_number':forms.TextInput(attrs={'id':'aadhar','placeholder':'Enter your aadhar number.'}),
           
            'district': forms.Select(attrs={'id': 'district'}),

            'address': forms.TextInput(attrs={'id': 'address','placeholder':'Enter your Address.'}),

            'department': forms.Select(attrs={'id': 'department'}),

            'consultation_type': forms.Select(attrs={'id': 'consultation_type'}),
        
            'symptoms': forms.Textarea(attrs={'id': 'symptoms','rows': 4, 'cols': 50,'placeholder':'Write about your health related issue.'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the default state to "Bihar"
        try:
            self.fields['state'].initial = State.objects.get(name="Bihar").id
        except State.DoesNotExist:
            pass 

    def clean(self):

        print('clean function running...')

        cleaned_data = super().clean()
        
        name = cleaned_data.get('name')
        contact_number = cleaned_data.get('contact_number')
        department = cleaned_data.get('department')
        consultation_type = cleaned_data.get('consultation_type')
        appointment_date = cleaned_data.get('appointment_date')

        # Check for existing appointments with the same details

        existing_appointment = PatientRegistration.objects.filter(
            name=name,
            contact_number=contact_number,
            department=department,
            consultation_type=consultation_type,
            appointment_date=appointment_date
        ).exists()

        if existing_appointment:
            raise ValidationError(
                "An appointment with this name and contact number already exists for the selected department and consultation type on this date."
            )
        return cleaned_data
