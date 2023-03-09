from django.contrib import messages
from django.conf import settings

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf

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



def get(request, id, *args, **kwargs, ):

    place = OrderPlaced.objects.get(id=id)
    date = place.payment.created_at

    orders = OrderPlaced.objects.filter(user_id=request.user.id, payment__created_at=date)
    total = 0
    for o in orders:
        total = total + (o.product.price * o.quantity)
    addrs = Address_Book.objects.get(user_id=request.user.id,status=True)

    data = {
            "total": total,
            "orders": orders,
            "shipping": addrs,
        }
    pdf = render_to_pdf('report.html', data)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
            # filename = "Report_for_%s.pdf" %(data['id'])
        filename = "Bill"

        content = "inline; filename= %s" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Page Not Found")


import matplotlib.pyplot as plt
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from .models import OrderPlaced
from django.views.decorators.csrf import csrf_exempt
import matplotlib
matplotlib.use('Agg')


@csrf_exempt
def products_sold_by_month(request):
    data = OrderPlaced.objects.filter(is_ordered=True).annotate(month=ExtractMonth('ordered_date')).values(
        'month').order_by('month')

    months = [month[1] for month in OrderPlaced.MONTH_CHOICES]

    totals = [data.filter(month=month[0]).aggregate(total=Count('id'))['total'] for month in OrderPlaced.MONTH_CHOICES]

    plt.bar(months, totals)
    plt.title('Products sold by month')
    plt.xlabel('Month')
    plt.ylabel('Total')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Convert the plot to a Django view response
    from io import BytesIO
    import base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    # Render the template with the plot and URLs
    context = {
        'graphic': graphic,
    }
    return render(request, 'admin/products_sold_by_month.html', context)

