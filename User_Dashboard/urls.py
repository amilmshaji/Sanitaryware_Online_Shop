from django.urls import path
from . import views

urlpatterns = [
    path('myprofile/', views.dashboard, name='myprofile'),
    path('editprofile/', views.editprofile, name='editprofile'),
]