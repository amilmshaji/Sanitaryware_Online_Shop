from django.contrib.auth.decorators import login_required
from django.core.checks import messages

from recommendation.models import SearchHistory
from variations.models import Color, Brand
from .forms import ReviewForm
from .models import Category, Product_Display, Info
from django.shortcuts import get_object_or_404, redirect, render
from . models import Product, ReviewRating, Productgallery
from cart.models import CartItem, Cart
from cart.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages

# Python program to move the image
# with the mouse




# Create your views here.
@login_required(login_url='login')
def Home(request,category_slug=None):
    categories = None
    products = None


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


    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True,is_featured=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:

        products = Product.objects.all().filter(is_available=True,is_featured=True).order_by('id')
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'recommended_products': recommended_products,

    }
    return render(request, 'index.html', context)

def store(request, category_slug=None):
    categories = None
    products = None
    colors = Color.objects.all()
    brands = Brand.objects.all()
    cat=Category.objects.all()

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True)
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:

        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'cat': cat,
        'colors': colors,
        'brands': brands,
    }
    return render(request, 'shop.html', context)

@login_required(login_url='login')
def filter_products(request):
    category = request.GET.get('category')
    color = request.GET.get('color')
    brand = request.GET.get('brand')


    products = Product.objects.filter(
        category__slug=category,
        color__slug=color,
        brand__slug=brand,

        is_available=True
    )

    data = []
    for product in products:
        data.append({
            'id': product.id,
            'name': product.product_name,
            'description': product.description,

            'image': product.images.url
        })

    return JsonResponse({'products': data})

def product_detail(request,  category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(
            request), product=single_product).exists()
        # return HttpResponse(in_cart)
        # exit()
    except Exception as e:
        raise e
    # if request.user.is_authenticated:
    #
    #     try:
    #         orderproduct = OrderProduct.objects.filter(
    #             user=request.user, product_id=single_product.id).exists()
    #     except OrderProduct.DoesNotExist:
    #         orderproduct = None
    # else:
    #     orderproduct = None

    reviews = ReviewRating.objects.filter(
        product_id=single_product.id, status=True)

    product_gallery=Productgallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        # 'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery':product_gallery,
    }
    return render(request, 'product-detail-variable.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        key=SearchHistory(query=keyword,user=request.user)
        key.save()
        if keyword:
            products = Product.objects.order_by(
                'created_date').filter(Q(category__category_name__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'shop.html', context)
from django.http import JsonResponse
from django.db.models import Q

def search_suggestions(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(category__category_name__icontains=keyword) | Q(product_name__icontains=keyword))
            suggestions = []
            for product in products:
                suggestion = {
                    'name': product.product_name,
                    'url': product.get_url()
                }
                suggestions.append(suggestion)
            return JsonResponse(suggestions, safe=False)
    return JsonResponse([], safe=False)


from django.views.generic import ListView
import json

class InfoListView(ListView):
    model = Info
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["qs_json"] = json.dumps(list(Info.objects.values()))
        return context


@login_required(login_url='login')
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:

            reviews = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you ! Your Review is Updated')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']



                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(
                    request, 'Thank You ! Your Review Has Been Submitted')
                return redirect(url)


def view(request):
    url = request.META.get('HTTP_REFERER')
    other_exist=Product_Display.objects.filter(user=request.user).exists()
    if other_exist:
        other = Product_Display.objects.get(user=request.user)
        if request.method == "POST":
            images = request.FILES['images']
            other.images = images
            other.save()
            messages.success(request, 'Your bathroom image is kept for display!')
            return redirect(url)
    else:
        if request.method == "POST":
            images = request.FILES['images']
            other = Product_Display(images=images, user=request.user)
            other.save()
            messages.success(request, 'Your bathroom image is kept for display!')
            return redirect(url)
    return render(request, 'product-detail-variable.html')



from django.shortcuts import render
from .models import Product, ReviewRating
from django.db.models import Q
from sklearn.ensemble import RandomForestRegressor






