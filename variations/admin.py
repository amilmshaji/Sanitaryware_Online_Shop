from django.contrib import admin

# Register your models here.
from variations.models import Color, Brand, Design, Dimensions, Brand_Company

admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Design)

admin.site.register(Dimensions)
# admin.site.register(Brand_Company)
