from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Account, Address_Book
from orders.models import OrderPlaced


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


def addressbook(request):
    address =Address_Book.objects.all().filter(user=request.user.id)


    context = {
        'address': address,
    }
    return render(request, 'dashboard/dash-address-book.html', context)

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
    context = {
        'orders': orders,
    }
    return render(request, 'dashboard/dash-my-order.html', context)



