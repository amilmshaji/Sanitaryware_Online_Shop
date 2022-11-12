
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


# Create your models here.
from django.urls import reverse


class MyAccountManager(BaseUserManager):
    def create_user(self, fname, lname, email,phone_number, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not lname:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
                        lname=lname,
                        fname=fname,
                        phone_number=phone_number,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fname, email, lname, password,  phone_number,):
        user = self.create_user(
            email=self.normalize_email(email),
            fname=fname,
            password=password,
            lname=lname,
            phone_number=phone_number,

        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100, blank=True, null=True, editable=False)
    lname = models.CharField(max_length=100, blank=True, null=True, editable=False)
    email = models.EmailField(max_length=100, unique=True, editable=False)
    phone_number = models.BigIntegerField(default=0, editable=False)



    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname',  'phone_number',]

    objects = MyAccountManager()


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    # def get_url(self):
    #     return reverse('profile', args=[self.fname])


class Address_Book(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100, blank=True, null=True, editable=False)
    lname = models.CharField(max_length=100, blank=True, null=True, editable=False)
    phone_number = models.BigIntegerField(default=0, editable=False)
    house = models.CharField(blank=True, max_length=100,null=True)
    street = models.CharField(blank=True, max_length=20,null=True)
    city = models.CharField(blank=True, max_length=20,null=True)
    state = models.CharField(blank=True, max_length=20,null=True)
    pin = models.IntegerField(blank=True,null=True)
    status = models.BooleanField(default=False)


    def __str__(self):
        return self.user.fname

    def full_address(self):
        return f'{self.house} {self.street}'

