from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.checkout, name='orders'),
    path('pdf/<int:id>/', views.get,name='pdf'),
]