from django.shortcuts import render,get_object_or_404, redirect
from django.db.models import Avg
from .models import ChaiVariety
from cart.models import Cart
from .forms import ChaiReviewForm
from django.contrib.auth.decorators import login_required

def all_chai(request):
    chais = ChaiVariety.objects.all()
    cart_items = {}
    
    if request.user.is_authenticated:
        try:
            cart = request.user.cart
            for item in cart.items.all():
                chai_id = item.chai.id
                quantity = item.quantity 
                cart_items[chai_id] = quantity
        except Cart.DoesNotExist:  
            pass
    
    return render(request, 'chai/all_chai.html', {
        'chais': chais,
        'cart_items': cart_items
    })

def Chai_detail(request, chai_id):
    chai = get_object_or_404(ChaiVariety, pk=chai_id)
    reviews = chai.reviews.all().order_by('-created_at')

    # Calculate average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    avg_rating = round(avg_rating, 1)

    if request.method == "POST":
        form = ChaiReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.chai = chai
            review.user = request.user
            review.save()
            return redirect('chai_detail', chai_id=chai_id)
    else:
        form = ChaiReviewForm()

    return render(request, 'chai/chai_detail.html', {
        'chai': chai,
        'reviews': reviews,
        'form': form,
        'avg_rating': avg_rating,
    })

