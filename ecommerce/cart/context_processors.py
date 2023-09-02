from cart.models import Cart
def counter(request):
    count=0
    if request.user.is_authenticated:
        u=request.user
        try:
            c=Cart.objects.filter(user=u)
            for i in c:
                count+=i.quantity
        except:
            count=0
    return {'count':count}




