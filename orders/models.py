from accounts.models import Account, Address_Book
from django.db import models

# Create your models here.
from shop_app.models import Product




class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.FloatField(blank=True,null=True)
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Address_Book,on_delete=models.SET_NULL, null=True,default=1)

    paid = models.BooleanField(default=False)


    def __str__(self):
        return self.customer.fname



class OrderPlaced(models.Model):
    MONTH_CHOICES = (
        (1, 'January'),
        (2, 'February'),
        (3, 'March'),
        (4, 'April'),
        (5, 'May'),
        (6, 'June'),
        (7, 'July'),
        (8, 'August'),
        (9, 'September'),
        (10, 'October'),
        (11, 'November'),
        (12, 'December'),
    )
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),

    )
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Address_Book,on_delete=models.SET_NULL, null=True,default=1)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    ordered_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_cost(self):
        return self.quantity

    def __str__(self):
        return self.customer.fname

    def amount(self):
        amountt = self.payment.amount
        return amountt

