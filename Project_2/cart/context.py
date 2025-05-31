from .models import Cart

def cart_context(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = None
    return {'cart': cart}
