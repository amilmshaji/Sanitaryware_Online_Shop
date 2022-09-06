from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def Home(request):
    return render(request,"index.html")

def Contact(request):
    return render(request,"contact.html")

# def Login(request):
#     return render(request,"login.html")

# def Register(request):
#     return render(request,"register.html")

def Category(request):
    return render(request,"category.html")

def Blog(request):
    return render(request,"blog.html")

def Checkout(request):
    return render(request,"checkout.html")

def Cart(request):
    return render(request,"cart.html")

from django.contrib import messages, auth
from django.shortcuts import render, redirect
from .models import Account




# Create your views here.

def login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are logged in')
            request.session['email']=email
            request.session['name']=user.name
            # store user details in session
            request.session['district']=user.district
            return redirect('home')
        else:
            messages.error(request, 'invalid login credentials')
            return redirect('/')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        fname=request.POST['fname']
        # mun_name=request.POST['mun_name']
        lname=request.POST['lname']
        city=request.POST['city']

        state=request.POST['state']
        district=request.POST['district']
        phone_number=request.POST['tel']
        print(email,password,fname,lname,city,state,district,phone_number)
        if Account.objects.filter(email=email).exists():
            messages.error(request, 'email already exists')
            return redirect('login/')
        # elif Account.objects.filter(lname=lname).exists():
        #     messages.error(request, 'username already exists')
        #     return redirect('register')
        else:
            user=Account.objects.create_user(email=email, password=password, fname=fname, lname=lname, city=city,state=state, district=district,  phone_number=phone_number)
            user.save()
            messages.success(request, 'you are registered')
            return redirect('login/')
    return render(request, 'register.html')

