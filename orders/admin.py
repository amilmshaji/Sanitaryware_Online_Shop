from django.contrib import admin

# Register your models here.
from orders.models import Payment, OrderPlaced

admin.site.register(Payment)

admin.site.register(OrderPlaced)