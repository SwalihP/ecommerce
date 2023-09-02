from django.shortcuts import render
from shop.models import Product
from django.db.models import Q
def searchresult(request):
    q=""
    p=None
    if (request.method=='POST'):
        q=request.POST['q']
        if (q):
            p=Product.objects.filter(Q(name__icontains=q) | Q(desc__icontains=q))
    return render(request,'search.html',{'q':q,'p':p})

