from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
# from django.contrib.auth import get_user_model
from accounts.models import CustomUser

class AccountTest(APITestCase):

    def setUp(self):
        User = CustomUser
        self.user = User.objects.create_user(
            email='karanti110@gmail.com',
            first_name='Karan',
            last_name='Verma',
            mobile='8214254256',
        )
        self.user.set_password('1234')
        self.user.save()

    def test_register(self):
        """the email and mobile number should be change"""
        _data = {
            "email": "karan123@gmail.com",
            "first_name": "Karan",
            "last_name": "Verma",
            "mobile": "821454256",
            "password": "1234",
            "password2": "1234" 
        }

        url = reverse('register') 
        _response = self.client.post(url, data=_data, format="json")
        
        self.assertEqual(_response.status_code, status.HTTP_201_CREATED)
        response_data = _response.json()

        print(response_data)
      
        
        self.assertEqual(response_data['data']['email'], _data['email'])

    # def test_login(self):
    #     _data = {
    #         "email": "karanti110@gmail.com",
    #         "password": "1234",
    #     }

    #     url = reverse('login')
    #     _response = self.client.post(url, data=_data, format="json")
        
    #     response_data = _response.json()
    #     print(f'response_data: {response_data}')
        
    #     self.assertEqual(_response.status_code, status.HTTP_200_OK)
       
