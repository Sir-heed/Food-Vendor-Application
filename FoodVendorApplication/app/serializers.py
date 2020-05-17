from rest_framework import serializers
from accounts.serializers import VendorSerializer
from accounts.models import Vendor
from .models import Menu, Order


class MenuSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)
    price = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    isRecurring = serializers.BooleanField(required=True)

# isRecurring
    def validate(self, data):
        # Check if there is isRecurring in the field passed # to allow update request without isRecurring field
        try: 
            # Confirm recurring and frequency of recurring
            if((data['isRecurring']==True and data['frequencyOfReoccurrence']!=0) or (data['isRecurring']==False and data['frequencyOfReoccurrence']==0)):
                return data
            else:
                raise serializers.ValidationError("Your isRecurring and frequencyOfReoccurrence fields are not in sync, check these fields again!!!")
        # This is for an update request as the required = True will not allow create request to go through
        except KeyError as e:
            return data

    class Meta:
        model = Menu
        fields = '__all__'
        read_only_fields = ['vendor','dateTimeCreated']


class OrderSerializer(serializers.ModelSerializer):
    # The menuId is used to get the id of menu from user, it's not one of the model fields
    menuId = serializers.IntegerField(required=True, write_only=True)
    menu = MenuSerializer(read_only=True)
    amountPaid = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    paymentStatus = serializers.BooleanField(required=True)

    def validate(self, data):
        # Check if there is paymentStatus and amountPaid in the field passed # to allow update request without paymentStatus and amountField field
        try:
            # Confirm payment status and amount paid
            if((data['paymentStatus']==True and data['amountPaid']!=0.00) or (data['paymentStatus']==False and data['amountPaid']==0.00)):
                return data
            else:
                raise serializers.ValidationError("Your payment status and amount paid are not in sync, check these fields again!!!")
        # This is for an update request as the required = True will not allow create request to go through
        except KeyError as e:
            return data

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['dateTimeCreated','orderStatus', 'vendor', 'customer']
