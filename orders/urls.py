from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.checkout, name='orders'),
    path('pdf/<int:id>/', views.get,name='pdf'),

    #sales url
    path('sales-report/', views.sales_report, name='sales_report'),
    path('product-sales/', views.product_sales, name='product_sales'),
    path('product-saless/<int:id>/', views.product_saless, name='product_saless'),


    path('low-stock/', views.low_stock_products, name='low_stock_products'),
    path('update_stock/<int:pk>/', views.update_stock, name='update_stock'),
    path('generate_low_stock_pdf/', views.generate_low_stock_pdf, name='generate_low_stock_pdf'),

]