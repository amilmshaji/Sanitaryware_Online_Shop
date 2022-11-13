from django.contrib import admin
from django.db import models
from .models import Product, Variation, ReviewRating, Productgallery, Product_Display, Color, Brand, Design
import admin_thumbnails

from .models import Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('category_name',)
    }
    list_display = (
        'category_name','thumbnail_preview',

    )

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Image Preview'
    thumbnail_preview.allow_tags = True


admin.site.register(Category, CategoryAdmin)


# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model=Productgallery
    extra=1

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'thumbnail_preview',
        'product_name',
        'price',
        'stock',
        'category',
        'is_available',
        'is_featured',


    )

    list_editable = ['price','stock','is_available','is_featured',]


    prepopulated_fields = {'slug': ('product_name',)}
    inlines=[ProductGalleryInline]

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Image Preview'
    thumbnail_preview.allow_tags = True


class VariationAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'color',
        'brand',
        'design',
        'is_active',
    )
    list_editable = (
        'is_active',

    )
    list_filter = (
        'product',
        'color',
        'brand',
        'design',
        'is_active',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)



class RatingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product',
        'review',
        'created_at',


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

admin.site.register(ReviewRating, RatingAdmin)

admin.site.register(Product_Display)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Design)







