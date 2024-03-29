# from django.contrib import admin
#
# from .models import Account
#
# admin.site.register(Account)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from shop_app.models import Color, Brand, Design
from .models import Account, Address_Book
from django.utils.html import format_html

import decimal, csv
from django.http import HttpResponse
from django.db.models import F
# Register your models here.




class AccountAdmin(UserAdmin):
    exclude =('password','Groups')

    list_display = (
        'email', 'fname', 'lname', 'last_login', 'is_active', 'date_joined'
    )
    list_editable = ['is_active']

    list_display_links = (
        'email', 'fname', 'lname',
    )
    readonly_fields = (
        'last_login', 'date_joined',
    )
    ordering = (
        '-date_joined',
    )
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    # This will help you to disbale add functionality
    def has_add_permission(self, request):
        return False

        # This will help you to disable delete functionaliyt

    def has_delete_permission(self, request, obj=None):
        return False

        # This will help you to disable change functionality

    def has_change_permission(self, request, obj=None):
        return False



admin.site.register(Account, AccountAdmin)

class Address_BookAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'fname',
        'lname',
        'phone_number',
        'house',
        'street',
        'city',
        'state',
        'pin',



    )
    # This will help you to disbale add functionality
    def has_add_permission(self, request):
        return False

        # This will help you to disable delete functionaliyt

    def has_delete_permission(self, request, obj=None):
        return False

        # This will help you to disable change functionality

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Address_Book, Address_BookAdmin)



