from django.urls import path

from shop_app import views
app_name='shop_app'
urlpatterns = [
    path('', views.Home, name='home'),

    path('allProdCat/',views.allProdCat,name='allProdCat'),

    path('<slug:c_slug>/',views.allProdCat,name='products_by_category'),
    path('<slug:c_slug>/<slug:product_slug>/', views.ProDetail, name='prodCatdetail')
]