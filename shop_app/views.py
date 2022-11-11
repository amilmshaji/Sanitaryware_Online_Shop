from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.core.checks import messages
from django.http.response import HttpResponse, HttpResponseRedirect

from .forms import ReviewForm
from .models import Category, Other_Product
from django.shortcuts import get_object_or_404, redirect, render
from . models import Product, ReviewRating, Productgallery
from cart.models import CartItem, Cart
from cart.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages

# Python program to move the image
# with the mouse

# Import the library pygame
import pygame as pg
from pygame.locals import *


# Create your views here.
def Home(request,category_slug=None):
    categories = None
    products = None

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
    }
    return render(request, 'index.html', context)


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True)
        paginator = Paginator(products, 1)
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
    }
    return render(request, 'shop.html', context)


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
        if keyword:
            products = Product.objects.order_by(
                'created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'shop.html', context)

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
    if request.method=="POST":
        images=request.FILES['images']
        other=Other_Product(images=images,user=request.user)
        other.save()
        messages.success(request, 'Your bathroom image is kept for display!')

        return redirect(url)
    return render(request, 'product-detail-variable.html')





def p(request, product_id):
    url = request.META.get('HTTP_REFERER')
    h_products = Other_Product.objects.filter(user=request.user)
    product = Product.objects.get(id=product_id)
    print(h_products)
    for i in h_products:
        user=i.user
        images=i.images



    # Take colors input
    YELLOW = (255, 255, 0)
    BLUE = (0, 0, 255)


    # Construct the GUI game
    pg.init()
    pg.display.set_caption('Your Bathroom Design')

    # Set dimensions of game GUI
    w, h = 1200, 600
    screen = pg.display.set_mode((w, h))
    WIDTH = 200
    HEIGHT = 200


    # Set the size for the image
    DEFAULT_IMAGE_SIZE = (WIDTH, HEIGHT)

    # Take image as input
    img = pg.image.load(product.display)

    # Scale the image to your needed size
    img = pg.transform.scale(img, DEFAULT_IMAGE_SIZE)

    img1 = pg.image.load(images)
    img.convert()
    img1.convert()
    img2 = pg.transform.scale(img1, (1200, 600))

    # Draw rectangle around the image

    rect = img.get_rect()
    rect.center = w // 2, h // 2

    # Set running and moving values
    running = True
    moving = False


    # stores the width of the
    # screen into a variable
    width = screen.get_width()

    # stores the height of the
    # screen into a variable
    height = screen.get_height()





    # Setting what happens when game
    # is in running state
    while running:
        # events = pg.event.get()

        #zoom out function

        # button_down = pg.mouse.get_pressed()
        # if button_down == (1, 0, 0):
        #     print("Clicked")
        #     WIDTH = WIDTH + 10
        #     HEIGHT = HEIGHT + 10
        #     img = pg.transform.scale(img, (WIDTH, HEIGHT))


        for event in pg.event.get():

            # Close if the user quits the
            # game
            if event.type == QUIT:
                running = False

            # Making the image move
            elif event.type == MOUSEBUTTONDOWN:
                if rect.collidepoint(event.pos):
                    moving = True

            # Set moving as False if you want
            # to move the image only with the
            # mouse click
            # Set moving as True if you want
            # to move the image without the
            # mouse click
            elif event.type == MOUSEBUTTONUP:
                moving = False

            # Make your image move continuously
            elif event.type == MOUSEMOTION and moving:
                rect.move_ip(event.rel)


            if event.type == pg.MOUSEBUTTONDOWN:  #if condition for buttons

                mouse = pg.mouse.get_pos()
                w1=1056
                h1=230
                h2=160
                if w1 <= mouse[0] <= w1 + 140 and h1 <= mouse[1] <= h1 + 40:    # if the mouse is clicked on the button the game is terminated
                    pg.quit()
                    return redirect(url)

                elif w1 <= mouse[0] <= w1 + 140 and h2 <= mouse[1] <= h1 + 40:
                    pg.quit()
                    return redirect(url)


        screen.fill(YELLOW)           # Set screen color and image on screen
        screen.blit(img2, (0, 0))
        screen.blit(img, rect)


        start_button = pg.draw.rect(screen, (0, 0, 240), (1050, 90, 100, 50));
        continue_button = pg.draw.rect(screen, (0, 244, 0), (1050, 160, 100, 50));
        quit_button = pg.draw.rect(screen, (244, 0, 0), (1050, 230, 100, 50));


        # Construct the border to the image
        pg.draw.rect(screen, BLUE, rect, 2)

        # Update the GUI pygame
        pg.display.update()

    # Quit the GUI game
    pg.quit()
    return redirect(url)

