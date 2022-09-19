from django.db import models

# Create your models here.
from django.urls import reverse

#category table
class Category(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    description=models.TextField(blank=True)
    image=models.ImageField(upload_to='category',blank=True)

    class Meta:
        ordering=('name',)
        verbose_name='category'
        verbose_name_plural='categories'

    def get_url(self):
        return reverse('shop:products_by_category',args=[self.slug])

    def __str__(self):
        return '{}'.format(self.name)

# #table determining product of all table
# class brand(Category):
#     pass
#
# #table determining product of all table
# class color(Category):
#     pass
#
# #product table which contains all the details
#
# class Product(models.Model):
#     name=models.CharField(max_length=250,unique=True)
#     slug = models.SlugField(max_length=250, unique=True)
#     description = models.TextField(blank=True)
#     price=models.DecimalField(max_digits=10,decimal_places=2)
#     category=models.ForeignKey(Category,on_delete=models.CASCADE)
#     image1=models.ImageField(upload_to='products',blank=True)
#     image2 = models.ImageField(upload_to='products', null=False)
#     stock=models.IntegerField()
#     available=models.BooleanField(default=True)
#     color = models.ForeignKey(color, on_delete=models.CASCADE)
#     discount = models.IntegerField(default=0)
#     brand = models.ForeignKey(brand, on_delete=models.CASCADE)
#     created=models.DateTimeField(auto_now_add=True)
#     updated=models.DateTimeField(auto_now=True)
#
#     def get_url(self):
#         return reverse('shop:prodCatdetail',args=[self.category.slug,self.slug])
#
#     class Meta:
#         ordering=('name',)
#         verbose_name='product'
#         verbose_name_plural='products'
#
#     def __str__(self):
#         return '{}'.format(self.name)