from . import views
from django.urls import path

urlpatterns = [
    path('contact/', views.Contact, name='contact'),
    path('login/', views.login, name='login'),
    path('category/', views.Category, name='category'),
    path('blog/', views.Blog, name='blog'),
    path('checkout/', views.Checkout, name='checkout'),
    path('wishlist/', views.wishlist, name='wishlist'),

    path('register/', views.register, name='register'),
    path('logout', views.logout, name='logout'),

]
