from django.contrib import messages
from django.conf import settings

from Sanitaryware_Shop.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from accounts.models import Address_Book

from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.
from cart.models import CartItem, Cart
from cart.views import _cart_id
import razorpay

from orders.models import Payment, OrderPlaced
from shop_app.models import Product


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_item=None):
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

        address = Address_Book.objects.get(user=request.user,status=True)

        tax = (2*total)/100
        razoramount = total*100
    except ObjectDoesNotExist:
        pass
    print(razoramount)
    customer=Address_Book.objects.filter(user=request.user,status=True)
    print(customer)

    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY,settings.RAZORPAY_API_SECRET_KEY))

    data = {
        "amount": total,
        "currency": "INR",
        "receipt": "order_rcptid_11"


    }
    payment_response = client.order.create(data=data)

    order_id = payment_response['id']
    request.session['order_id'] = order_id
    order_status = payment_response['status']
    if order_status == 'created':
        payment = Payment(user=request.user,
                          amount=total,
                          razorpay_order_id = order_id,
                          razorpay_payment_status = order_status)
        payment.save()

    context = {
        'razoramount':razoramount,
        'customer': customer,
        'address' : address,
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'checkout.html', context)

def payment_done(request):
    order_id=request.session['order_id']
    payment_id = request.GET.get('payment_id')
    print(payment_id)

    payment=Payment.objects.get(razorpay_order_id = order_id)

    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    customer=Address_Book.objects.get(user=request.user,status=True)

    cart=CartItem.objects.filter(user=request.user)
    # item = Product.objects.get(product=product, id=item_id)

    for c in cart:
        OrderPlaced(user=request.user,customer=customer,product=c.product,quantity=c.quantity,payment=payment,is_ordered=True).save()
        prod=Product.objects.get(product_name=c.product.product_name)
        prod.stock=prod.stock-c.quantity
        prod.save()
        c.delete()
    messages.success(request, 'Thank You for ordering...!')
    return redirect('my_orders')



