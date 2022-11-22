from django.db import models

# Create your models here.
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

class Dimensions(models.Model):
    dimensions = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return self.dimensions