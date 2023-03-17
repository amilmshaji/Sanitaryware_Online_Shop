from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.checkout, name='orders'),
    path('pdf/<int:id>/', views.get,name='pdf'),

    #sales url
    # path('products_sold_by_month/', views.products_sold_by_month, name='products_sold_by_month'),
    path('product-sales/', views.product_sales, name='product_sales'),

]