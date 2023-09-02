from django.shortcuts import render
from shop.models import Category
from shop.models import Product
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
def home(request):
    c=Category.objects.all()
    return render(request,'category.html',{'c':c})

def products(request,s):
    c=Category.objects.get(slug=s)
    s=Product.objects.filter(category__slug=s)
    return render(request,'products.html',{'s':s,'c':c})

def prodetails(request,s):
    p=Product.objects.get(slug=s)
    return render(request,'details.html',{'p':p})

def register(request):
    if(request.method=='POST'):
        u=request.POST['u']
        p=request.POST['p']
        c=request.POST['c']
        e=request.POST['e']
        f=request.POST['f']
        l=request.POST['l']
        if(p==c):
            u=User.objects.create_user(username=u,password=p,email=e,first_name=f,last_name=l)
            u.save()
            return home(request)
        else:
            messages.error(request,"INCORRECT PASSWORD")
    return render(request,'register.html')

def user_login(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p=request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return home(request)
        else:
            messages.error(request,"Invalid Username or Password")
    return render(request,'login.html')

def user_logout(request):
    logout(request)
    return home(request)
