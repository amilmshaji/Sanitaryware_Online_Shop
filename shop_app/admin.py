from django.contrib import admin
from django.db import models
from .models import Product, Variation, ReviewRating, Productgallery
import admin_thumbnails

from .models import Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('category_name',)
    }
    list_display = (
        'category_name', 'slug',
    )


admin.site.register(Category, CategoryAdmin)


# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model=Productgallery
    extra=1

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_name',
        'price',
        'stock',
        'category',
        'created_date',
        'modified_date',
        'is_available',
    )
    prepopulated_fields = {'slug': ('product_name',)}
    inlines=[ProductGalleryInline]


class VariationAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'variation_category',
        'variation_value',
        'is_active',
    )
    list_editable = (
        'is_active',

    )
    list_filter = (
        'product',
        'variation_category',
        'variation_value',
        'is_active',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(Productgallery)