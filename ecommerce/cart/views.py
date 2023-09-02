from django.shortcuts import render,redirect
from shop.models import Product
from cart.models import Cart
from django.contrib.auth.decorators import login_required
from cart.models import Account
from cart.models import Order

@login_required
def add_cart(request,p):
    p=Product.objects.get(id=p)
    u=request.user
    try:
        c=Cart.objects.get(products=p,user=u)
        if c.quantity<c.products.stock:
            c.quantity+=1
            c.save()
    except Cart.DoesNotExist:
        c=Cart.objects.create(products=p,user=u,quantity=1)
        c.save()
    return redirect('cart:cartview')

@login_required
def cartview(request):
    total=0
    u=request.user
    try:
        c=Cart.objects.filter(user=u)
        for i in c:
            total+=i.quantity*i.products.price
    except Cart.DoesNotExist:
        pass
    return render(request,'cart.html',{'c':c,'t':total})
@login_required
def remove_cart(request,p):
    p=Product.objects.get(id=p)
    u=request.user
    try:
        c=Cart.objects.get(products=p,user=u)
        if c.quantity>1:
            c.quantity-=1
            c.save()
        else:
            c.delete()
    except Cart.DoesNotExist:
        pass
    return redirect('cart:cartview')
@ login_required
def delete_cart(request,p):
    p=Product.objects.get(id=p)
    u=request.user
    try:
        c=Cart.objects.get(products=p,user=u)
        c.delete()
    except Cart.DoesNotExist:
        pass

    return redirect('cart:cartview')
@login_required
def orderform(request):
    total=0
    if(request.method=="POST"):
        a=request.POST['a']
        p=request.POST['p']
        n=request.POST['n']
        u=request.user
        c=Cart.objects.filter(user=u)
        for i in c:
            total+=i.quantity*i.products.price
        ac=Account.objects.get(acctnumber=n)
        if (ac.amount >= total):
            ac.amount-=total
            ac.save()
            for i in c:
                o=Order.objects.create(user=u,products=i.products,address=a,phone=p,order_status="paid",noofitems=i.quantity)
                print(i.products.stock)
                i.products.stock-=i.quantity
                i.products.save()
                print(i.products.stock)
                o.save()
            c.delete()
            msg="Ordered successfully"
            return render(request,'orderdetail.html',{'msg':msg,'t':total})
        else:
            msg="Insufficient balance"
            return render(request,'orderdetail.html',{'msg':msg,})


    return render(request,'orderform.html')

@login_required
def orderview(request):
    u=request.user
    o=Order.objects.filter(user=u,order_status="paid")
    return render(request,'orderview.html',{'o':o,'name':u.username})


