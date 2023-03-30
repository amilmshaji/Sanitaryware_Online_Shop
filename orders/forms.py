from django import forms

from shop_app.models import Product


class ProductStockUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['stock']
        widgets = {
            'stock': forms.NumberInput(attrs={'class': 'form-control'})
        }
