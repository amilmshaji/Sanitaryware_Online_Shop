from . import views
from django.urls import path

urlpatterns = [
    path('', views.Home, name='home'),
    path('contact/', views.Contact, name='contact'),
    path('login/', views.Login, name='login'),
    path('category/', views.Category, name='category'),
    path('blog/', views.Blog, name='blog'),
    path('checkout/', views.Checkout, name='checkout'),
    path('cart/', views.Cart, name='cart'),
    path('register/', views.Register, name='register'),
]
