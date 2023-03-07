from django.contrib import messages

from . models import Cart, CartItem
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from shop_app.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


#for timer in cart
from datetime import datetime, timedelta
from django.utils import timezone

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

@login_required(login_url='login')
def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)

    # Check if the product is currently locked
    cart_item = CartItem.objects.filter(product=product, is_active=True).exclude(user=current_user).first()
    if cart_item and cart_item.reserved_until > timezone.now():
        time_left = cart_item.reserved_until - timezone.now()
        messages.success(request, f"This product is currently locked for {time_left.seconds } seconds.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # Lock the product for 2 minutes
    reserved_until = timezone.now() + timedelta(minutes=2)

    if current_user.is_authenticated:
        is_cart_item_exist = CartItem.objects.filter(
            product=product, user=current_user, is_active=True).exists()
        if is_cart_item_exist:
            cart_item = CartItem.objects.get(
                product=product, user=current_user, is_active=True)
            if product.stock > cart_item.quantity:
                cart_item.quantity += 1
                cart_item.save()
                messages.success(request, "Cart item updated.")
            else:
                messages.success(request, "No more stock to add!")
        else:
            cart_item = CartItem.objects.create(
                product=product, quantity=1, user=current_user, reserved_until=reserved_until)
            cart_item.save()
            messages.success(request, "Cart item added.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        is_cart_item_exist = CartItem.objects.filter(
            product=product, cart=cart, is_active=True).exists()
        if is_cart_item_exist:
            cart_item = CartItem.objects.get(
                product=product, cart=cart, is_active=True)
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
                reserved_until=reserved_until,
            )
            cart_item.save()
        messages.success(request, "Cart item added.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(
            product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_item=None, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price*cart_item.quantity)
            quantity += cart_item.quantity
        # tax = (2*total)/100
        # grand_total = total
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        # 'tax': tax,
        # 'grand_total': grand_total,
    }

    return render(request, 'cart.html', context)

