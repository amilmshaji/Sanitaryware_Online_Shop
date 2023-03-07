from django.urls import path
from . import views
from .views import InfoListView


urlpatterns = [
    path('', views.Home, name='home'),

    path('store/', views.store, name='store'),

    path('category/<slug:category_slug>/',
         views.store, name='products_by_category'),

    path('category/<slug:category_slug>/<slug:product_slug>/',
         views.product_detail, name='product_detail'),

    path('search/', views.search, name='search'),

    path('submit_review/<int:product_id>/',
         views.submit_review, name='submit_review'),
    path('view/', views.view, name='view'),
    path('main_view/', views.InfoListView, name='main-view'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('filter-products/', views.filter_products, name='filter-products'),

]