import decimal
from datetime import datetime
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import MenuSerializer, OrderSerializer
from .models import Menu, Order
# Create your views here.

# Menu API
class MenuViewSet(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuSerializer

    # Get all menus
    def get(self, request, format=None):
        menu = Menu.objects.all()
        serializer = MenuSerializer(menu, many=True)
        print(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Vendor create a menu
    def post(self, request, format=None):
        # Get the logged in user
        user = request.user
        serializer = self.serializer_class(data=request.data)
        # Check if the user is a vendor
        if hasattr(user, 'vendor'):
            if serializer.is_valid():
                # Create menu with users input
                menu = Menu.objects.create(
                    name=request.data.get('name'),
                    description=request.data.get('description'),
                    price=request.data.get('price'),
                    quantity=request.data.get('quantity'),
                    vendor=user.vendor,
                    isRecurring=bool(request.data.get('isRecurring')),
                    frequencyOfReoccurrence=request.data.get('frequencyOfReoccurrence')
                    # frequencyOfReoccurrence=request.data.get('frequencyOfReoccurrence') if bool(
                    #     request.data.get('isRecurring')) else 0
                )
                menu.save()
                return Response(MenuSerializer(menu).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You are not authorized to create a menu", status=status.HTTP_401_UNAUTHORIZED)

    # Vendor Update a menu with the input id
    def patch(self, request, pk, format=None):
        # pk = request.data.get('id')
        try:
            # Get the menu with the given id
            menu = Menu.objects.get(id=pk)
            serializer = MenuSerializer(menu, data=request.data, partial=True)
            # Get the logged in user
            user = request.user
            # Check if the logged in user is a vendor and the owner of the menu
            if (hasattr(user, 'vendor') and (user.email == menu.vendor.user.email)):
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("You are not authorized to edit this menu", status=status.HTTP_401_UNAUTHORIZED)
        except Menu.DoesNotExist:
            return Response("There's no menu with an id of {}".format(pk), status=status.HTTP_400_BAD_REQUEST)

    # Vendor Delete a menu with the input id
    def delete(self, request, pk, format=None):
        # pk = request.data.get('id')
        try:
            menu = Menu.objects.get(id=pk)
            # Get the logged in user
            user = request.user
            # Check if the logged in user is a vendor and the owner of the menu
            if (hasattr(user, 'vendor') and (user.email == menu.vendor.user.email)):
                menu.delete()
                return Response("Menu with id of {} deleted successfully".format(pk), status=status.HTTP_200_OK)
            else:
                return Response("You are not authorized to edit this menu", status=status.HTTP_401_UNAUTHORIZED)
        except Menu.DoesNotExist:
            return Response("There's no menu with an id of {}".format(pk), status=status.HTTP_400_BAD_REQUEST)

# ORDER API
class OrderViewSet(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    # Get all order
    def get(self, request, format=None):
        order = Order.objects.all()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # create an order
    # Purchase or preorder food
    def post(self, request, format=None):
        # Get the logged in user
        user = request.user
        serializer = self.serializer_class(data=request.data)
        # Check if the user is a vendor
        if hasattr(user, 'customer'):
            if serializer.is_valid():
                # Create order with users input
                # print(request.data.get('name'))
                menuId = request.data.get('menuId')
                try:
                    menu = Menu.objects.get(id=menuId)
                    amountPaid = request.data.get('amountPaid')
                    # paymentStatus = request.data.get('paymentStatus')
                    order = Order.objects.create(
                        customer=user.customer,
                        menu=menu,
                        vendor=menu.vendor,
                        amountDue=menu.price,
                        amountPaid=amountPaid,
                        description=request.data.get('description'),
                        amountOutstanding = menu.price - decimal.Decimal(amountPaid),
                        paymentStatus = request.data.get('paymentStatus')
                    )
                    order.save()
                    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
                except Menu.DoesNotExist:
                    return Response("There's no menu with an id of {}".format(menuId), status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You are not authorized to create an order", status=status.HTTP_401_UNAUTHORIZED)

    # Customer Update an order with the input id
    def patch(self, request, pk, format=None):
        # pk = request.data.get('id')
        try:
            # Get the order with the given id
            order = Order.objects.get(id=pk)
            serializer = OrderSerializer(order, data=request.data, partial=True)
            # Get the logged in user
            user = request.user
            # Check if the logged in user is a customer and the owner of the menu
            if (hasattr(user, 'customer') and (user.email == order.customer.user.email)):
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("You are not authorized to edit this menu", status=status.HTTP_401_UNAUTHORIZED)
        except Menu.DoesNotExist:
            return Response("There's no menu with an id of {}".format(pk), status=status.HTTP_400_BAD_REQUEST)

    # Customer Delete an order with the input id
    def delete(self, request, pk, format=None):
        # pk = request.data.get('id')
        try:
            order = Order.objects.get(id=pk)
            # Get the logged in user
            user = request.user
            # Check if the logged in user is a vendor and the owner of the menu
            if (hasattr(user, 'customer') and (user.email == order.customer.user.email)):
                order.delete()
                return Response("Order with id of {} deleted successfully".format(pk), status=status.HTTP_200_OK)
            else:
                return Response("You are not authorized to delete this order", status=status.HTTP_401_UNAUTHORIZED)
        except Order.DoesNotExist:
            return Response("There's no order with an id of {}".format(pk), status=status.HTTP_400_BAD_REQUEST)

# Customer Cancel Order
class CancelOrderViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        # pk = request.data.get('id')
        try:
            order = Order.objects.get(id=pk)
            # Get the logged in user
            user = request.user
            # Check if the logged in user is a cutomer and the owner of the order
            if (hasattr(user, 'customer') and (user.email == order.customer.user.email)):
                # Check if the Order status is done
                if order.orderStatus == Order.ORDER_STATUS[1][0]:
                    return Response('Sorry, the order is done thus cannot be canceled', status=status.HTTP_200_OK)
                else:
                    # Set order status to cancelled
                    # todaysDate = datetime.now().date()
                    # todayOrder = Order.objects.get(dateAndTimeOfOrder.date()=todaysDate)
                    # print(todayOrder)
                    order.orderStatus = Order.ORDER_STATUS[2][0]
                    order.save()
                    return Response('Order cancelled successfully')
            else:
                return Response("You are not authorized to cancel this order", status=status.HTTP_401_UNAUTHORIZED)
        except Order.DoesNotExist:
            return Response("There's no order with an id of {}".format(pk), status=status.HTTP_400_BAD_REQUEST)

# Vendor update order status
class UpdateOrderStatusViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        # pk = request.data.get('id')
        try:
            order = Order.objects.get(id=pk)
            # Get the logged in user
            user = request.user
            # Check if the logged in user is a vendor and the owner of the order
            if (hasattr(user, 'vendor') and (user.email == order.vendor.user.email)):
                # Check if the Order status is cancelled
                if order.orderStatus == Order.ORDER_STATUS[2][0]:
                    return Response('Sorry, the order has been cancelled by the customer', status=status.HTTP_200_OK)
                else:
                    # Set order status to done
                    order.OrderStatus = Order.ORDER_STATUS[1][0]
                    order.save()
                    return Response('Order updated successfully')
            else:
                return Response("You are not authorized to update this order", status=status.HTTP_401_UNAUTHORIZED)
        except Order.DoesNotExist:
            return Response("There's no order with an id of {}".format(pk), status=status.HTTP_400_BAD_REQUEST)

# Generate daily report of sales

class SalesReportViewSet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):
        user = request.user
        # Check if the logged in user is a vendor and the owner of the order
        if (hasattr(user, 'vendor') and (user.email == order.vendor.user.email)):
            pass
            # print(order.dateAndTimeOfOrder.date())
            # print(datetime.now().date())
            # todaysDate = datetime.now().date()
            # todayOrder = Order.objects.get(dateAndTimeOfOrder.date()=todaysDate)
            # print(todayOrder)
            # date = date
        else:
            return Response("You are not authorized to generate a daily report", status=status.HTTP_401_UNAUTHORIZED)
# send notifications to the customer on available menu or debts,

# order progress and other relevant information