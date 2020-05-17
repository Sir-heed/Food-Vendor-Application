from rest_framework import serializers
# from FoodVendorApplication.settings import AUTH_USER_MODEL
from .models import Vendor, Customer, Auth

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = ['email','phoneNumber']
        read_only_fields = ['last_login','dateTimeCreated', 'isActive']

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=False)
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['amountOutstanding']

    def create(self, validated_data):
        userData = validated_data.pop('user')
        user = Auth.objects.create(**userData)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer

class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=False)
    class Meta:
        model = Vendor
        fields = '__all__'
        # fields = ['user', 'bussinessName']

    def create(self, validated_data):
        userData = validated_data.pop('user')
        user = Auth.objects.create(**userData)
        vendor = Vendor.objects.create(user=user, **validated_data)
        return vendor

# Since the login fields and set password fields take in the same input, thus the same serializer can be used
class SetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

# class LoginSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(required=True)