from django.urls import include, path

# from rest_framework import routers
from app.views import MenuViewSet, OrderViewSet, CancelOrderViewSet, UpdateOrderStatusViewSet, SalesReportViewSet, NotificationViewSet

# router = routers.DefaultRouter()
# router.register('order', OrderViewSet)
# router.register('vendor', VendorViewSet)
# router.register('password', SetPassword)

urlpatterns = [
    path('menu/', MenuViewSet.as_view(), name='menu'),
    path('menu/<int:pk>/', MenuViewSet.as_view(), name='edit-menu'),
    path('order/', OrderViewSet.as_view(), name='order'),
    path('order/<int:pk>/', OrderViewSet.as_view(), name='edit-order'),
    path('order/<int:pk>/cancel/', CancelOrderViewSet.as_view(), name='cancel-order'),
    path('order/<int:pk>/update/', UpdateOrderStatusViewSet.as_view(), name='update-order'),
    path('sales/report/', SalesReportViewSet.as_view(), name='sales-report'),
    path('notification/users/<int:pk>/', NotificationViewSet.as_view(), name='customers-notification')
]
