
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,username, fname, lname, email,phone_number, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not lname:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
                        lname=lname,
                        fname=fname,
                        username=username,
                        phone_number=phone_number,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fname, email, lname, password, username=None, phone_number=None,):
        user = self.create_user(
            email=self.normalize_email(email),
            fname=fname,
            password=password,
            lname=lname,
            username=username,
            phone_number=phone_number,

        )
        user.is_admin = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100, blank=True, null=True)
    lname = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.BigIntegerField(default=0)
    username = models.CharField(max_length=100, unique=True)



    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname', 'username',  'phone_number',]

    objects = MyAccountManager()

    def __str__(self):
        return self.email


    def has_module_perms(self, add_label):
        return True
from django.db import models
#
# # Create your models here.
from django.db import models

#Customer Registration Table
class reg_user(models.Model):
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100, blank=True, null=True)
    lname = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.BigIntegerField(default=0)
    username = models.CharField(max_length=100, unique=True)



    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

#Login Table
class log_user(models.Model):
     email= models.CharField(max_length=200,primary_key=True,unique=True)
     password = models.CharField(max_length=200)
