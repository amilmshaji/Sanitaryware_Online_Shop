from django.contrib import admin

# Register your models here.
from variations.models import Color, Brand, Design, Dimensions

admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Design)

admin.site.register(Dimensions)
