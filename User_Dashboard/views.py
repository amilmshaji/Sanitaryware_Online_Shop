from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Account, Address_Book
from orders.models import OrderPlaced
from shop_app.models import Product_Display, Product


@login_required(login_url='login')
def dashboard(request):
    # orders = Order.objects.order_by(
    #     '-created_at').filter(user_id=request.user.id, is_ordered=True)
    # order_count = orders.count()
    userprofile=Account.objects.get(id=request.user.id)
    context = {
        # 'orders_count': order_count,
        'userprofile':userprofile,
    }
    return render(request, 'dashboard/dash-my-profile.html', context)

@login_required(login_url='login')
def editprofile(request):
    # orders = Order.objects.order_by(
    #     '-created_at').filter(user_id=request.user.id, is_ordered=True)
    # order_count = orders.count()
    userprofile=Account.objects.get(id=request.user.id)

    if request.method == 'POST':
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        phone_number = request.POST.get("tel")

        userprofile.fname=fname
        userprofile.lname=lname
        userprofile.phone_number=phone_number
        userprofile.save()
        return redirect('myprofile')

    context = {
        # 'orders_count': order_count,
        'userprofile':userprofile,
    }
    return render(request, 'dashboard/dash-edit-profile.html', context)


@login_required(login_url='login')
def changePassword(request):
    if request.method == 'POST':
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']

        user=Account.objects.get(email__exact=request.user.email)

        if new_password == confirm_password:
            success=user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password change Successfully')
                return redirect('changePassword')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('changePassword')
        else:
            messages.error(request, 'Password does not match')
            return redirect('changePassword')
    return render(request, 'dashboard/change_password.html')

@login_required(login_url='login')
def addressbook(request):
    address =Address_Book.objects.all().filter(user=request.user.id)


    context = {
        'address': address,
    }
    return render(request, 'dashboard/dash-address-book.html', context)

@login_required(login_url='login')
def addressadd(request):
    if request.method == 'POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        phone_number=request.POST['tel']
        house = request.POST['house']
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        pin = request.POST['pin']

        profile=Address_Book(user=request.user,fname=fname,lname=lname,phone_number=phone_number,house=house,street=street,
                            city=city,state=state,pin=pin)
        profile.save()
        messages.success(request, 'New address is added...!')
        return redirect('addressbook')
    return render(request, 'dashboard/dash-address-add.html')

@login_required(login_url='login')
def addressedit(request,address_id):
    address = Address_Book.objects.get(id=address_id)
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        phone_number=request.POST['tel']
        house = request.POST['house']
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        pin = request.POST['pin']

        address.fname=fname
        address.lname=lname
        address.phone_number=phone_number
        address.house=house
        address.street=street
        address.city=city
        address.state=state
        address.pin=pin

        address.save()
        messages.success(request, 'your address is updated...!')
        return redirect('addressbook')

    context = {
            'address': address,
    }
    return render(request,'dashboard/dash-address-edit.html', context)

@login_required(login_url='login')
def address_set(request,address_id):
    url = request.META.get('HTTP_REFERER')
    all = Address_Book.objects.filter(user=request.user)
    for a in all:
        if a.status==True:
            a.status=False
            a.save()
    address = Address_Book.objects.get(id=address_id)
    address.status=True
    address.save()
    return redirect(url)


@login_required(login_url='login')
def my_orders(request):
    orders = OrderPlaced.objects.filter(
        user=request.user, is_ordered=True).order_by('ordered_date')
    # price=
    context = {
        'orders': orders,
    }
    return render(request, 'dashboard/dash-my-order.html', context)

# Import the library pygame
import pygame as pg
from pygame.locals import *

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
                        # pg.quit()
                        pg.image.save(screen, "screenshot.png")
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

