from django.db import models
from django.utils.html import mark_safe



from django.urls.base import reverse
from accounts.models import Account
from django.db.models import Aggregate, Avg, Count
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    @property
    def thumbnail_preview(self):
        if self.cat_image:
            return mark_safe('<img src="{}" width="100" height="100" />'.format(self.cat_image.url))
        return ""

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name  #shows the name

class Color(models.Model):
    color = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.color

class Brand(models.Model):
    brand = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.brand

class Design(models.Model):
    design = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.design

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/product')
    display = models.ImageField(upload_to='photos/display',default="a3.png")
    stock = models.IntegerField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE,null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE,null=True, blank=True)
    design = models.ForeignKey(Design, on_delete=models.CASCADE,null=True, blank=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    @property
    def thumbnail_preview(self):
        if self.images:
            return mark_safe('<img src="{}" width="100" height="100" />'.format(self.images.url))
        return ""

    def averageReview(self):
        reviews = ReviewRating.objects.filter(
            product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(
            product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)



class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    variation_category = models.CharField(
        max_length=100, choices=variation_category_choice, blank=True)
    variation_value = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value
#
#
# class Color(models.Model):
#     color = models.CharField(max_length=100,null=True, blank=True)
#
#     def __str__(self):
#         return self.color
#
# class Brand(models.Model):
#     brand = models.CharField(max_length=100,null=True, blank=True)
#
#     def __str__(self):
#         return self.brand
#
# class Design(models.Model):
#     design = models.CharField(max_length=100,null=True, blank=True)
#
#     def __str__(self):
#         return self.design
#
#
#
# class Variation(models.Model):
#     id = models.AutoField(primary_key=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     color = models.ForeignKey(Color, on_delete=models.CASCADE,null=True, blank=True)
#     brand = models.ForeignKey(Brand, on_delete=models.CASCADE,null=True, blank=True)
#     design = models.ForeignKey(Design, on_delete=models.CASCADE,null=True, blank=True)
#
#     is_active = models.BooleanField(default=True)
#     created_date = models.DateField(auto_now_add=True)
#
#     objects = VariationManager()
#
#     def __str__(self):
#         return str(self.product)


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,editable=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE,editable=False)
    review = models.TextField(max_length=500, blank=True,)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True,editable=False)
    status = models.BooleanField(default=True,editable=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.product)






class Productgallery(models.Model):
    product=models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name='Product Gallery'
        verbose_name_plural='Product gallery'


from django_resized import ResizedImageField



class Product_Display(models.Model):
    user = models. OneToOneField(Account, on_delete=models.CASCADE,null=True,editable=False,unique=True)

    images = ResizedImageField(upload_to='view/photos',null=True, blank=True)
