from django.urls import path
from . import views

urlpatterns = [
    path('myprofile/', views.dashboard, name='myprofile'),
    path('editprofile/', views.editprofile, name='edit_profile'),
    path('changePassword/', views.changePassword, name='changePassword'),
    path('addressbook/', views.addressbook, name='addressbook'),
    path('addressadd/', views.addressadd, name='addressadd'),

    path('addressedit/<int:address_id>/', views.addressedit, name='addressedit'),

    path('address_set/<int:address_id>/', views.address_set, name='address_set'),
    path('my_orders/', views.my_orders, name='my_orders'),

]