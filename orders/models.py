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



# class Order(models.Model):
#     STATUS = (
#         ('New', 'New'),
#         ('Accepted', 'Accepted'),
#         ('Completed', 'Completed'),
#         ('Cancelled', 'Cancelled'),
#
#     )
#     user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
#     payment = models.ForeignKey(
#         Payment, on_delete=models.SET_NULL, null=True, blank=True)
#     order_number = models.CharField(max_length=20)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     phone = models.CharField(max_length=15)
#     email = models.EmailField(max_length=50)
#     address_line_1 = models.CharField(max_length=50)
#     address_line_2 = models.CharField(max_length=50, blank=True)
#     country = models.CharField(max_length=50)
#     state = models.CharField(max_length=50)
#     city = models.CharField(max_length=50)
#     order_note = models.CharField(max_length=100, blank=True)
#     order_total = models.FloatField()
#     tax = models.FloatField()
#     status = models.CharField(max_length=10, choices=STATUS, default='New')
#     ip = models.CharField(blank=True, max_length=20)
#     is_ordered = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def full_name(self):
#         return f'{self.first_name} {self.last_name}'
#
#     def full_address(self):
#         return f'{self.address_line_1} {self.address_line_2}'
#
#     def __str__(self):
#         return self.first_name
#
#
# class OrderProduct(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     payment = models.ForeignKey(
#         Payment, on_delete=models.SET_NULL, blank=True, null=True)
#     user = models.ForeignKey(Account, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     product_price = models.FloatField()
#     ordered = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.product.product_name
