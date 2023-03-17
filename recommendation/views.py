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


# import joblib
#
# def recommend_products(request):
#     # Get the user's search history
#     search_history = SearchHistory.objects.filter(user=request.user)
#
#     # Extract the keywords used in the search history
#     keywords = [search.query for search in search_history]
#
#     # Find other users who have searched for similar keywords
#     similar_search_history = SearchHistory.objects.filter(query__in=keywords)
#
#     # Extract the distinct keywords from similar search history
#     similar_keywords = similar_search_history.values_list('query', flat=True).distinct()
#
#     # Retrieve the product recommendations based on the similar keywords
#     products = Product.objects.filter(Q(category__category_name__in=similar_keywords)).distinct()
#
#     # Load the random forest model
#     model = joblib.load('path/to/random_forest_model.pkl')
#
#     # Prepare the data for the model
#     product_ids = [product.id for product in products]
#     product_features = Product.objects.filter(product__id__in=product_ids)
#     product_feature_dict = {}
#     for feature in product_features:
#         if feature.product_id not in product_feature_dict:
#             product_feature_dict[feature.product_id] = []
#         product_feature_dict[feature.product_id].append(feature.value)
#     product_feature_list = [product_feature_dict[product_id] for product_id in product_ids]
#
#     # Make predictions using the model
#     predicted_scores = model.predict(product_feature_list)
#
#     # Sort the products by their predicted scores
#     product_scores = list(zip(products, predicted_scores))
#     product_scores.sort(key=lambda x: x[1], reverse=True)
#
#     # Create a list of recommended products
#     recommended_products = [product for product, score in product_scores[:10]]
#
#     context = {
#         'recommended_products': recommended_products,
#     }
#     return render(request, 'recommendations.html', context)