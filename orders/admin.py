from django.contrib import admin

# Register your models here.
from orders.models import Payment, OrderPlaced

class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product',

        'quantity',

        'payment',
        'status',
        'amount',
        'is_ordered',
        'ordered_date',
    )

    # # This will help you to disbale add functionality
    # def has_add_permission(self, request):
    #     return False
    #
    #     # This will help you to disable delete functionaliyt
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False
    #
    #     # This will help you to disable change functionality
    #
    # def has_change_permission(self, request, obj=None):
    #     return False


admin.site.register(OrderPlaced, OrderProductAdmin)


