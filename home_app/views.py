from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def Home(request):
    return render(request,"index.html")

def Contact(request):
    return render(request,"contact.html")

def Login(request):
    return render(request,"login.html")

def Register(request):
    return render(request,"register.html")

def Category(request):
    return render(request,"category.html")

def Blog(request):
    return render(request,"blog.html")

def Checkout(request):
    return render(request,"checkout.html")

def Cart(request):
    return render(request,"cart.html")

