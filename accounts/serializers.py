from rest_framework import serializers
from accounts.models import CustomUser
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from accounts.utils import Utils
from django.contrib.auth import authenticate
from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from accounts.models import District,State

class UserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'mobile', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):

        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError({"detail": "Password and confirm password don't match"})
        
        return data
    
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError({"detail": "This email is already in use"})
        return value

    def validate_mobile(self, value):
        if CustomUser.objects.filter(mobile=value).exists():
            raise serializers.ValidationError({"detail": "Mobile number is already in use"})
        return value

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def validate_email(self, value):
        # print(value)
         # Check if the email exists in the database
        try:
            user = CustomUser.objects.get(email=value)

        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'detail':"No account found with this email"})
        
        return value

    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Check if the password is correct
        user = authenticate(email=email, password=password)
       
        if not user:
            raise serializers.ValidationError({"detail":"Incorrect password"})

        # Check if user is active
        if not user.is_active:
            raise serializers.ValidationError({"detail":"This account is inactive"})

        return data
    



class UserPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({"detail": "Password and confirm password don't match"})
        return attrs
    
    def update(self, user, validated_data):
        user.set_password(validated_data['password'])
        user.save()
        return user

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    
    def validate(self, attrs):
        email = attrs.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError({"detail": "No user associated with this email."})
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        link = f"{self.context['request'].build_absolute_uri('/account/reset-password/')}{uid}/{token}"
        # link = f"http://127.0.0.1:8000/account/reset-password/{uid}/{token}"


        data = {
            "subject": 'Reset your password',
            "body": f'Please click the below link to reset your password:\n\n{link}',
            "to_email": user.email,
        }

        Utils.send_email(data)
        return attrs

class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        uid = self.context.get('uid')
        token = self.context.get('token')

        if password != confirm_password:
            raise serializers.ValidationError({"detail": "Password and confirm password don't match"})
        
        try:
            user_id = smart_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError({"detail": "Token is not valid or expired."})
            
            user.set_password(password)
            user.save()
            return attrs
        
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError({"detail": "Invalid token or user does not exist."})
        
        except DjangoUnicodeDecodeError:
            raise serializers.ValidationError({"detail": "Token is not valid or expired."})


from rest_framework import serializers

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True, help_text="The refresh token to be blacklisted")

    def validate_refresh_token(self, value):
        # Optional: Add custom validation logic if needed
        if not value:
            raise serializers.ValidationError("Refresh token is required")
        return value


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id','name']

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id','name']

class StateWiseDistrictSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True) 

    class Meta:
        model = State
        fields = ['id','name', 'districts']  


