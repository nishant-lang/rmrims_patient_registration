from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserPasswordChangeSerializer,
    SendPasswordResetEmailSerializer,
    PasswordResetSerializer,StateWiseDistrictSerializer
    # LogoutSerializer
)
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
# from django.contrib.auth import authenticate, login , logout
from django.http import HttpResponse
from accounts.models import State,District


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
from django.views.decorators.csrf import csrf_exempt



@api_view(['POST'])
@permission_classes([AllowAny])

def user_registration(request):
    # print('__________________________________')
    print(request.data)

    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({"message": "User created successfully", "data": serializer.data, "token": token}, status=status.HTTP_201_CREATED)
    
    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)





# from django.views.decorators.csrf import csrf_exempt

# @api_view(['POST'])
# @permission_classes([AllowAny])
# @csrf_exempt

# def user_login(request):
#     serializer = UserLoginSerializer(data=request.data)
#     if serializer.is_valid():
#         email = serializer.validated_data.get('email')
#         password = serializer.validated_data.get('password')
#         user = authenticate(email=email, password=password)
#         if user is not None:
#             # login(request, user)  # Log the user in
#             # token = get_tokens_for_user(user)
#             return Response({"message": "User login successful", "authenticated": True}, status=status.HTTP_200_OK)
#         return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
#     return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])

def user_login(request):

    print(f'login request:   {request}')


    serializer = UserLoginSerializer(data=request.data)

    if serializer.is_valid():

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        
        user = authenticate(email=email, password=password)

        print(email)
        print(password)
        print(user)

        if user is not None:
            # Generate JWT token using SimpleJWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "message": "User login successful", 
                "authenticated": True, 
                "access_token": access_token,
                "refresh_token": str(refresh)
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
@permission_classes([IsAuthenticated])

def user_change_password(request):
    serializer = UserPasswordChangeSerializer(data=request.data, context={'user': request.user})
    if serializer.is_valid():
        user = request.user
        serializer.update(user, serializer.validated_data)

        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])

def send_password_reset_email(request):
    serializer = SendPasswordResetEmailSerializer(data=request.data,context={'request': request})
    if serializer.is_valid():
        return Response({"message": "Reset password email sent, please check."}, status=status.HTTP_200_OK)
    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])

def password_reset(request, uid, token):

    context = {'uid': uid, 'token': token}
    serializer = PasswordResetSerializer(data=request.data, context=context)
    if serializer.is_valid():
        return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['GET'])

# def get_state_wise_district(request, state_name):
#     try:
#         print('get_state_wise_district run.')
#         state = State.objects.get(state=state_name)  # Replace with your actual field name
#         serializer = StateWiseDistrictSerializer(state)
#         return Response(serializer.data)
#     except Exception as e:
#         # Catch any other exception and return a generic error
#         return Response({"error": str(e)}, status=500)


# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from .models import State, District
# from .serializers import StateWiseDistrictSerializer,StateSerializer

  

# @api_view(['GET'])

# def get_state_wise_district(request, state_name=None):

#     if state_name is None:
#         # If no state_name is provided, return all states
#         try:
#             states = State.objects.all()  # Get all states
#             serializer = StateSerializer(states, many=True)
#             return Response({'states': serializer.data},status=200)
        
#         except Exception as e:
#             return Response({"error": str(e)}, status=500)
#     else:
#         try:
#             state = State.objects.get(name=state_name)  
#             serializer = StateWiseDistrictSerializer(state)
#             return Response(serializer.data,status=200)
    
#         except State.DoesNotExist:
#             # Handle case where the state is not found
#             return Response({"error": f"State '{state_name}' not found."}, status=404)
    
#         except Exception as e:
#             # Catch any other exception and return a generic error
#             return Response({"error": str(e)}, status=500)





from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import DatabaseError
import logging
from .models import State
from .serializers import StateSerializer, StateWiseDistrictSerializer



# Setting up logger
logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_state_wise_district(request, state_id=None):

    try:
        if state_id is None:
            # Return all states if no state_name is provided
            states = State.objects.all()
            serializer = StateSerializer(states, many=True)
            return Response({'states': serializer.data}, status=200)
        else:
            # Get the state and its districts
            state = State.objects.get(id=state_id)
            
            serializer = StateWiseDistrictSerializer(state)
            return Response(serializer.data, status=200)

    except State.DoesNotExist:
        # If state doesn't exist, return a 404 error
        logger.error(f"State '{state_id}' not found.")
        return Response({"error": f"State '{state_id}' not found."}, status=404)
    except DatabaseError as db_err:
        # Handle database errors
        logger.error(f"Database error occurred: {str(db_err)}")
        return Response({"error": "Database error occurred."}, status=500)
    except Exception as e:
        # Generic error handler
        logger.error(f"Error occurred: {str(e)}")
        return Response({"error": str(e)}, status=500)

    

