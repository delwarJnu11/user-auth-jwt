from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login,authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserListSerializer
)

from .models import User


class AuthUserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)
        
#login view
# class AuthUserLoginView(APIView):
#     serializer_class = UserLoginSerializer
#     permission_classes = (AllowAny, )

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         valid = serializer.is_valid(raise_exception=True)

#         if valid:
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']
#             user = authenticate(request, email=email, password=password)

#             if user:
#                 login(request, user)
#                 status_code = status.HTTP_200_OK

#                 response = {
#                     'success': True,
#                     'statusCode': status_code,
#                     'message': 'User logged in successfully',
#                     'access': serializer.data['access'],
#                     'refresh': serializer.data['refresh'],
#                     'authenticatedUser': {
#                         'email': serializer.data['email'],
#                         'role': serializer.data['role']
#                     }
#                 }

#                 return Response(response, status=status_code)
#             else:
#                 status_code = status.HTTP_401_UNAUTHORIZED
#                 response = {
#                     'success': False,
#                     'statusCode': status_code,
#                     'message': 'Invalid login credentials',
#                 }
#                 return Response(response, status=status_code)
        
class AuthUserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                status_code = status.HTTP_200_OK

                refresh = RefreshToken.for_user(user)
                refresh_token = str(refresh)
                access_token = str(refresh.access_token)

                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'User logged in successfully',
                    'access': access_token,
                    'refresh': refresh_token,
                    'authenticatedUser': {
                        'email': email,
                        'role': user.role  # Assuming user has a 'role' attribute
                    }
                }

                return Response(response, status=status_code)
            else:
                status_code = status.HTTP_401_UNAUTHORIZED
                response = {
                    'success': False,
                    'statusCode': status_code,
                    'message': 'Invalid login credentials',
                }
                return Response(response, status=status_code)

        
#User list view
class UserListView(APIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.role != 1:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched users',
                'users': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)