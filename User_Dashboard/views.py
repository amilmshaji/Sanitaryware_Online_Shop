from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Account, UserProfile


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
    return render(request, 'dashboard/dash-address-book.html')

def addressadd(request):
    return render(request, 'dashboard/dash-address-add.html')

