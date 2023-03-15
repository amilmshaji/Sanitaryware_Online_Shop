from django.urls import path
from . import views

urlpatterns = [

    path('recommendations/', views.recommend_products, name='recommendations'),

]