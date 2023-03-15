from django.shortcuts import render

from shop_app.models import Product, ReviewRating
from .models import SearchHistory
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

from django.shortcuts import render
def recommend_products(request):
    # Get the user's search history
    search_history = SearchHistory.objects.filter(user=request.user)

    # Extract the keywords used in the search history
    keywords = [search.query for search in search_history]

    # Find other users who have searched for similar keywords
    similar_search_history = SearchHistory.objects.filter(query__in=keywords)
    print(similar_search_history)

    # Extract the distinct keywords from similar search history
    similar_keywords = similar_search_history.values_list('query', flat=True).distinct()
    print(similar_keywords)

    # Retrieve the product recommendations based on the similar keywords
    recommended_products = Product.objects.filter(Q(category__category_name__in=similar_keywords)).distinct()
    print(recommended_products)

    context = {
        'recommended_products': recommended_products,
    }
    return render(request, 'recommendations.html', context)
