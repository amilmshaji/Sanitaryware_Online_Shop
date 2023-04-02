from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class Color(models.Model):
    color = models.CharField(max_length=100,null=True, blank=True,unique=True)

    def save(self, *args, **kwargs):
        self.color = self.color.lower()
        super(Color, self).save(*args, **kwargs)

    def clean(self):
        # Check if a brand with the same name already exists (case-insensitive)
        existing_colors = Color.objects.filter(color__iexact=self.color).exclude(id=self.id)
        if existing_colors.exists():
            raise ValidationError('A colour with this name already exists.')

    def __str__(self):
        return self.color.capitalize()


class Brand(models.Model):
    brand = models.CharField(max_length=100, null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.brand = self.brand.lower()
        super(Brand, self).save(*args, **kwargs)

    def clean(self):
        # Check if a brand with the same name already exists (case-insensitive)
        existing_brands = Brand.objects.filter(brand__iexact=self.brand).exclude(id=self.id)
        if existing_brands.exists():
            raise ValidationError('A brand with this name already exists.')

    def __str__(self):
        return self.brand.capitalize()


class Design(models.Model):
    design = models.CharField(max_length=100,null=True, blank=True,unique=True)

    def save(self, *args, **kwargs):
        self.design = self.design.lower()
        super(Design, self).save(*args, **kwargs)

    def clean(self):
        # Check if a Design with the same name already exists (case-insensitive)
        existing_design = Design.objects.filter(design__iexact=self.design).exclude(id=self.id)
        if existing_design.exists():
            raise ValidationError('A design with this name already exists.')

    def __str__(self):
        return self.design.capitalize()

class Dimensions(models.Model):
    dimensions = models.CharField(max_length=100,null=True, blank=True,unique=True)

    def save(self, *args, **kwargs):
        self.dimensions = self.dimensions.lower()
        super(Dimensions, self).save(*args, **kwargs)

    def clean(self):
        # Check if a dimensions with the same name already exists (case-insensitive)
        existing_dimensions = Dimensions.objects.filter(dimensions__iexact=self.dimensions).exclude(id=self.id)
        if existing_dimensions.exists():
            raise ValidationError('A dimensions with this name already exists.')

    def __str__(self):
        return self.dimensions.capitalize()


class Brand_Company(models.Model):
    brand = models.CharField(max_length=100,null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.brand