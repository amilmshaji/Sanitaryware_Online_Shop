from django.contrib.auth.decorators import login_required
from django.core.checks import messages

from .forms import ReviewForm
from .models import Category, Product_Display, Info
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
                'created_date').filter(Q(product_name__icontains=keyword))
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
            products = Product.objects.filter(Q(product_name__icontains=keyword))
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





def p(request, product_id):
    url = request.META.get('HTTP_REFERER')
    h_products = Product_Display.objects.filter(user=request.user)
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


    DEFAULT_IMAGE_SIZE = (WIDTH, HEIGHT)  # Set the size for the image

    img = pg.image.load(product.display)  # Take image as input -product image
    img4 = pg.image.load(product.display2)  # Take image as input -product image
    img5 = pg.image.load(product.display3)  # Take image as input -product image


    img = pg.transform.scale(img, DEFAULT_IMAGE_SIZE)  # Scale the image to your needed size
    img4 = pg.transform.scale(img4, DEFAULT_IMAGE_SIZE)  # Scale the image to your needed size
    img5 = pg.transform.scale(img5, DEFAULT_IMAGE_SIZE)  # Scale the image to your needed size



    img1 = pg.image.load(images) #design image background
    img.convert()
    img1.convert()
    img4.convert()
    img5.convert()


    img2 = pg.transform.scale(img1, (1200, 600))



    # Draw rectangle around the image
    rect1 = img.get_rect()
    rect1.x = 40   #initial position of image 1
    rect1.y = 0

    rect2 = img4.get_rect() #initial postion of image 2
    rect2.x = 40
    rect2.y = 200

    rect3 = img5.get_rect()  # initial postion of image 3
    rect3.x = 40
    rect3.y = 400

    # Set running and moving values
    running = True
    moving = False
    moving2 = False
    moving3 = False


    # stores the width of the
    # screen into a variable
    width = screen.get_width()


    # stores the height of the
    # screen into a variable
    height = screen.get_height()


    # Setting what happens when game
    # is in running state

    while running:
        for event in pg.event.get():

            # Close if the user quits the window
            if event.type == QUIT:
                running = False

            # Making the images move
            elif event.type == MOUSEBUTTONDOWN:
                if rect1.collidepoint(event.pos):
                    moving = True
                if rect2.collidepoint(event.pos):
                    moving2 = True
                if rect3.collidepoint(event.pos):
                    moving3 = True

            elif event.type == MOUSEBUTTONUP:  # Set moving as False if you want to move the image only with the mouse click
                moving = False  # Set moving as True if you want to move the image without the mouse click
                moving2 = False
                moving3 = False



            elif event.type == MOUSEMOTION and moving:  # Make your image move continuously

                rect1.move_ip(event.rel)
            elif event.type == MOUSEMOTION and moving2:  # Make your image 2 move continuously

                rect2.move_ip(event.rel)
            elif event.type == MOUSEMOTION and moving3:  # Make your image 2 move continuously

                rect3.move_ip(event.rel)

            if event.type == pg.MOUSEBUTTONDOWN:  #if condition for buttons

                mouse = pg.mouse.get_pos()
                w1=1056
                h1=90
                h2=160
                h3=230
                if w1 <= mouse[0] <= w1 + 140 and h1 <= mouse[1] <= h1 + 40:
                    if WIDTH <= 220 and HEIGHT <= 220:# zoom out product image
                        WIDTH = WIDTH + 5
                        HEIGHT = HEIGHT + 5
                        img = pg.transform.scale(img, (WIDTH, HEIGHT))

                elif w1 <= mouse[0] <= w1 + 140 and h2 <= mouse[1] <= h2 + 40:  # zoom in product image
                    if WIDTH >= 180 and HEIGHT >= 180:

                        WIDTH = WIDTH - 5
                        HEIGHT = HEIGHT - 5
                        img = pg.transform.scale(img, (WIDTH, HEIGHT))

                elif w1 <= mouse[0] <= w1 + 140 and h3 <= mouse[1] <= h3 + 40:  # quit window button
                    pg.quit()
                    return redirect(url)

            if event.type == pg.MOUSEBUTTONDOWN:  #if condition for buttons for second image

                mouse = pg.mouse.get_pos()
                w1=1056
                h1=90
                h2=160
                h3=230
                if w1 <= mouse[0] <= w1 + 140 and h1 <= mouse[1] <= h1 + 40:
                    if WIDTH <= 220 and HEIGHT <= 220:# zoom out product image 2
                        WIDTH = WIDTH + 5
                        HEIGHT = HEIGHT + 5
                        img4 = pg.transform.scale(img4, (WIDTH, HEIGHT))

                elif w1 <= mouse[0] <= w1 + 140 and h2 <= mouse[1] <= h2 + 40:  # zoom in product image2
                    if WIDTH >= 180 and HEIGHT >= 180:

                        WIDTH = WIDTH - 5
                        HEIGHT = HEIGHT - 5
                        img4 = pg.transform.scale(img4, (WIDTH, HEIGHT))

                elif w1 <= mouse[0] <= w1 + 140 and h3 <= mouse[1] <= h3 + 40:  # quit window button
                    pg.quit()
                    return redirect(url)

                if event.type == pg.MOUSEBUTTONDOWN:  # if condition for buttons for second image

                    mouse = pg.mouse.get_pos()
                    w1 = 1056
                    h1 = 90
                    h2 = 160
                    h3 = 230
                    if w1 <= mouse[0] <= w1 + 140 and h1 <= mouse[1] <= h1 + 40:
                        if WIDTH <= 220 and HEIGHT <= 220:  # zoom out product image 2
                            WIDTH = WIDTH + 5
                            HEIGHT = HEIGHT + 5
                            img5 = pg.transform.scale(img5, (WIDTH, HEIGHT))

                    elif w1 <= mouse[0] <= w1 + 140 and h2 <= mouse[1] <= h2 + 40:  # zoom in product image2
                        if WIDTH >= 180 and HEIGHT >= 180:
                            WIDTH = WIDTH - 5
                            HEIGHT = HEIGHT - 5
                            img5 = pg.transform.scale(img5, (WIDTH, HEIGHT))

                    elif w1 <= mouse[0] <= w1 + 140 and h3 <= mouse[1] <= h3 + 40:  # quit window button
                        pg.quit()
                        return redirect(url)



        screen.fill(YELLOW)  # set screen color and image on screen
        screen.blit(img2, (0, 0))
        screen.blit(img, rect1)
        screen.blit(img4, rect2)
        screen.blit(img5, rect3)

        # Define colors
        background_color = (0, 0, 0)
        primary_color = (0, 200, 100)
        secondary_color = (200, 0, 0)
        text_color = (255, 255, 255)

        # Define button dimensions
        button_width = 100
        button_height = 50
        button_padding = 10
        start_button_rect = pg.Rect(1050, 90, button_width, button_height)
        continue_button_rect = pg.Rect(1050, 160, button_width, button_height)
        quit_button_rect = pg.Rect(1050, 230, button_width, button_height)

        # Draw buttons
        pg.draw.rect(screen, primary_color, start_button_rect)
        pg.draw.rect(screen, primary_color, continue_button_rect)
        pg.draw.rect(screen, secondary_color, quit_button_rect)

        # Draw button text
        button_font = pg.font.SysFont('Helvetica', 20)
        start_text = button_font.render('Zoom OUT', True, text_color)
        continue_text = button_font.render('Zoom IN', True, text_color)
        quit_text = button_font.render('Quit', True, text_color)
        screen.blit(start_text, (start_button_rect.x + button_padding, start_button_rect.y + button_padding))
        screen.blit(continue_text, (continue_button_rect.x + button_padding, continue_button_rect.y + button_padding))
        screen.blit(quit_text, (quit_button_rect.x + button_padding, quit_button_rect.y + button_padding))

        # Add icons
        quit_icon = button_font.render('X', True, text_color)
        screen.blit(quit_icon, (quit_button_rect.x + button_padding, quit_button_rect.y + button_padding))

        # Update the GUI pygame
        pg.display.update()

    # Quit the GUI game
    pg.quit()
    return redirect(url)

