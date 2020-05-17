from django.db import models
from django.contrib.postgres.fields import ArrayField

from accounts.models import Vendor, Customer

# Create your models here.


class Menu(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField()
    dateTimeCreated = models.DateTimeField(auto_now_add=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    isRecurring = models.BooleanField(default=False)
    frequencyOfReoccurrence = models.IntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    ORDER_STATUS = (
        ('In-Progress', 'In-Progress'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled')
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    description = models.TextField()
    amountDue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amountPaid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amountOutstanding = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    orderStatus = models.CharField(max_length=250, choices=ORDER_STATUS, default='In-Progress')
    # A boolean field to show paid or pre-paid
    paymentStatus = models.BooleanField()
    dateAndTimeOfOrder = models.DateTimeField(auto_now_add=True)

# class Notification(models.Model):
#     vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, primary_key=True)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, primary_key=True)
#     message = models.TextField()
#     dateTimeCreated = models.DateTimeField(auto_now_add=True)
