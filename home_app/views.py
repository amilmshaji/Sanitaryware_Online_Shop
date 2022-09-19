


def Contact(request):
    return render(request,"contact.html")

def Category(request):
    return render(request,"category.html")

def Blog(request):
    return render(request,"blog.html")

def Checkout(request):
    return render(request,"checkout.html")

def Cart(request):
    return render(request,"cart.html")


from django.shortcuts import render
from django.contrib import messages, auth
from django.shortcuts import render, redirect
from .models import Account
from django.contrib.auth import authenticate
6
# Create your views here.

def Home(request):
    return render(request,"index.html")


def login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(email=email, password=password)
        print(email)
        print(password)
        print(user)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are logged in')
            # store user details in session
            request.session['email']=email
            return redirect('home')
        else:
            messages.error(request, 'invalid login credentials')
            return redirect('register')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']
        fname=request.POST['fname']
        lname=request.POST['lname']
        phone_number=request.POST['tel']
        print(email,password,fname,lname,phone_number)
        if Account.objects.filter(email=email).exists():
            messages.error(request, 'email already exists')
            return redirect('register')
        # elif Account.objects.filter(username=username).exists():
        #     messages.error(request, 'username already exists')
        #     return redirect('register')
        else:
            user=Account.objects.create_user(email=email, password=password, fname=fname, lname=lname,  phone_number=phone_number)
            user.save()
            messages.success(request, 'you are registered')
            return redirect('/login')
    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


# from django.contrib import messages, auth
# from django.shortcuts import render, redirect
# from .models import reg_user,log_user
# from django.contrib.auth import authenticate
# from hashlib import sha256

# def register(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         username = request.POST['username']
#         phone_number = request.POST['tel']
#         password = sha256(password.encode()).hexdigest()
#         print(email, password, fname, lname, username, phone_number)
#         if reg_user.objects.filter(email=email).exists():
#             messages.error(request, 'email already exists')
#             return redirect('register')
#         else:
#             user=reg_user(email=email,  fname=fname, lname=lname, username=username, phone_number=phone_number)
#             log=log_user(email=email,password=password)
#             user.save()
#             log.save()
#             messages.success(request, 'you are registered')
#             return redirect('/login')
#     return render(request, 'register.html')
#
# # Login Function
#
# def login(request):
#     if 'email' in request.session:
#         return redirect('home')
#     if request.method=='POST':
#         email=request.POST['email']
#         password=request.POST['password']
#         password2 = sha256(password.encode()).hexdigest()
#         user=log_user.objects.filter(email=email,password=password2)
#         if user:
#             user_details=log_user.objects.get(email=email,password=password2)
#             email=user_details.email
#             request.session['email']=email
#             return redirect('home')
#         # else:
#         #     messages.error(request, 'invalid login credentials')
#         #     return redirect('register')/
#
#     return render(request,'login.html')
