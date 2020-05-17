from django.urls import include, path

from rest_framework import routers
from accounts.views import CustomerViewSet, VendorViewSet, SetPassword, CustomerLogin, VendorLogin, LogoutUser

router = routers.DefaultRouter()
router.register('customers', CustomerViewSet)
router.register('vendors', VendorViewSet)
# router.register('password', SetPassword)

urlpatterns = [
    path('', include(router.urls)),
    path('password', SetPassword.as_view(), name='password'),
    path('customer/login', CustomerLogin.as_view(), name='customer-login'),
    path('vendor/login', VendorLogin.as_view(), name='vendor-login'),
    path('logout', LogoutUser.as_view(), name='logout')
]
