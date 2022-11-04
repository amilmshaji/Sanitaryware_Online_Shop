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
# admin.site.register(Variation, VariationAdmin)



class RatingAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'user',
        'review',
        'created_at',


    )


admin.site.register(ReviewRating, RatingAdmin)
