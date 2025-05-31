from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from cart.models import Order
from chai.models import ChaiReview

def home(request):
    reviews=ChaiReview.objects.all()
    return render(request,'index.html',{
        'reviews':reviews
    })

@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)
    orders=orders.order_by('ordered_at')
    return render(request,'account.html',{
        'user':request.user,
        'orders':orders,
    })
