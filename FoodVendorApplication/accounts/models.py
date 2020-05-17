from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, active=False, admin=False, staff=False):
        if not email:
            raise ValueError("Users must have an email address")
        user_obj = self.model(email = self.normalize_email(email))
        # user_obj.set_password(password)
        user_obj.staff = staff
        user_obj.admin = admin
        user_obj.active = active
        user_obj.save(using=self._db)
        return user_obj

    def create_staff_user(self, email, password):
        user = self.create_user(email, password=password, staff=True)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password, staff=True, admin=True)
        return user

class Auth(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    phoneNumber = models.CharField(max_length=11)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    dateTimeCreated = models.DateTimeField(auto_now_add=True)

    # REQUIRED_FIELDS = ['phoneNumber','dateTimeCreated']
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.staff

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

class Vendor(models.Model):
    user = models.OneToOneField(Auth, on_delete=models.CASCADE, primary_key=True)
    businessName = models.CharField(max_length=255)

    def __str__(self):
        return self.user.email

class Customer(models.Model):
    user = models.OneToOneField(Auth, on_delete=models.CASCADE, primary_key=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    amountOutstanding = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.firstName