from django.contrib import admin
from django.db import models
from .models import Product, Variation, ReviewRating, Productgallery, Product_Display, Color, Brand, Design, Info
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

from django.utils import timezone

class ProductAdmin(admin.ModelAdmin):
    # ...

    list_filter = (
        ('created_date', admin.DateFieldListFilter),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        today = timezone.now().date()
        yesterday = today - timezone.timedelta(days=1)
        last_month = today - timezone.timedelta(days=30)

        if request.GET.get('date_filter') == 'today':
            return qs.filter(created_date=today)
        elif request.GET.get('date_filter') == 'yesterday':
            return qs.filter(created_date=yesterday)
        elif request.GET.get('date_filter') == 'last_month':
            return qs.filter(created_date__gte=last_month, created_date__lte=today)
        else:
            return qs

    def changelist_view(self, request, extra_context=None):
        if request.GET.get('date_filter'):
            self.list_display = (
                'thumbnail_preview',
                'product_name',
                'price',
                'stock',
                'category',
                'is_available',
                'is_featured',
                'created_date',
            )
            self.list_filter = ()
        else:
            self.list_display = (
                'thumbnail_preview',
                'product_name',
                'price',
                'stock',
                'category',
                'is_available',
                'is_featured',
            )
            self.list_filter = (
                ('created_date', admin.DateFieldListFilter),
            )

        return super().changelist_view(request, extra_context=extra_context)

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


admin.site.register(Product, ProductAdmin)



class RatingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product',
        'review',
        'rating',
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

admin.site.register(Info)
