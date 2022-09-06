from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
import datetime


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, fname, lname, email, city,state, district, role, phone_number, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not fname:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            lname=lname,
            city=city,
            state=state,
            district=district,
            phone_number=phone_number,
            role=role,
            fname=fname,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user
#
#     def create_superuser(self, name, email, username, password, district=None, phone_number=None, role=None,
#                          mun_name=None, state=None):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             username=username,
#             password=password,
#             name=name,
#             mun_name=mun_name,
#             state=state,
#             district=district,
#             phone_number=phone_number,
#             role=role,
#
#         )
#         user.is_admin = True
#         user.is_active = True
#         user.is_staff = True
#         user.is_superadmin = True
#         user.save(using=self._db)
#         return user


class Account(AbstractBaseUser):
    state_choices = (('kerala', 'kerala'), ('demo', 'demo'))
    district_choices = (
        ('Kozhikode', 'Kozhikode'),
        ('Malappuram', 'Malappuram'),
        ('Kannur', 'Kannur'),
        ('Trivandrum', 'Trivandrum'),
        ('Palakkad', 'Palakkad'),
        ('Thrissur', 'Thrissur'),
        ('Kottayam', 'Kottayam'),
        ('Alappuzha', 'Alappuzha'),
        ('Idukki', 'Idukki'),
        ('Kollam', 'Kollam'),
        ('Ernakulam', 'Ernakulam'),
        ('Wayanad', 'Wayanad'),
        ('Kasaragod', 'Kasaragod'),
        ('Pathanamthitta', 'Pathanamthitta')
    )
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100, blank=True, null=True)
    lname = models.CharField(max_length=100, blank=True, null=True)
    # username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.BigIntegerField(default=0)
    city = models.CharField(max_length=50,)

    state = models.CharField(max_length=50, choices=state_choices)
    district = models.CharField(max_length=50, choices=district_choices)
    # mun_name = models.CharField(max_length=100, blank=True, null=True)
    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname','city', 'district', 'state', 'phone_number']

    # objects = MyAccountManager()

    # def full_name(self):
    #     return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     return self.is_admin
    #
    # def has_module_perms(self, add_label):
    #     return True
