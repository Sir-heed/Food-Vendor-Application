from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
# from FoodVendorApplication.settings import AUTH_USER_MODEL
from .serializers import CustomerSerializer, VendorSerializer, UserSerializer, SetPasswordSerializer
from .models import Customer, Vendor, Auth

# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

# Set password for both the vendor an customer after signup, it takes in email
class SetPassword(APIView):
    serializer_class = SetPasswordSerializer

    def post(self, request, format=None):
        email = request.data.get('email')
        password = request.data.get('password')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Check if the email is in database
            if Auth.objects.filter(email=email).exists():
                user = Auth.objects.get(email = email)
                # Check if the password is empty
                if user.password == "":
                    user.set_password(password)
                    user.active = True
                    user.save()
                    return Response("User password set successfully", status=status.HTTP_201_CREATED)
                else:
                    return Response("You already set your password, you can proceed to login", status = status.HTTP_409_CONFLICT)
            else:
                return Response("User does not exist, return to the signup page", status = status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login the customer
class CustomerLogin(APIView):
    serializer_class = SetPasswordSerializer

    def post(self, request, format=None):
        # Logout user if already login
        logout(request)
        # Get input data
        email = request.data.get('email')
        password = request.data.get('password')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                # Check if user exist
                user = Auth.objects.get(email=email)
                # Check if user is customer
                try:
                    customer = Customer.objects.get(user_id=user.id)
                    # Check if password match
                    if check_password(password, user.password):
                        login(request, user)
                        return Response("User logged in succesfully", status=status.HTTP_200_OK)
                    else:
                        return Response("Invalid password", status=status.HTTP_404_NOT_FOUND)
                except Customer.DoesNotExist:
                    return Response("This email does not belong to a customer", status=status.HTTP_400_BAD_REQUEST)
            except Auth.DoesNotExist:
                return Response("No account exist for this email", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login the vendor
class VendorLogin(APIView):
    serializer_class = SetPasswordSerializer

    def post(self, request, format=None):
        # Logout user if already login
        logout(request)
        # Get input data
        email = request.data.get('email')
        password = request.data.get('password')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Check if email is registered
            try:
                user = Auth.objects.get(email=email)
                # if user is a vendor
                try:
                    vendor = Vendor.objects.get(user_id=user.id)
                    # Check if password match
                    if check_password(password, user.password):
                        login(request, user)
                        return Response("User logged in succesfully", status=status.HTTP_200_OK)
                    else:
                        return Response("Invalid password", status=status.HTTP_404_NOT_FOUND)
                except Vendor.DoesNotExist:
                    return Response("This email does not belong to a vendor", status=status.HTTP_400_BAD_REQUEST)
            except Auth.DoesNotExist:
                return Response("No account exist for this email", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Logout user
class LogoutUser(APIView):
    def get(self, request, format=None):
        logout(request)
        return Response('User logged out successfully', status=status.HTTP_200_OK)
