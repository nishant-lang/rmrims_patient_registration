from django.urls import path
from .apis import user_registration,user_login,user_change_password,send_password_reset_email,password_reset,get_state_wise_district
from .views import registration_view,login_view,logout_view,patient_register_view,patient_dashbord


urlpatterns = [
    
    path('user-registration/', registration_view, name='user-registration'), 
    path('login-view/', login_view, name='login-view'), 
    path('patient-registration/',patient_register_view,name='patient-registration'),
    path('dashbord/',patient_dashbord,name='dashbord'),
    path('logout/', logout_view, name='logout'),
  
    # path('load_districts/', views.load_districts, name='load_districts'),

    # path('register/', user_registration, name='register'),
    path('indian/states/', get_state_wise_district, name='get_state_wise_district'),  
    path('st_wise_dis/<int:state_id>/', get_state_wise_district, name='st_wise_dis'),
    path('login/', user_login, name='login'),
    path('change-password/',user_change_password, name='change-password'),
    path('send-reset-password-email',send_password_reset_email, name='send-reset-password-email'),
    path('reset-password/<uid>/<token>',password_reset, name='reset_password'),
]
